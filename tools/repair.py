"""Turn a parent alpha draft into a documented repair variant (knowledge/repair-playbook.md).

Usage:
  python tools/repair.py <parent_tag> <technique> [<technique2>] [--out alphas/drafts/repairs.json] [--print] [--tag TAG]
Techniques: band ewm weekly w10 szvo slow2x slow3x multihorizon winsor gate (at most 2, applied in order).
The parent keeps its leading comment lines (Thesis/Source/...), gets a '# Repair:' line, and its final
'alpha = X' line becomes 's = X' (except w10/slow2x/slow3x, which edit in place). The result is appended
to --out (deduped by tag) with lb/wlb set from the longest window + delay, and checked with check_alpha.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from check_alpha import IDENT, call_args, check, expr_hash, known_items, strip_comment
from mutate import load_drafts

ROOT = Path(__file__).resolve().parent.parent
PB = "knowledge/repair-playbook.md"

# technique -> (description, source)
INFO = {
    "band": ("banding / buy-hold spread: enter at the extremes, exit late", "Novy-Marx & Velikov, RFS 2016"),
    "ewm": ("partial trading toward the target via exponential smoothing", "Garleanu & Pedersen, JF 2013"),
    "weekly": ("trade one day a week, hold the signal in between", "weekly rebalance, " + PB),
    "w10": ("longer 10-day windows instead of 5-day", "horizon change, " + PB),
    "szvo": ("size and volatility neutral", "Isichenko 2021; " + PB),
    "slow2x": ("2x weight on the slow terms so the fast base trades less", PB),
    "slow3x": ("3x weight on the slow terms so the fast base trades less", PB),
    "multihorizon": ("average of the 5-, 10- and 20-day versions of the signal", PB),
    "winsor": ("winsorize the signal to damp outliers", PB),
    "gate": ("trade only on volume-shock days, where the effect is stronger", PB),
}

# technique -> lines appended after 's = ...' (each ends in a comment)
TEMPLATES = {
    "band": [  # weighted book (0/1 flags flip too often: R_PRICE2_band2 TVR 1.93); flags cast to float32
        "q = cs_rank(s)  # cross-sectional rank of the signal, in [1,2]",
        "up = (q*0 + 1)*((ts_max(q, 5) > 1.8)*(q > 1.6))  # float32 1 (no extra variable) if the name reached the top tail in 5 days and is still in the upper band",
        "dn = (q*0 + 1)*((ts_min(q, 5) < 1.2)*(q < 1.4))  # float32 1 if the name reached the bottom tail in 5 days and is still in the lower band",
        "alpha = at_zero2nan((up + dn)*cs_zscore(s))  # hold the banded names at signal weight; no position elsewhere",
    ],
    "ewm": ["alpha = ts_mean_exp(s, 10, 0.7)  # exponentially smoothed signal: trade partially toward the target"],
    "weekly": [
        "s0 = at_nan2zero(s)  # signal with NaN as 0 so the stale-signal blend is defined",
        "f0 = (day_of_the_week*0 + 1)*(day_of_the_week < ts_delay(day_of_the_week, 1))  # float32 1 on the week's first trading day",
        "f1 = ts_delay(f0, 1)  # 1 if the week started yesterday",
        "f2 = ts_delay(f0, 2)  # 1 if the week started 2 days ago",
        "f3 = ts_delay(f0, 3)  # 1 if the week started 3 days ago",
        "alpha = at_zero2nan(f0*s0 + (1-f0)*(f1*ts_delay(s0, 1) + (1-f1)*(f2*ts_delay(s0, 2) + (1-f2)*(f3*ts_delay(s0, 3) + (1-f3)*ts_delay(s0, 4)))))  # use the signal from the week's first day all week",
    ],
    "szvo": [
        "sz = cs_rank(at_signlog(mktcap))  # size rank (log market cap)",
        "vo = cs_rank(ts_std(ret1, 20))  # 1-month volatility rank",
        "alpha = cs_factorneut(s, [sz, vo])  # remove size and volatility exposure",
    ],
    "winsor": ["alpha = cs_winsor(s, 0.05, False)  # clip the 5% tails of the signal"],
    "gate": ["alpha = at_zero2nan(s * (cs_rank(volume/ts_mean(volume, 20)) > 1.5))  # keep only names in a volume shock"],
}


def die(msg):
    sys.exit(f"repair.py: {msg}")


def split_expr(expr):
    lines = expr.splitlines()
    i = 0
    while i < len(lines) and (lines[i].strip().startswith("#") or not lines[i].strip()):
        i += 1
    return [l for l in lines[:i] if l.strip()], [l for l in lines[i:] if l.strip()]


def last_alpha(code):
    for i in range(len(code) - 1, -1, -1):
        if re.match(r"\s*alpha\s*=", code[i]):
            return i
    die("parent has no 'alpha =' line")


def parts(line):
    """'name = expr  # comment' -> (name, expr, comment)."""
    code, _, com = line.partition("#")
    name, _, e = code.partition("=")
    return name.strip(), e.strip(), com.strip()


def window_spots(code, w):
    """Positions of a last argument == w in calls that are rolling windows (ts_delay lags excluded)."""
    spots = []
    for m in re.finditer(rf",\s*{w}\s*\)", code):
        depth, i = 0, m.end() - 1  # walk back from the ')' to its matching '('
        while i >= 0:
            depth += code[i] == ")"
            depth -= code[i] == "("
            if depth == 0:
                break
            i -= 1
        fn = re.search(r"(\w+)\s*$", code[:i])
        if fn and fn.group(1) != "ts_delay":
            spots.append(m)
    return spots


def swap_windows(line, old, new):
    """Change rolling windows old -> new (not ts_delay lags); keep comments in step."""
    code, sep, com = line.partition("#")
    spots = window_spots(code, old)
    for m in reversed(spots):
        code = code[:m.start()] + m.group().replace(str(old), str(new)) + code[m.end():]
    return code + sep + (re.sub(rf"(?<!\d){old}-day", f"{new}-day", com) if spots else com)


def has_window(code, w):
    return any(window_spots(strip_comment(l), w) for l in code)


def top_split_plus(e):
    out, depth, cur = [], 0, ""
    for ch in e:
        depth += ch == "("
        depth -= ch == ")"
        if ch == "+" and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    return out


def is_slow(term, code):
    """A term is slow if it reaches filing data (ts_fill) or a window/delay >= 60 days
    through the local definitions; the fast base uses only short windows."""
    def slowtxt(t):
        return "ts_fill" in t or any(int(x) >= 60 for x in re.findall(r",\s*(\d+)\s*\)", t))
    defs = {parts(l)[0]: strip_comment(l) for l in code if "=" in strip_comment(l)}
    seen, todo = set(), set(re.findall(r"[A-Za-z_]\w*", term))
    while todo:
        n = todo.pop()
        if n in seen or n not in defs:
            continue
        seen.add(n)
        if slowtxt(defs[n]):
            return True
        todo |= set(re.findall(r"[A-Za-z_]\w*", defs[n].split("=", 1)[1]))
    return slowtxt(term)


def slow(code, k):
    """Weight every slow (filing-data) term k x and keep the single fast base at 1x.
    Accepts 'a(r) + a(k1) + ...' and the playbook form 'a(r) + 3*(a(k1) + ...)'."""
    i = last_alpha(code)
    _, e, com = parts(code[i])
    m = re.fullmatch(r"at_zero2nan\((.*)\)", e)
    inner = m.group(1) if m else e
    terms = top_split_plus(inner)
    fast = [t for t in terms if not is_slow(t, code)]
    if len(terms) < 2:
        die(f"slow{k}x needs a final line that is a sum of terms; the parent's has one term")
    if len(fast) != 1:
        die(f"slow{k}x needs exactly one fast (non-ts_fill, short-window) term; parent has {len(fast)} of {len(terms)}")
    if any(re.search(r"\*\s*\d+(\.\d+)?\s*$", t) for t in terms):
        die(f"slow{k}x: write weights in front (k*term), not behind")
    out = []
    for t in terms:
        g = re.fullmatch(r"\d+(?:\.\d+)?\s*\*\s*(.+)", t)  # drop any existing leading weight
        out.append(t if t in fast else f"{k}*{g.group(1) if g else t}")
    new = " + ".join(out)
    line = (f"alpha = at_zero2nan({new})" if m else f"alpha = {new}") + \
           f"  # fast base at 1x, the {len(terms) - 1} slow term(s) at {k}x"
    return code[:i] + [line] + code[i + 1:]


def multihorizon(code):
    i = last_alpha(code)
    body = [l for l in code[:i]]
    _, e, com = parts(code[i])
    base = [f"s_5 = {e}  # {com or 'parent signal'}"]
    base_code = body + base
    names = sorted({parts(l)[0] for l in body if "=" in strip_comment(l)} | {"s"}, key=len, reverse=True)
    pat = re.compile(r"(?<![\w.])(" + "|".join(map(re.escape, names)) + r")(?![\w(])")
    extra = []
    for w in (10, 20):
        for l in body + [f"s = {e}  # {com or 'parent signal'}"]:
            l = swap_windows(l, 5, w)  # rolling windows only, comments kept in step
            c, sep, cm = l.partition("#")
            c = pat.sub(lambda m: f"{m.group(1)}_{w}", c)  # one pass: no chained renames
            extra.append(c + sep + cm)
    # parent body (5-day) stays as written; s_5 is the 5-day signal
    final = "alpha = (cs_rank(s_5) + cs_rank(s_10) + cs_rank(s_20))/3  # average rank across 5/10/20-day horizons"
    return base_code + extra + [final]


def apply(tech, code):
    if tech in ("w10", "multihorizon") and not has_window(code, 5):
        die(f"{tech} needs 5-day windows in the parent; none found")
    if tech == "w10":
        return [swap_windows(l, 5, 10) for l in code]
    if tech in ("slow2x", "slow3x"):
        return slow(code, int(tech[4]))
    if tech == "multihorizon":
        return multihorizon(code)
    i = last_alpha(code)
    _, e, com = parts(code[i])
    out = code[:i] + [f"s = {e}  # {com or 'parent signal'}"]
    if com and com != "parent signal":
        out[-1] = f"s = {e}  # {com}"
    return out + TEMPLATES[tech]


WINCALL = re.compile(r"\b(ts_\w+|decay_linear|delta)\s*\(")
LB_MAX = 300  # portal maximum ("Lookback cannot exceed 300", lessons Oct 6 11:45)


def expr_need(text, needs):
    """Days of history `text` needs: nested windows and lags add up, locals carry their own need."""
    best = max([needs[n] for n in IDENT.findall(text) if n in needs] + [0])
    for m in WINCALL.finditer(text):
        args = call_args(text, m.end() - 1)
        ints = [int(a) for a in args[1:] if re.fullmatch(r"\d+", a)]
        inner = max([expr_need(a, needs) for a in args if not re.fullmatch(r"[\d.]+|True|False", a)] + [0])
        best = max(best, (ints[0] if ints else 0) + inner)
    return best


def lookback(code_lines):
    """Slow lookback: the alpha's nested window/lag need, +70 for ts_fill, +20 warm-up, in [60, 300]."""
    needs = {}
    for l in code_lines:
        c = strip_comment(l)
        if re.match(r"\s*[A-Za-z_]\w*\s*=(?!=)", c):
            name, rhs = c.split("=", 1)
            needs[name.strip()] = expr_need(rhs, needs)  # sequential: redefinitions see earlier values
    code = "\n".join(strip_comment(l) for l in code_lines)
    lb = needs.get("alpha", 0) + (70 if "ts_fill" in code else 0) + 20
    return min(max(lb, 60), LB_MAX)


