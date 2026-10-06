"""Build alphas/queue/next.json for window.R.add from checked drafts.

Usage: python tools/make_queue.py SLOW:alphas/drafts/c1.json FAST:alphas/drafts/a101.json
SLOW items get state 'squeued' and an explicit Slow lookback; FAST items get state 'queued'.
Only drafts that PASS check_alpha and are not already in the ledger are included, in the given order.
Lookback = the draft's own `lb` if it has one, else 2 x the longest window + 20 (min 60); capped at 300.
"""
import json
import re
import sys
from pathlib import Path

from check_alpha import check, known_items

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "alphas" / "queue" / "next.json"
MAX_LB = 300  # portal rejects Slow lookbacks above 300


def lookback(expr):
    code = "\n".join(l.split("#", 1)[0] for l in expr.splitlines())
    w = [int(x) for x in re.findall(r",\s*(\d+)\s*\)", code)]
    return max(60, 2 * max(w, default=10) + 20)


def main(specs):
    ledger_tags, _ = known_items(None)
    drafted = set()
    for f in (ROOT / "alphas" / "drafts").glob("*.json"):
        drafted |= {it["tag"] for it in json.loads(f.read_text(encoding="utf-8"))}
    ledger_only = ledger_tags - drafted  # tags already run (ledger), not just drafted
    queue = []
    for spec in specs:
        mode, path = spec.split(":", 1)
        for it in json.loads((ROOT / path).read_text(encoding="utf-8")):
            if check(it["expr"])[0] or it["tag"] in ledger_only:
                continue
            job = {"tag": it["tag"], "base": it.get("family") or it.get("base"), "expr": it["expr"]}
            if mode.upper() == "SLOW":
                job.update(state="squeued", lb=min(MAX_LB, int(it.get("lb") or lookback(it["expr"]))))
            queue.append(job)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(queue, indent=1), encoding="utf-8")
    print(f"{len(queue)} jobs -> {OUT.relative_to(ROOT)}")
    for j in queue:
        print(f"  {j.get('state', 'queued'):8} lb={j.get('lb', '-'):>4} {j['tag']}")


if __name__ == "__main__":
    main(sys.argv[1:])
