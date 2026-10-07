"""Pruned grid search over combinations of proven alpha LEGS (no LLM cost).

Usage:
  python tools/grid.py --n 30            # next 30 untried combos, best prior first -> alphas/drafts/grid-<k>.json
  python tools/grid.py --expand TAG ...  # successive-halving rung: neighbours of a promising result
  python tools/grid.py --list            # how many combos exist / survive pruning
Then: python tools/make_queue.py SLOW:alphas/drafts/grid-<k>.json

Design (see knowledge/grid-search.md):
- Search space = one fast BASE leg (price/volume pattern) x a set of slow PARTNER legs x partner weight x neutralisation.
  Partners whose returns move against short-term reversal (accruals, issuance, balance-sheet composition) lower
  turnover and pool correlation; this is the recipe behind 5 of our first 8 submissions.
- Pruning BEFORE simulating (the simulator, ~60-100 Slow runs/day, is the scarce resource):
  static rules (<= 10 variables, check_alpha), diversity rules (skip base/partner pairs we already submitted
  twice -- they now collide with our own submissions), and a prior score (base IR from the registry, partner
  diversity bonus). Only the top --n go to the queue (rung 0).
- Successive halving (Hyperband, Li et al. JMLR 2018): results with Slow IR >= .065 are promoted with --expand,
  which generates their neighbours (other weights, extra partner, size/vol neutralisation); the rest are dropped.
- Multiple testing (Deflated Sharpe, Bailey & Lopez de Prado 2014): every generated combo is counted in
  alphas/grid_state.json ("trials"), so the report can state how many combinations were tried per submission.
"""
import argparse
import csv
import json
import sys
from itertools import combinations
from pathlib import Path

from check_alpha import check

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "alphas" / "grid_state.json"