def ledger_metrics(tag):
    p = ROOT / "alphas" / "ledger.md"
    if not p.exists():
        return None, None
    for l in p.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) == 13 and c[1] == tag:
            ir = re.match(r"-?\.?\d+\.?\d*", c[8])
            co = re.match(r"-?\.?\d+\.?\d*(@\d+)?( own)?", c[9])
            if ir or co:
                return (ir.group() if ir else None), (co.group() if co else None)
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("parent")
    ap.add_argument("techniques", nargs="+")
    ap.add_argument("--out", default=str(ROOT / "alphas" / "drafts" / "repairs.json"))
    ap.add_argument("--print", action="store_true")
    ap.add_argument("--tag")
    ap.add_argument("--force", action="store_true", help="replace an existing tag in --out")
    a = ap.parse_args()
    if len(a.techniques) > 2:
        die("at most 2 techniques stacked")
    if any(t in ("w10", "multihorizon") for t in a.techniques[1:]):
        die("w10/multihorizon edit the parent's windows: list them first")
    bad = [t for t in a.techniques if t not in INFO]
    if bad:
        die(f"unknown technique {bad}; choose from {', '.join(INFO)}")
    drafts = load_drafts()
    if a.parent not in drafts:
        die(f"parent tag {a.parent} not in alphas/drafts/*.json")
    par = drafts[a.parent]
    head, code = split_expr(par["expr"])
    for t in a.techniques:
        code = apply(t, code)
    ir, co = ledger_metrics(a.parent)
    met = ", ".join(x for x in ([f"IR {ir}"] if ir else []) + ([f"corr {co}"] if co else []))
    desc = " + ".join(INFO[t][0] for t in a.techniques)
    src = "; ".join(dict.fromkeys(INFO[t][1] for t in a.techniques))
    rep = f"# Repair: {desc} ({src}). Parent {a.parent}" + (f" {met}." if met else ".")
    expr = "\n".join(head + [rep] + code)
    tag = a.tag or "R_" + re.sub(r"^[A-Za-z]_", "", a.parent) + "_" + "_".join(a.techniques)
    lb = lookback(code)
    item = {"tag": tag, "base": par.get("base"), "family": par.get("family") or par.get("base"),
            "parent": a.parent, "technique": "+".join(a.techniques), "expr": expr,
            "lb": lb, "wlb": lb, "state": "squeued"}
    errs, warns, _, nv = check(expr)
    if a.print:
        print(expr)
    if expr_hash(expr) == expr_hash(par["expr"]):
        die(f"{'+'.join(a.techniques)} leaves {a.parent}'s code unchanged (e.g. slow3x on a 3x parent)")
    out = Path(a.out)
    tags, hashes = known_items(out.resolve())
    if not a.force:
        if tag in tags or tag in drafts:
            die(f"tag {tag} already exists in the ledger or drafts; use --tag")
        if expr_hash(expr) in hashes:
            die(f"same code as {hashes[expr_hash(expr)]}")
    items = json.loads(out.read_text(encoding="utf-8")) if out.exists() else []
    if any(x["tag"] == tag for x in items) and not a.force:
        die(f"{tag} already in {out} (it may have run); use --tag or --force")
    if not errs:  # never write a variant that fails the checker
        items = [x for x in items if x["tag"] != tag] + [item]
        out.write_text(json.dumps(items, indent=1), encoding="utf-8")
    print(f"{'FAIL (not written)' if errs else 'PASS'} {tag} (vars={nv}, lb={lb}) -> {out}"
          + "".join(f"\n  - {e}" for e in errs) + "".join(f"\n  ~ {w}" for w in warns))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
