"""Merge a runner metrics snapshot into alphas/ledger.md and alphas/runner-export.json.

The Chrome privacy filter redacts expressions (they contain URLs), so the runner only gives us
metrics. Expressions come from alphas/drafts/*.json, joined on tag.

1. In the Trexsim tab run SNAPSHOT_JS (below) and save the returned lines, one per row, to
   alphas/snapshots/<YYYYMMDD-HHMM>.txt
2. python tools/ledger_sync.py alphas/snapshots/<file>.txt

Row format: tag|state|lb|wlb|f_ir|f_tvr|f_irtvr|f_corr|f_elig|f_rw|f_best|s_ir|s_tvr|s_irtvr|s_corr|s_corrId|
            s_corrIrTvr|s_corrOwn|s_elig|s_oos1|s_rw|s_best|s_vt|err
The S corr cell reads ".720@605850 (irtvr .111 vs bar .203)", "own" when the blocker is ours.
Full metrics (incl. Slow TVR, OOS1, recency IR, best-year share, verdict) go to runner-export.json.
Ledger rows are keyed by tag: a new tag is appended, an existing row is updated in place.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "alphas" / "ledger.md"
EXPORT = ROOT / "alphas" / "runner-export.json"

SNAPSHOT_JS = r"""
const F=x=>x?[x.ir,x.tvr,x.irtvr,x.corr,x.elig?1:0,x.st&&x.st.rw,x.st&&x.st.best]:['','','','','','',''];
const S=x=>x?[x.ir,x.tvr,x.irtvr,x.corr,x.corrId,x.corrIrTvr,x.corrOwn?1:0,x.elig?1:0,x.st&&x.st.oos1,x.st&&x.st.rw,x.st&&x.st.best,x.vt]:Array(12).fill('');
R.jobs.filter(j=>j.f||j.s||/fail|timeout|submitted/.test(j.state))
 .map(j=>[j.tag,j.state,j.lb||'',j.wlb||'',...F(j.f),...S(j.s),String(j.err||j.subErr||'').replace(/[^A-Za-z0-9 _.:-]/g,' ').slice(0,60)].join('|'))
"""
FIELDS = ["tag", "state", "lb", "wlb", "f_ir", "f_tvr", "f_irtvr", "f_corr", "f_elig", "f_rw", "f_best",
          "s_ir", "s_tvr", "s_irtvr", "s_corr", "s_corrId", "s_corrIrTvr", "s_corrOwn", "s_elig",
          "s_oos1", "s_rw", "s_best", "s_vt", "err"]
HEADER = ["Time (IST)", "Tag", "Family", "F IR", "F TVR", "F IR/sqrtTVR", "F corr", "F E",
          "S IR", "S corr", "S E", "State", "Submitted"]


def num(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return ""
    s = f"{x:.3f}"
    return s.replace("0.", ".", 1) if abs(x) < 1 else s  # ledger style: .076


def yes_no(v):
    return {"1": "yes", "0": "no"}.get(v, "")


def drafts_by_tag():
    out = {}
    for f in sorted((ROOT / "alphas" / "drafts").glob("*.json")):
        for it in json.loads(f.read_text(encoding="utf-8")):
            out[it["tag"]] = it
    return out


def parse_snapshot(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip().strip('",')
        if line.count("|") < len(FIELDS) - 1:
            continue
        rows.append(dict(zip(FIELDS, line.split("|", len(FIELDS) - 1))))
    return rows


def ledger_row(r, family, old):
    f_done, s_done = r["f_ir"] != "", r["s_ir"] != ""
    if old and not f_done:  # keep hand-entered Fast cells (e.g. rows written before this tool)
        fast = old[3:8]
    else:
        fast = [num(r["f_ir"]), num(r["f_tvr"]), num(r["f_irtvr"]), num(r["f_corr"]),
                yes_no(r["f_elig"]) if f_done else ""]
    if s_done:
        s_corr = num(r["s_corr"]) + (f"@{r['s_corrId']}" if r["s_corrId"] else "")
        if r["s_corrOwn"] == "1":
            s_corr += " own"
        if r["s_corrIrTvr"] not in ("", "null"):
            s_corr += f" (irtvr {num(r['s_irtvr'])} vs bar {num(1.2 * float(r['s_corrIrTvr']))})"
        slow = [num(r["s_ir"]), s_corr, yes_no(r["s_elig"])]
    else:
        slow = old[8:11] if old else ["", "", ""]
    submitted = r["state"] == "submitted" or (old is not None and old[12].upper() == "YES")
    return [old[0] if old else datetime.now().strftime("%b %d %H:%M").replace(" 0", " "),
            r["tag"], family, *fast, *slow, r["state"], "YES" if submitted else "no"]


def main(path):
    rows, drafts = parse_snapshot(path), drafts_by_tag()
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    index = {}
    for i, l in enumerate(lines):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) == len(HEADER) and cells[1] not in {"Tag", "---"}:
            index[cells[1]] = (i, cells)
    added = updated = 0
    for r in rows:
        d = drafts.get(r["tag"], {})
        old = index.get(r["tag"])
        family = (old[1][2] if old else "") or d.get("family") or d.get("base") or r["tag"].split("_")[0]
        new = ledger_row(r, family, old[1] if old else None)
        text = "| " + " | ".join(new) + " |"
        if old:
            if [c for c in old[1]] != new:
                lines[old[0]] = text
                updated += 1
        else:
            lines.append(text)
            index[r["tag"]] = (len(lines) - 1, new)
            added += 1
    LEDGER.write_text("\n".join(lines) + "\n", encoding="utf-8")

    export = {r["tag"]: {**r, "expr": drafts.get(r["tag"], {}).get("expr"),
                         "family": drafts.get(r["tag"], {}).get("family")} for r in rows}
    if EXPORT.exists():
        prev = json.loads(EXPORT.read_text(encoding="utf-8"))
        for k, v in prev.items():
            if k in export and not export[k]["expr"]:
                export[k]["expr"] = v.get("expr")
        export = {**prev, **export}
    EXPORT.write_text(json.dumps(export, indent=1), encoding="utf-8")
    print(f"ledger: {added} added, {updated} updated; export: {len(export)} jobs "
          f"({sum(1 for v in export.values() if v.get('expr'))} with expr)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(SNAPSHOT_JS)
        sys.exit(0)
    main(sys.argv[1])
