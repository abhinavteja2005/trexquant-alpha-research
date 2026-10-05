"""Systematic variants of near-miss alphas (Fast IR .06-.078, or pool corr .5-.6).

Usage:
  python tools/mutate.py --auto [--max 8]          # near-misses from the ledger that have an expr in drafts
  python tools/mutate.py --tag P_A101 [--tag ...]  # specific parents
Writes alphas/drafts/mut-<YYYYMMDD-HHMM>.json; then run check_alpha on it.

Each variant appends 1-2 commented lines (or edits one window/variable), keeping the parent's
Thesis/Source lines and adding a '# Variant:' line, so documentation stays intact.
"""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from check_alpha import ALLOWED_WINDOWS, check

ROOT = Path(__file__).resolve().parent.parent
WINDOWS = sorted(ALLOWED_WINDOWS)
# (suffix, why, lines appended after the parent's final alpha line)
WRAPS = [
    ("sub", "neutralize within sub-industry (finer than the simulator's industry neutralization)",
     ["alpha = cs_indneut(alpha, subindustry)  # demean within sub-industry"]),
    ("s3", "3-day smoothing lowers turnover and pool correlation with fast reversal books",
     ["alpha = ts_mean(alpha, 3)  # 3-day average of the signal"]),
    ("vc", "condition on abnormal volume: the effect should be stronger on heavy-volume days",
     ["alpha = alpha*cs_rank(volume/ts_mean(volume, 20))  # scale up names trading above their 20-day volume"]),
    ("lv", "tilt to calm stocks, where reversal is less likely to be news-driven",
     ["alpha = alpha*cs_rank(-ts_std(ret1, 20))  # scale up low-volatility names"]),
    ("tl", "keep only the tails, where the signal is strongest",
     ["alpha = cs_remove_middle(alpha, 0.5)  # drop the middle 50% of names"]),
]
SWAPS = [("volume", "number_of_trades_last_hour", "trd", "trade count instead of share volume"),
         ("close", "vwap_last_hour", "vw", "last-hour VWAP instead of the close print")]


def variants(parent):
    tag, expr = parent["tag"], parent["expr"]
    out = []

    def add(suffix, why, new_expr):
        out.append({**{k: v for k, v in parent.items() if k not in {"tag", "expr"}},
                    "tag": f"{tag}_{suffix}", "parent": tag,
                    "expr": f"# Variant: {why} (parent {tag})\n{new_expr}"})

    for suffix, why, lines in WRAPS:
        add(suffix, why, expr + "\n" + "\n".join(lines))
    # Window grid: move each distinct window one step down and one step up.
    for w in sorted({int(x) for x in re.findall(r",\s*(\d+)\s*\)", expr)} & ALLOWED_WINDOWS):
        i = WINDOWS.index(w)
        for nw in (WINDOWS[i - 1] if i else None, WINDOWS[i + 1] if i + 1 < len(WINDOWS) else None):
            if nw:
                new = re.sub(rf"(,\s*){w}(\s*\))", rf"\g<1>{nw}\g<2>", expr)
                add(f"w{nw}", f"window {w} -> {nw}", new)
    for old, new_var, suffix, why in SWAPS:
        if re.search(rf"\b{old}\b", expr.split("\n", 2)[-1]):
            body = "\n".join(l if l.lstrip().startswith("#") else re.sub(rf"\b{old}\b", new_var, l)
                             for l in expr.splitlines())
            add(suffix, why, body)
    if parent.get("f_ir") is not None and parent["f_ir"] <= -0.06:
        add("neg", "sign flip of a strong negative", expr + "\nalpha = -alpha  # flip the sign")
    return out


def load_drafts():
    d = {}
    for f in sorted((ROOT / "alphas" / "drafts").glob("*.json")):
        for it in json.loads(f.read_text(encoding="utf-8")):
            d[it["tag"]] = it
    return d


def near_misses(drafts):
    out = []
    for l in (ROOT / "alphas" / "ledger.md").read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) != 13 or c[1] not in drafts:
            continue
        try:
            ir, corr = float(c[3]), float(c[6] or 1)
        except ValueError:
            continue
        if (0.06 <= ir < 0.078 and corr <= 0.6) or (ir >= 0.07 and 0.5 < corr <= 0.6) or ir <= -0.06:
            out.append({**drafts[c[1]], "f_ir": ir, "f_corr": corr})
    return sorted(out, key=lambda p: -abs(p["f_ir"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--max", type=int, default=8, help="max variants kept per parent")
    a = ap.parse_args()
    drafts = load_drafts()
    parents = near_misses(drafts) if a.auto else [drafts[t] for t in a.tag]
    kept = []
    for p in parents:
        ok = [v for v in variants(p) if not check(v["expr"])[0] and v["tag"] not in drafts]
        kept += ok[: a.max]
    if not kept:
        print("no variants (no near-miss parents with an expression in alphas/drafts)")
        return
    out = ROOT / "alphas" / "drafts" / f"mut-{datetime.now():%Y%m%d-%H%M}.json"
    out.write_text(json.dumps(kept, indent=1), encoding="utf-8")
    print(f"wrote {len(kept)} variants of {len(parents)} parents to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
