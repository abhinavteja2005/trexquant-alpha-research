"""Thompson-sampling slot allocator across alpha families (B2).

Usage: python tools/bandit.py [--slots 20] [--seed N]   -> writes reports/next_slots.md
Family key: ledger Family text before the first '+', space or '(', uppercased, trailing digits
stripped. Trial = ledger row with a Slow IR. Hit = Slow IR >= .065 AND (S E yes OR corr <= .6),
or Submitted YES. Slots ~ share of Beta(hits+1, misses+1) wins; >= 30% reserved for families
with < 3 Slow trials (drafts-only families included).
"""
import argparse
import json
import random
import re
from collections import Counter, defaultdict

from check_alpha import ROOT


def fam_key(text, tag=""):
    k = re.split(r"[+\s(]", text.strip(), maxsplit=1)[0].upper().rstrip("0123456789")
    return k or tag.split("_")[0].upper().rstrip("0123456789")


def num(s):
    m = re.search(r"\d*\.?\d+", s)
    return float(m.group()) if m else None


def load():
    trials, hits, tags = Counter(), Counter(), set()
    for line in (ROOT / "alphas" / "ledger.md").read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.split("|")]
        if len(c) < 14 or not c[2] or c[2] == "Tag" or c[2].startswith("-"):
            continue
        tags.add(c[2])
        sir = num(c[9])
        if sir is None:
            continue
        k = fam_key(c[3], c[2])
        corr = num(c[10])
        trials[k] += 1
        if c[13].lower() == "yes" or (sir >= 0.065 and (c[11].lower() == "yes" or (corr is not None and corr <= 0.6))):
            hits[k] += 1
    drafts = set()
    for f in (ROOT / "alphas" / "drafts").glob("*.json"):
        for it in json.loads(f.read_text(encoding="utf-8")):
            drafts.add(fam_key(it.get("family") or it.get("base") or "", it["tag"]))
    return trials, hits, drafts


def allocate(weights, n):
    """Largest-remainder rounding of weights (sum 1) to n integers."""
    raw = {k: w * n for k, w in weights.items()}
    out = {k: int(v) for k, v in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - out[k], reverse=True)[: n - sum(out.values())]:
        out[k] += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slots", type=int, default=20)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    rnd = random.Random(a.seed)
    trials, hits, drafts = load()
    fams = sorted(set(trials) | drafts)
    # exploit pool: Thompson win counts; explore pool: families with < 3 Slow trials
    wins = Counter()
    exploit = [f for f in fams if trials[f] >= 3] or fams
    for _ in range(2000):
        wins[max(exploit, key=lambda f: rnd.betavariate(hits[f] + 1, trials[f] - hits[f] + 1))] += 1
    explore = [f for f in fams if trials[f] < 3]
    n_exp = min(a.slots, max(-(-a.slots * 3 // 10), 0)) if explore else 0
    slots = Counter(allocate({f: 1 / len(explore) for f in explore}, n_exp)) if explore else Counter()
    rest = a.slots - n_exp
    for f, s in allocate({f: w / 2000 for f, w in wins.items()}, rest).items():
        slots[f] += s
    lines = [f"# Next slots ({a.slots}, seed {a.seed})", "",
             "| Family | Slow trials | Hits | Posterior mean | Slots | Note |", "|---|---|---|---|---|---|"]
    for f in sorted(fams, key=lambda f: (-slots[f], f)):
        mean = (hits[f] + 1) / (trials[f] + 2)
        note = "explore" if trials[f] < 3 else "exploit"
        lines.append(f"| {f} | {trials[f]} | {hits[f]} | {mean:.2f} | {slots[f]} | {note} |")
    text = "\n".join(lines) + "\n"
    (ROOT / "reports" / "next_slots.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