# Fast legs: code lines ending with a z-scored variable `b`. prior = best known Slow/Fast IR of the base alone.
BASES = {
    "VW": dict(prior=.083, fam="VWAPT", vars={"close", "vwap_last_hour", "number_of_trades_last_hour"}, lb=60,
               src="liquidity reversal (Campbell, Grossman & Wang, QJE 1993)", code=[
        "g = ts_mean((close - vwap_last_hour)/vwap_last_hour, 5)  # 5-day avg close-vs-VWAP gap",
        "busy = cs_rank(number_of_trades_last_hour/ts_mean(number_of_trades_last_hour, 20)) > 1.3  # unusually many last-hour trades",
        "b = cs_zscore(at_zero2nan(-cs_rank(g) * busy))  # fade the gap on busy closes"]),
    "A54": dict(prior=.112, fam="A101", vars={"low", "close", "high", "open"}, lb=60,
                src="Kakushadze, 101 Formulaic Alphas (2016), https://arxiv.org/abs/1601.00991 (Alpha #54)", code=[
        "loc = (low - close)/(low - high - 0.001*close)  # how far the close sits above the low, 0..1",
        "b = cs_zscore(-loc*(open/close)**5)  # long closes near the low after a drop"]),
    "A44": dict(prior=.067, fam="A101", vars={"high", "volume"}, lb=60,
                src="Kakushadze, 101 Formulaic Alphas (2016), https://arxiv.org/abs/1601.00991 (Alpha #44)", code=[
        "b = cs_zscore(-ts_corr_binary(high, cs_rank(volume), 5))  # short names whose highs move with volume rank"]),
    "A50": dict(prior=.072, fam="A101", vars={"volume", "vwap_last_hour"}, lb=60,
                src="Kakushadze, 101 Formulaic Alphas (2016), https://arxiv.org/abs/1601.00991 (Alpha #50)", code=[
        "c = ts_corr_binary(cs_rank(volume), cs_rank(vwap_last_hour), 5)  # 5-day corr of volume rank and VWAP rank",
        "b = cs_zscore(-ts_max(cs_rank(c), 5))  # short the most persistent co-movers"]),
    "A53": dict(prior=.068, fam="A101", vars={"close", "low", "high"}, lb=60,
                src="Kakushadze, 101 Formulaic Alphas (2016), https://arxiv.org/abs/1601.00991 (Alpha #53)", code=[
        "pos = ((close - low) - (high - close))/(close - low + 0.001*close)  # close location within the day's range",
        "b = cs_zscore(-delta(pos, 10))  # fade the 10-day change in close location"]),
    "A02": dict(prior=.071, fam="A101", vars={"volume", "close", "open"}, lb=60,
                src="Kakushadze, 101 Formulaic Alphas (2016), https://arxiv.org/abs/1601.00991 (Alpha #2)", code=[
        "dv = delta(at_signlog(volume), 2)  # 2-day change in log volume",
        "oc = (close - open)/open  # open-to-close return",
        "b = cs_zscore(-ts_corr_binary(cs_rank(dv), cs_rank(oc), 5))  # short names whose volume and return ranks co-move"]),
    "A15": dict(prior=.073, fam="A101", vars={"high", "volume"}, lb=60,
                src="Kakushadze, 101 Formulaic Alphas (2016), https://arxiv.org/abs/1601.00991 (Alpha #15)", code=[
        "c = ts_corr_binary(cs_rank(high), cs_rank(volume), 3)  # 3-day corr of high-price rank and volume rank",
        "b = cs_zscore(-ts_sum(cs_rank(c), 3))  # short names where that corr stays high"]),
    "A26": dict(prior=.073, fam="A101", vars={"volume", "high"}, lb=60,
                src="Kakushadze, 101 Formulaic Alphas (2016), https://arxiv.org/abs/1601.00991 (Alpha #26)", code=[
        "c = ts_corr_binary(ts_rank(volume, 5), ts_rank(high, 5), 5)  # corr of 5-day volume and high ranks",
        "b = cs_zscore(-ts_max(c, 3))  # short names with the highest recent co-peaking"]),
}
# Slow legs: code lines ending with a z-scored variable p_<key>.
PARTNERS = {
    "ACC": dict(vars={"net_income", "cash_from_operations", "total_assets"}, lb=140, src="accruals (Sloan, The Accounting Review 1996, https://www.jstor.org/stable/248290)", code=[
        "p_acc = cs_zscore(-cs_rank((ts_fill(net_income) - ts_fill(cash_from_operations))/ts_fill(total_assets)))  # low accruals: earnings backed by cash"]),
    "ISS": dict(vars={"shsout"}, lb=300, src="net share issuance (Pontiff & Woodgate, JF 2008)", code=[
        "p_iss = cs_zscore(-cs_rank(shsout/ts_delay(shsout, 250) - 1))  # net issuance: short dilution, long buybacks"]),
    "BS": dict(vars={"total_assets", "current_liabilities", "accounts_receivable_excluding_notes", "goodwill", "accumulated_depreciation"}, lb=120,
               src="balance-sheet composition (Green, Hand & Zhang, RFS 2017, https://doi.org/10.1093/rfs/hhx019); our sweep batch 1",
               code=["ta = ts_fill(total_assets)  # total assets",
                     "p_bs = cs_zscore(cs_rank(ts_fill(current_liabilities)/ta) + cs_rank(ts_fill(accounts_receivable_excluding_notes)/ta) - cs_rank(ts_fill(goodwill)/ta) + cs_rank(ts_fill(accumulated_depreciation)/ta))  # balance-sheet composite (our SWC_BS legs)"]),
    "CL": dict(vars={"total_assets", "current_liabilities"}, lb=120, src="current liabilities / assets (our strongest sweep leg, OOS1 .086)", code=[
        "p_cl = cs_zscore(cs_rank(ts_fill(current_liabilities)/ts_fill(total_assets)))  # short-term operating liabilities per dollar of assets"]),
}
PARTNER_SETS = [("ACC",), ("BS",), ("ISS",), ("CL",), ("ACC", "BS"), ("BS", "ISS"), ("ACC", "ISS"), ("CL", "ISS")]
WEIGHTS = [1.0, 1.5, 2.0]
NEUT = ["none", "size"]
SATURATED = {("VW", "ACC"), ("VW", "FMOM"), ("A54", "ACC")}  # already submitted: they now hit our own submissions


def tag(base, parts, w, neut):
    return f"G_{base}_{'_'.join(parts)}_w{str(w).replace('.', '')}" + ("_sz" if neut == "size" else "")


def build(base, parts, w, neut, note=""):
    B = BASES[base]
    vs = set(B["vars"]) | {v for p in parts for v in PARTNERS[p]["vars"]} | ({"mktcap"} if neut == "size" else set())
    if len(vs) > 10:
        return None
    lines = [f"# Thesis: a short-horizon price/volume pattern ({base}) blended with slow characteristics ({', '.join(parts)}) whose "
             "returns move against short-term reversal, so the blend keeps the pattern's IR with lower turnover and lower overlap "
             "with crowded pool alphas (the partner recipe behind our submissions).",
             f"# Source: {B['src']}; " + "; ".join(PARTNERS[p]["src"] for p in parts),
             f"# Grid: base {base}, partners {'+'.join(parts)}, partner weight {w}, neutralisation {neut}. {note}".rstrip()]
    lines += B["code"]
    seen = set()
    for p in parts:
        for l in PARTNERS[p]["code"]:
            if l.split("=")[0].strip() in seen:
                continue
            seen.add(l.split("=")[0].strip())
            lines.append(l)
    psum = " + ".join(f"at_nan2zero(p_{p.lower()})" for p in parts)
    if neut == "size":
        lines.append("sz = cs_rank(at_signlog(mktcap))  # size rank (log market cap)")
        lines.append(f"alpha = cs_factorneut(at_zero2nan(at_nan2zero(b) + {w}*({psum})), [sz])  # base + {w}x partners, size neutral")
    else:
        lines.append(f"alpha = at_zero2nan(at_nan2zero(b) + {w}*({psum}))  # base + {w}x partners")
    expr = "\n".join(lines)
    if check(expr)[0]:
        return None
    lb = max([B["lb"]] + [PARTNERS[p]["lb"] for p in parts])
    return {"tag": tag(base, parts, w, neut), "base": base, "family": "G_" + B["fam"], "expr": expr, "lb": min(lb, 300),
            "grid": {"base": base, "parts": list(parts), "w": w, "neut": neut}}


