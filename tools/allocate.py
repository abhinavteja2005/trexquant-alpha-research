"""Thompson-sampling bandit over alpha SOURCES (RD-Agent(Q) style): split the next batch of simulator slots by yield.

Usage: python tools/allocate.py [--slots 30]   -> alphas/queue/allocation.json + printed table
A pull is one Slow run from a source; reward = 1 if Slow IR >= .065 (near-miss or better), +1 more if submitted.
Each source gets Beta(1 + rewards, 1 + misses); we draw 2000 samples and give slots in proportion to how often each
source wins, keeping >= 2 slots for every active source (exploration).
"""
import argparse
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = [("SWC", "combine"), ("WSE", "combine"), ("G_A", "grid"), ("SW_", "sweep"), ("N_", "llm"), ("MM", "llm"),
           ("MO", "llm"), ("MR", "llm"), ("LIQ", "llm"), ("MOMX", "llm"), ("HR_", "llm"), ("FUND", "llm"), ("PV_", "llm"),
           ("A101", "translate"), ("R_", "repair"), ("Y_", "repair"), ("X_", "repair"), ("U_", "repair"), ("T_", "repair")]
ACTIVE = ["repair", "combine", "grid", "llm", "sweep", "translate"]


def source(tag):
    for p, s in SOURCES:
        if tag.startswith(p):
            return s
    return "early"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slots", type=int, default=30)
    a = ap.parse_args()
    reg = list(csv.DictReader((ROOT / "alphas" / "registry.csv").open(encoding="utf-8")))
    stat = {s: [0, 0] for s in ACTIVE}
    for r in reg:
        s = source(r["tag"])
        if s not in stat or not r["slow_ir"]:
            continue
        win = (float(r["slow_ir"]) >= .065) + (r["status"] == "SUBMITTED")
        stat[s][0] += win
        stat[s][1] += 1
    random.seed(7)
    wins = {s: 0 for s in ACTIVE}
    for _ in range(2000):
        draw = {s: random.betavariate(1 + w, 1 + max(0, n - w)) for s, (w, n) in stat.items()}
        wins[max(draw, key=draw.get)] += 1
    free = a.slots - 2 * len(ACTIVE)
    alloc = {s: 2 + round(free * wins[s] / 2000) for s in ACTIVE}
    out = {"slots": a.slots, "allocation": alloc, "stats": {s: {"rewards": w, "runs": n} for s, (w, n) in stat.items()}}
    (ROOT / "alphas" / "queue" / "allocation.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for s in ACTIVE:
        w, n = stat[s]
        print(f"{s:10} runs {n:4} rewards {w:3}  ->  {alloc[s]} slots")


if __name__ == "__main__":
    main()
