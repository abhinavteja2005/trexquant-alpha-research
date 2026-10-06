"""Collect crashed / failed / empty alphas for the Crash Analyst (handoff/cycle.md).

Usage:
  python tools/crash_report.py                       # from alphas/registry.csv
  python tools/crash_report.py --snapshot <file>     # also from a ledger_sync snapshot (states + err text)
Writes alphas/crashes/pending.json: crashes not yet diagnosed in knowledge/crashes.md, each with its
expression (from alphas/drafts/*.json or alphas/crashes/exprs.json) or expr=null. For missing expressions it
prints CRASH_JS: run it in the runner tab; it returns CODE ONLY (comments removed, so no URLs and the Chrome
filter passes it). Save the output to alphas/crashes/exprs.json as {tag: code}.
"""
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "alphas" / "crashes" / "pending.json"
EXPRS = ROOT / "alphas" / "crashes" / "exprs.json"
LOG = ROOT / "knowledge" / "crashes.md"
CRASH_STATUS = re.compile(r"FAIL|CRASH|EMPTY|TIMEOUT|ERROR", re.I)
CRASH_STATE = {"ffail", "sfail", "ftimeout", "stimeout", "subfail"}

CRASH_JS = r"""
const want = %s;
(window.R ? R.jobs : JSON.parse(localStorage.R3_jobs || '[]')).filter(j => want.includes(j.tag))  /* read-only */.map(j => ({tag: j.tag, state: j.state, lb: j.lb, wlb: j.wlb,
  err: String(j.err || j.subErr || '').replace(/[^A-Za-z0-9 _.:-]/g, ' ').slice(0, 160),
  code: j.expr.split('\n').map(l => l.replace(/#.*$/, '').trimEnd()).filter(l => l.trim()).join('\n')}))
"""


def drafts():
    out = {}
    for f in sorted((ROOT / "alphas" / "drafts").glob("*.json")):
        for it in json.loads(f.read_text(encoding="utf-8")):
            out[it["tag"]] = (it["expr"], f.name)
    if EXPRS.exists():
        for tag, code in json.loads(EXPRS.read_text(encoding="utf-8")).items():
            out.setdefault(tag, (code, "crashes/exprs.json (code only)"))
    return out


def diagnosed():
    if not LOG.exists():
        return set()
    return set(re.findall(r"^\|\s*([A-Za-z0-9_]+)\s*\|", LOG.read_text(encoding="utf-8"), re.M)) - {"Tag"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot")
    a = ap.parse_args()
    found = {}
    reg = ROOT / "alphas" / "registry.csv"
    if reg.exists():
        for r in csv.DictReader(reg.open(encoding="utf-8")):
            empty = r.get("slow_ir") in ("0", "0.0") and r.get("slow_tvr") in ("0", "0.0")
            if CRASH_STATUS.search(r["status"]) or empty:
                found[r["tag"]] = {"tag": r["tag"], "status": r["status"], "err": "", "lb": r.get("lookback", "")}
    if a.snapshot:  # ledger_sync row format: tag|state|lb|wlb|...|err (last field)
        for line in Path(a.snapshot).read_text(encoding="utf-8").splitlines():
            c = line.strip().strip('",').split("|")
            if len(c) > 4 and (c[1] in CRASH_STATE or (c[11:13] == ["0", "0"])):
                found.setdefault(c[0], {"tag": c[0], "status": c[1], "lb": c[2]}).update(err=c[-1], wlb=c[3])
    d, done = drafts(), diagnosed()
    pending = []
    for tag, row in found.items():
        if tag in done:
            continue
        expr, src = d.get(tag, (None, None))
        pending.append({**row, "expr": expr, "expr_source": src})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(pending, indent=1), encoding="utf-8")
    missing = [p["tag"] for p in pending if not p["expr"]]
    print(f"{len(pending)} undiagnosed crashes -> {OUT.relative_to(ROOT)} ({len(missing)} without expression)")
    for p in pending:
        print(f"  {p['tag']:22} {p['status'][:45]:45} expr: {p['expr_source'] or 'MISSING'}")
    if missing:
        print("\nRun in the runner tab, save the result to alphas/crashes/exprs.json as {tag: code}:")
        print(CRASH_JS % json.dumps(missing))


if __name__ == "__main__":
    main()
