"""Diversity guard: what our submissions are built from, and which queued jobs would only add more of the same.

Usage: python tools/diversity.py            # report + write the skip list into alphas/queue/ops.json
       python tools/diversity.py --dry      # report only
Legs are detected from each alpha's code (data + pattern fingerprints). A leg used in >= SAT submissions is
saturated. A queued job is skipped if (a) a saturated leg carries most of its risk (weight >= 1 on a slow leg, or
it is the base), or (b) its leg set overlaps a submitted alpha's leg set with Jaccard >= .6.
Rule from Abhinav (Oct 7): diversity first; do not keep submitting variations of what we already have.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAT = 3
LEGS = [  # (leg, regex on code without comments)
    ("ACC", r"net_income\)? - ts_fill\(cash_from_operations|net_income.*cash_from_operations"),
    ("ISS", r"shsout/ts_delay\(shsout"),
    ("RND", r"research_and_development_expense"),
    ("GP", r"gross_profit"),
    ("FMOM", r"return_on_assets|sales_to_total_assets_ratio"),
    ("BS", r"current_liabilities|accumulated_depreciation|goodwill|accounts_receivable_excluding_notes|other_current_assets|current_assets_report"),
    ("SBC", r"stock_based_compensation"),
    ("FCF", r"free_cash_flow"),
    ("AG", r"ta/ts_delay\(ta|total_assets\)/ts_delay"),
    ("VWGAP", r"vwap_last_hour\)/vwap_last_hour|close - vwap_last_hour"),
    ("LATEHR", r"return_last_hour|close_price_last_hour"),
    ("A54", r"\(open/close\)\*\*5"),
    ("A44", r"ts_corr_binary\(high, cs_rank\(volume\)"),
    ("A50", r"cs_rank\(volume\), cs_rank\(vwap_last_hour\)"),
    ("A53", r"delta\(pos, 10\)"),
    ("A02", r"delta\(at_signlog\(volume\), 2\)"),
    ("A15", r"cs_rank\(high\), cs_rank\(volume\), 3"),
    ("A26", r"ts_rank\(volume, 5\), ts_rank\(high, 5\)"),
]
# Submissions whose code is not in the repo (queued directly by the old cloud chat): legs from the records.
KNOWN = {"U_VWAPT_FMOM_w1": {"VWGAP", "FMOM"}, "Y_PLsz_ACC_w07": {"VWGAP", "LATEHR", "ACC"}}
SLOW = {"ACC", "ISS", "RND", "GP", "FMOM", "BS", "SBC", "FCF", "AG"}


def code_of(expr):
    return "\n".join(l.split("#", 1)[0] for l in expr.splitlines())


def legs(expr):
    c = code_of(expr)
    return {name for name, rx in LEGS if re.search(rx, c)}


def heavy_slow(expr):
    """Slow legs with weight >= 1 in the final blend (base legs always count)."""
    c = code_of(expr)
    last = [l for l in c.splitlines() if l.strip().startswith("alpha")]
    m = re.search(r"\+\s*([0-9.]+)\*", last[-1]) if last else None
    w = float(m.group(1)) if m else 1.0
    return w >= 1.0


def main(dry):
    exprs = {}
    for f in (ROOT / "alphas" / "drafts").glob("*.json"):
        for it in json.loads(f.read_text(encoding="utf-8")):
            exprs.setdefault(it["tag"], it["expr"])
    reg = list(csv.DictReader((ROOT / "alphas" / "registry.csv").open(encoding="utf-8")))
    subs = [r["tag"] for r in reg if r["status"] == "SUBMITTED"]
    sub_legs = {t: (KNOWN.get(t) or legs(exprs.get(t, ""))) for t in subs}
    use = {}
    for t, L in sub_legs.items():
        for l in L:
            use[l] = use.get(l, 0) + 1
    sat = {l for l, n in use.items() if n >= SAT}
    print(f"Submissions: {len(subs)}")
    for t in subs:
        print(f"  {t:18} {'+'.join(sorted(sub_legs[t])) or '?'}")
    print("Leg usage: " + ", ".join(f"{l} {n}" for l, n in sorted(use.items(), key=lambda x: -x[1])))
    print(f"Saturated (>= {SAT} submissions): {', '.join(sorted(sat)) or 'none'}")
    ops_p = ROOT / "alphas" / "queue" / "ops.json"
    ops = json.loads(ops_p.read_text())
    queued = [r["tag"] for r in reg if r["status"] == "QUEUED"]
    skip, keep = [], []
    for t in queued:
        L = legs(exprs.get(t, ""))
        if not L:
            keep.append(t)
            continue
        why = ""
        heavy = (L & sat) & (L - SLOW | (SLOW if heavy_slow(exprs[t]) else set()))
        if heavy:
            why = "saturated leg " + "+".join(sorted(heavy))
        for s, S in sub_legs.items():
            if S and len(L & S) / len(L | S) >= .6:
                why = why or f"same legs as {s}"
        (skip if why else keep).append(t)
        if why:
            print(f"  skip {t:22} {'+'.join(sorted(L)):24} {why}")
    print(f"Queued {len(queued)}: keep {len(keep)}, skip {len(skip)}")
    if not dry:
        ops["skip"] = sorted(set(ops.get("skip", [])) | set(skip))
        ops["front"] = [t for t in ops.get("front", []) if t not in skip]
        ops["diversity"] = {"saturated_legs": sorted(sat), "rule": "skip queued jobs whose risk is a saturated leg or whose legs match a submission (Jaccard >= .6)"}
        ops_p.write_text(json.dumps(ops, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main("--dry" in sys.argv)