def tried():
    out = set()
    reg = ROOT / "alphas" / "registry.csv"
    if reg.exists():
        out |= {r["tag"] for r in csv.DictReader(reg.open(encoding="utf-8"))}
    for f in (ROOT / "alphas" / "drafts").glob("*.json"):
        out |= {it["tag"] for it in json.loads(f.read_text(encoding="utf-8"))}
    return out


def prior(c):
    g = c["grid"]
    s = BASES[g["base"]]["prior"]
    s += .01 * len(g["parts"]) + (.005 if "BS" in g["parts"] or "CL" in g["parts"] else 0)  # diversity bonus: new partner family
    s -= .004 * abs(g["w"] - 1.5)
    s -= .03 * c.get("sat", 0)  # saturated legs run later
    return s


def save(items, state, label):
    state["batches"] = state.get("batches", 0) + 1
    state["trials"] = state.get("trials", 0) + len(items)
    out = ROOT / "alphas" / "drafts" / f"grid-{state['batches']}.json"
    out.write_text(json.dumps(items, indent=1), encoding="utf-8")
    STATE.write_text(json.dumps(state, indent=1), encoding="utf-8")
    print(f"{len(items)} {label} -> {out.relative_to(ROOT)} (total trials {state['trials']})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--expand", nargs="*")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    state = json.loads(STATE.read_text()) if STATE.exists() else {"batches": 0, "trials": 0}
    done = tried()
    ops = ROOT / "alphas" / "queue" / "ops.json"
    sat = set(json.loads(ops.read_text()).get("diversity", {}).get("saturated_legs", [])) if ops.exists() else set()
    leg = {"ACC": "ACC", "ISS": "ISS", "BS": "BS", "CL": "BS", "VW": "VWGAP", **{b: b for b in BASES if b.startswith("A")}}  # grid key -> diversity leg (tools/diversity.py)
    space = [build(b, p, w, n) for b in BASES for p in PARTNER_SETS for w in WEIGHTS for n in NEUT
             if not any((b, x) in SATURATED for x in p)]
    for c in space:  # diversity orders, never excludes (Abhinav, Oct 7 evening)
        if c:
            g = c["grid"]
            c["sat"] = (leg.get(g["base"]) in sat) + sum(leg.get(x) in sat for x in g["parts"])
    ok = [c for c in space if c and c["tag"] not in done]
    if a.list:
        print(f"space {len(BASES) * len(PARTNER_SETS) * len(WEIGHTS) * len(NEUT)}; after saturation/var-cap/check "
              f"{len([c for c in space if c])}; untried {len(ok)}")
        return 0
    if a.expand:
        items = []
        for t in a.expand:
            src = next((c for c in space if c and c["tag"] == t), None)
            if not src:
                print(f"expand skipped: {t} is not a grid tag", file=sys.stderr)
                continue
            g = src["grid"]
            for c in ok:
                h = c["grid"]
                near = h["base"] == g["base"] and (
                    (h["parts"] == g["parts"] and (h["w"] != g["w"] or h["neut"] != g["neut"]))
                    or (set(g["parts"]) < set(h["parts"]) and len(h["parts"]) == len(g["parts"]) + 1))
                if near and c not in items:
                    c = dict(c)
                    c["expr"] = c["expr"].replace("# Grid:", f"# Grid (rung up from {t}):", 1)
                    items.append(c)
        if items:
            save(items[:4 * len(a.expand)], state, "neighbours")
        return 0
    per_base, items = {}, []
    for c in sorted(ok, key=prior, reverse=True):  # breadth: at most 4 per base per batch
        b = c["grid"]["base"]
        if per_base.get(b, 0) >= 4:
            continue
        per_base[b] = per_base.get(b, 0) + 1
        items.append(c)
        if len(items) >= a.n:
            break
    if items:
        save(items, state, "grid combos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
