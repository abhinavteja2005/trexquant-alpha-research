"""Originality check for alpha drafts (B1): weighted-Jaccard overlap of code fingerprints.

Usage:
  python tools/originality.py alphas/drafts/c1.json [--json]
Fingerprint = multiset of known variables, operators and integer window args (>= 2),
comments stripped, local names ignored. Compared with every alpha in alphas/drafts/*.json
that has a ledger row (tested), and with submitted ones. Reject > .8, warn > .6.
Exit code 1 if any draft is rejected.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

from check_alpha import IDENT, OPERATORS, ROOT, VARS, strip_comment

REJECT, WARN = 0.8, 0.6


def fingerprint(expr):
    code = "\n".join(strip_comment(l) for l in expr.splitlines())
    local = set(re.findall(r"^\s*([A-Za-z_]\w*)\s*=(?!=)", code, re.M))  # locally assigned names
    fp = Counter()
    for m in IDENT.finditer(code):
        n = m.group()
        if m.start() > 0 and (code[m.start() - 1].isdigit() or code[m.start() - 1] == "."):
            continue  # part of a number like 1e5
        if n not in local and (n in VARS or n in OPERATORS):
            fp[n] += 1
    # integer literals >= 2 that are call arguments (windows): preceded by ',' and followed by ',' or ')'
    for m in re.finditer(r"[,(]\s*(\d+)\s*(?=[,)])", code):
        if int(m.group(1)) >= 2:
            fp["#" + m.group(1)] += 1
    return fp


def skeleton(expr):
    """Comment-free code with integers masked and local names numbered: equal skeletons = same alpha
    up to windows/constants."""
    code = "\n".join(strip_comment(l) for l in expr.splitlines() if strip_comment(l).strip())
    local = list(dict.fromkeys(re.findall(r"^\s*([A-Za-z_]\w*)\s*=(?!=)", code, re.M)))
    for i, n in enumerate(local):
        code = re.sub(rf"(?<![\w.]){re.escape(n)}(?!\w)", f"L{i}_", code)
    return re.sub(r"\s+", "", re.sub(r"(?<![\w.])\d+(\.\d+)?(?![\w.])", "N", code))


def jaccard(a, b):
    keys = set(a) | set(b)
    den = sum(max(a[k], b[k]) for k in keys)
    return sum(min(a[k], b[k]) for k in keys) / den if den else 0.0


def ledger_rows():
    """tag -> submitted flag, for every ledger row."""
    rows = {}
    for line in (ROOT / "alphas" / "ledger.md").read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.split("|")]
        if len(c) > 13 and c[2] and c[2] not in {"Tag", "---"} and not c[2].startswith("-"):
            rows[c[2]] = c[13].lower() == "yes"
    return rows


def references():
    """tag -> (fingerprint, submitted, skeleton) for every tested draft (one with a ledger row)."""
    rows, refs = ledger_rows(), {}
    for f in (ROOT / "alphas" / "drafts").glob("*.json"):
        for it in json.loads(f.read_text(encoding="utf-8")):
            if it["tag"] in rows:
                refs[it["tag"]] = (fingerprint(it["expr"]), rows[it["tag"]], skeleton(it["expr"]))
    return refs


def main(argv):
    p = Path(argv[0]).resolve()
    items = json.loads(p.read_text(encoding="utf-8"))
    # the file under test is NOT excluded wholesale: tested tags in it count as references
    # (the same-tag skip below prevents self-comparison)
    refs = references()
    parent = {it["tag"]: it.get("parent") for it in items}
    out = []
    for n, it in enumerate(items):
        fp, sk = fingerprint(it["expr"]), skeleton(it["expr"])
        best, who = 0.0, "-"
        # earlier untested drafts in the same file count too (catches sibling duplicates)
        pool = list(refs.items()) + [(x["tag"], (fingerprint(x["expr"]), False, skeleton(x["expr"])))
                                     for x in items[:n] if x["tag"] not in refs]
        for tag, (rfp, sub, rsk) in pool:
            if tag == it["tag"]:
                continue
            s = jaccard(fp, rfp)
            if s < 1 and sk == rsk:
                s = max(s, REJECT + 0.01)  # same code up to windows/constants
            par = it.get("parent")
            if par and (tag == par or parent.get(tag) == par) and s < 1 and sk != rsk:
                continue  # a deliberate repair/mutation of its parent (exact copies are never exempt)
            if s > best:
                best, who = s, tag + (" (submitted)" if sub else "")
        status = "REJECT" if best > REJECT else "WARN" if best > WARN else "OK"
        out.append({"tag": it["tag"], "max_sim": round(best, 3), "closest": who, "status": status})
    if "--json" in argv:
        print(json.dumps(out, indent=1))
    else:
        for r in out:
            print(f"{r['status']:6} {r['tag']}  max={r['max_sim']:.2f}  closest={r['closest']}")
        c = Counter(r["status"] for r in out)
        print(f"{c['OK']} ok, {c['WARN']} warn, {c['REJECT']} rejected of {len(out)}")
    return 1 if any(r["status"] == "REJECT" for r in out) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
