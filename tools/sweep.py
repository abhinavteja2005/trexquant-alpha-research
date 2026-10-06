"""Field sweep: apply a few dimensionless templates to data fields we have not used yet (no LLM cost).

Usage:
  python tools/sweep.py --n 40            # next 40 untried (field, template) pairs -> alphas/drafts/sweep-<k>.json
  python tools/sweep.py --flip TAG ...    # sign-flipped copies of finished sweep alphas with clearly negative IR
  python tools/sweep.py --list            # classification of every field (for review)
Then: python tools/make_queue.py SLOW:alphas/drafts/sweep-<k>.json

Why: correlation is measured on daily PnL, so alphas built on different data are often uncorrelated with the
pool; most hand-built ideas here reuse the same ~45 fields. Each template is a standard characteristic transform
(level, 6-month change, deviation from own history) as in the anomaly-replication literature; the portal
industry-neutralises and de-means, so a cross-sectional rank is a long/short book. Signs are unknown a priori:
every pair is first run with sign +1, and results with IR <= -0.04 are re-queued flipped (--flip).
State (pairs already generated) lives in alphas/sweep_state.json.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from check_alpha import check

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "alphas" / "sweep_state.json"
VARS = json.loads((ROOT / "knowledge" / "variables.json").read_text())

SRC_FUND = ("# Source: Green, Hand & Zhang, \"The Characteristics that Provide Independent Information about Average U.S. "
            "Monthly Stock Returns\" (Review of Financial Studies 2017), https://doi.org/10.1093/rfs/hhx019; Hou, Xue & "
            "Zhang, \"Replicating Anomalies\" (Review of Financial Studies 2020), https://doi.org/10.1093/rfs/hhy131")
SRC_INTRA = ("# Source: Heston, Korajczyk & Sadka, \"Intraday Patterns in the Cross-section of Stock Returns\" (Journal of "
             "Finance 2010), https://doi.org/10.1111/j.1540-6261.2010.01573.x")

SKIP = {"industry", "sector", "subindustry", "trading_days_until_next_earnings_announcement", "cashdvd"}
SKIP_RE = re.compile(r"^(days_|day_of|month_of|quarter_of|cpi_|gdp_|real_gdp|unemployment_|wti_|ret\d|close_spx|close_vix)"
                     r"|deposits|non_interest|net_interest_income|collaterals")  # calendar/macro/returns; bank-only fields
INTRA_RE = re.compile(r"_(first|last)_hour$")
RATIO_RE = re.compile(r"ratio|pct|margin|growth|yield|return_on|_roe|^roe|roa_|normalized_roe|_to_|per_employee|turnover")
PERSHARE_RE = re.compile(r"per_(diluted_)?share|eps")
SHARES_RE = re.compile(r"shares|shsfloat")


def classify(v):
    """RATIO (already dimensionless), PERSHARE (/close), SHARES (count), DOLLAR (/total_assets), INTRA, or SKIP."""
    if v in SKIP or SKIP_RE.search(v):
        return "SKIP"
    if INTRA_RE.search(v):
        if v.startswith(("skew_", "std_")) or "price" in v:
            return "INTRA"
        return "SKIP"  # raw first/last-hour returns, vwap, volumes: already heavily used / crowded reversal
    if v in {"open", "high", "low", "close", "volume", "vwap", "mktcap", "shsout", "ret1", "ret5", "ret20"}:
        return "SKIP"
    if SHARES_RE.search(v):
        return "SHARES"
    if RATIO_RE.search(v) or v.startswith(("price_to", "roa_")):
        return "RATIO"
    if PERSHARE_RE.search(v):
        return "PERSHARE"
    return "DOLLAR"


def used_fields():
    out = set()
    for f in (ROOT / "alphas" / "drafts").glob("*.json"):
        if f.name.startswith("sweep-"):
            continue
        for it in json.loads(f.read_text(encoding="utf-8")):
            code = "\n".join(l.split("#", 1)[0] for l in it["expr"].splitlines())
            out |= set(re.findall(r"[A-Za-z_]\w*", code))
    return out


def norm_lines(v, cls):
    """Code lines defining n = a dimensionless version of field v, plus the variables it uses."""
    if cls == "RATIO":
        return [f"n = ts_fill({v})  # {v}: already a dimensionless ratio, carried forward between reports"]
    if cls == "PERSHARE":
        return [f"n = ts_fill({v})/close  # {v} per share divided by price: a yield (dimensionless)"]
    if cls == "DOLLAR":
        return [f"n = ts_fill({v})/ts_fill(total_assets)  # {v} scaled by total assets (dimensionless)"]
    if cls == "SHARES":
        return [f"n = ts_fill({v})/ts_delay(ts_fill({v}), 120) - 1  # 6-month growth in {v} (dimensionless)"]
    if v.startswith("skew_") or "return" in v:
        return [f"n = {v}  # {v}: intraday skewness / return dispersion, already dimensionless"]
    if v.startswith("std_volume"):
        base = "volume_first_hour" if "first" in v else "volume_last_hour"
        return [f"n = {v}/ts_mean({base}, 20)  # intraday volume dispersion relative to the stock's usual hourly volume"]
    return [f"n = {v}/close  # {v} relative to today's close (dimensionless)"]


TEMPLATES = {
    # key: (classes, code lines, lb, thesis fragment)
    "L": ({"RATIO", "PERSHARE", "DOLLAR"}, ["alpha = cs_rank(n)  # long high, short low (portal industry-neutralises)"], 100,
          "the cross-sectional LEVEL of {v} is a firm characteristic that investors price slowly"),
    "D": ({"RATIO", "PERSHARE", "DOLLAR"}, ["alpha = cs_rank(n - ts_delay(n, 120))  # 6-month change: improving minus deteriorating firms"], 220,
          "the 6-month CHANGE in {v} carries news that is under-reacted to (fundamental momentum)"),
    "Z": ({"RATIO", "PERSHARE", "DOLLAR", "SHARES"}, ["alpha = cs_rank(ts_zscore(n, 120))  # today's value vs the firm's own 6-month history"], 220,
          "{v} far from its own recent history signals a shift the market has not fully priced"),
    "IF": ({"INTRA"}, ["alpha = -cs_zscore(ts_mean(n, 5))  # fade a week of unusual intraday readings"], 60,
           "an unusual week of {v} reflects temporary liquidity pressure that reverts"),
    "IZ": ({"INTRA"}, ["alpha = cs_rank(ts_zscore(n, 20))  # today's reading vs the stock's own month"], 60,
           "{v} far from its own month signals informed trading that continues"),
}


def abbr(v):
    parts = [p for p in v.split("_") if p]
    s = "".join(p[0] for p in parts)[:6].upper()
    return s + str(sum(map(ord, v)) % 97)


def make(v, cls, t, sign=1):
    tmpl_cls, lines, lb, frag = TEMPLATES[t]
    code = norm_lines(v, cls) + lines
    if sign < 0:
        code[-1] = code[-1].replace("alpha = ", "alpha = -(", 1).replace("  #", ")  # SIGN FLIPPED after a negative first run;", 1)
    head = [f"# Thesis: {frag.format(v=v)}. Field-sweep alpha (template {t}, class {cls}); sign {'+' if sign > 0 else '-'}.",
            SRC_INTRA if cls == "INTRA" else SRC_FUND]
    tag = f"SW_{t}_{abbr(v)}" + ("_N" if sign < 0 else "")
    return {"tag": tag, "base": f"sweep {t}", "family": f"SW_{cls}", "field": v, "template": t, "sign": sign,
            "expr": "\n".join(head + code), "lb": lb}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--flip", nargs="*")
    a = ap.parse_args()
    state = json.loads(STATE.read_text()) if STATE.exists() else {"done": [], "batches": 0}
    done = set(state["done"])
    if a.list:
        for v in VARS:
            print(f"{classify(v):8} {v}")
        return 0
    if a.flip:
        allsw = {}
        for f in (ROOT / "alphas" / "drafts").glob("sweep-*.json"):
            allsw.update({it["tag"]: it for it in json.loads(f.read_text())})
        items = [make(allsw[t]["field"], allsw[t]["family"][3:], allsw[t]["template"], -1) for t in a.flip if t in allsw]
    else:
        used = used_fields()
        cand = []
        for t in ["L", "D", "IF", "Z", "IZ"]:  # breadth first: every field once before second templates
            for v in VARS:
                cls = classify(v)
                if cls == "SKIP" or v in used or cls not in TEMPLATES[t][0] or f"{v}|{t}" in done:
                    continue
                cand.append((v, cls, t))
        items = []
        for v, cls, t in cand:
            it = make(v, cls, t)
            errs = check(it["expr"])[0]
            if errs:
                print(f"skip {it['tag']} {v}: {errs[0]}", file=sys.stderr)
                continue
            items.append(it)
            done.add(f"{v}|{t}")
            if len(items) >= a.n:
                break
    if not items:
        print("nothing to generate")
        return 0
    state["batches"] += 1
    out = ROOT / "alphas" / "drafts" / f"sweep-{state['batches']}.json"
    out.write_text(json.dumps(items, indent=1), encoding="utf-8")
    state["done"] = sorted(done)
    STATE.write_text(json.dumps(state, indent=1), encoding="utf-8")
    print(f"{len(items)} sweep alphas -> {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
