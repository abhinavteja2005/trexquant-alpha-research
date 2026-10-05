"""Static checker for Trexsim alpha drafts. Run before queueing anything.

Usage:
  python tools/check_alpha.py alphas/drafts/c1.json      # [{tag, base, expr, ...}, ...]
  python tools/check_alpha.py alpha.txt                  # one alpha's code
  python tools/check_alpha.py drafts.json --json         # machine-readable result
  python tools/check_alpha.py drafts.json --no-dupes     # skip the ledger/drafts duplicate check
Exit code 1 if any alpha fails.

Rejects: unknown variables or operators, > 10 variables, the forbidden earnings
variable, missing '# Thesis:' / '# Source:' lines, raw price/volume levels,
windows outside ALLOWED_WINDOWS, and tags/expressions already in the ledger or
in another drafts file. Warns on code lines without a comment.
"""
import hashlib
import json
import keyword
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARS = set(json.loads((ROOT / "knowledge" / "variables.json").read_text()))
MAX_VARS = 10
FORBIDDEN = {"trading_days_until_next_earnings_announcement"}
ALLOWED_WINDOWS = {3, 5, 10, 20, 40, 60, 120, 250}
# knowledge/operators.md: 32 builtins + the user's 4 custom operators + safe Python builtins.
OPERATORS = {
    "at_nan2zero", "at_signlog", "at_signsqrt", "at_zero2nan",
    "cs_booksize", "cs_factorneut", "cs_harmonic_mean", "cs_indneut", "cs_poslimit", "cs_rank",
    "cs_remove_middle", "cs_scale", "cs_shrink_balance", "cs_winsor", "cs_zscore",
    "ts_corr_binary", "ts_delay", "ts_diff", "ts_fill", "ts_harmonic_mean", "ts_max", "ts_mean",
    "ts_mean_exp", "ts_median", "ts_min", "ts_norm", "ts_rank", "ts_skew", "ts_std",
    "ts_std_normalized", "ts_sum", "ts_zscore",
    "delta", "decay_linear", "ts_argmax", "ts_argmin",
    "abs",
}
GROUPS = {"industry", "subindustry", "sector"}
# Operators whose LAST integer argument is a lookback window.
WINDOWED = re.compile(r"^(ts_(?!delay$|diff$)\w+|decay_linear|delta)$")
# Level variables: price, volume or size in raw units. Must appear in a ratio,
# a rank/correlation over time, or a log, never as a bare level.
LEVEL = re.compile(
    r"^(open|high|low|close|volume|mktcap|shsout|shsfloat|cashdvd|close_spx|close_vix"
    r"|(open|high|low|close)_price_(first|last)_hour|vwap_(first|last)_hour"
    r"|volume_(first|last)_hour|number_of_trades_(first|last)_hour)$")
SCALE_FREE = re.compile(r"/|ts_corr|ts_rank|ts_zscore|at_signlog")
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def strip_comment(line):
    return line.split("#", 1)[0]


def expr_hash(expr):
    code = "\n".join(strip_comment(l).strip() for l in expr.splitlines())
    return hashlib.sha1(re.sub(r"\s+", "", code).encode()).hexdigest()[:12]


def call_args(code, start):
    """Split the argument list of the call whose '(' is at code[start]."""
    depth, args, cur = 0, [], ""
    for ch in code[start:]:
        if ch == "(":
            depth += 1
            if depth == 1:
                continue
        elif ch == ")":
            depth -= 1
            if depth == 0:
                args.append(cur.strip())
                return args
        elif ch == "," and depth == 1:
            args.append(cur.strip())
            cur = ""
            continue
        cur += ch
    return args


def check(expr):
    errs, warns = [], []
    lines = expr.splitlines()
    if not any(l.strip().startswith("# Thesis:") for l in lines):
        errs.append("missing '# Thesis:' line")
    if not any(l.strip().startswith("# Source:") for l in lines):
        errs.append("missing '# Source:' line")

    code_lines = [strip_comment(l) for l in lines]
    code = "\n".join(code_lines)
    if not re.search(r"^\s*alpha\s*=", code, re.M):
        errs.append("no 'alpha =' assignment")
    for i, l in enumerate(lines, 1):
        if l.strip() and not l.strip().startswith("#") and "#" not in l:
            warns.append(f"line {i}: no comment")

    local = set(re.findall(r"^\s*([A-Za-z_]\w*)\s*=(?!=)", code, re.M))
    used, unknown, bad_ops = set(), set(), set()
    for m in IDENT.finditer(code):
        name = m.group()
        if m.start() > 0 and (code[m.start() - 1].isdigit() or code[m.start() - 1] == "."):
            continue  # part of a number like 1e5 or an attribute
        if code[m.end():].lstrip().startswith("("):
            if name not in OPERATORS:
                bad_ops.add(name)
            continue
        if name in local or keyword.iskeyword(name) or name in {"True", "False", "None", "int_factors"}:
            continue
        (used if name in VARS else unknown).add(name)

    if unknown:
        errs.append("unknown variables: " + ", ".join(sorted(unknown)))
    if bad_ops:
        errs.append("unknown operators: " + ", ".join(sorted(bad_ops)))
    if len(used) > MAX_VARS:
        errs.append(f"{len(used)} variables > {MAX_VARS}")
    bad = used & FORBIDDEN
    if bad:
        errs.append("forbidden variable: " + ", ".join(sorted(bad)))

    for i, line in enumerate(code_lines, 1):
        levels = {n for n in IDENT.findall(line) if LEVEL.match(n)}
        if levels and not SCALE_FREE.search(line):
            errs.append(f"line {i}: raw level {', '.join(sorted(levels))} (not in a ratio/rank/log)")

    for m in re.finditer(r"([A-Za-z_]\w*)\s*\(", code):
        if not WINDOWED.match(m.group(1)):
            continue
        args = call_args(code, m.end() - 1)
        ints = [a for a in args[1:] if re.fullmatch(r"\d+", a)]
        allowed = ALLOWED_WINDOWS | ({1, 2} if m.group(1) == "delta" else set())  # delta takes a lag
        if ints and int(ints[-1]) not in allowed:
            errs.append(f"{m.group(1)} window {ints[-1]} not in {sorted(ALLOWED_WINDOWS)}")
    for m in re.finditer(r"ts_delay\s*\(", code):
        args = call_args(code, m.end() - 1)
        if len(args) > 1 and args[-1].lstrip().startswith("-"):
            errs.append("ts_delay with a negative lag (forward bias)")

    return errs, warns, len(used - GROUPS), len(used)


def known_items(exclude):
    """Tags in the ledger, and tag -> expr hash for every drafts file except `exclude`."""
    tags, hashes = set(), {}
    ledger = ROOT / "alphas" / "ledger.md"
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.split("|")]
            if len(cells) > 3 and cells[2] and cells[2] not in {"Tag", "---"}:
                tags.add(cells[2])
    for f in (ROOT / "alphas" / "drafts").glob("*.json"):
        if f.resolve() == exclude:
            continue
        for it in json.loads(f.read_text(encoding="utf-8")):
            tags.add(it["tag"])
            hashes[expr_hash(it["expr"])] = it["tag"]
    return tags, hashes


def main(argv):
    p = Path(argv[0]).resolve()
    as_json, dupes = "--json" in argv, "--no-dupes" not in argv
    if p.suffix == ".json":
        items = json.loads(p.read_text(encoding="utf-8"))
    else:
        items = [{"tag": p.stem, "expr": p.read_text(encoding="utf-8")}]
    tags, hashes = known_items(p) if dupes else (set(), {})
    seen_tags, seen_hash, results = set(), {}, []
    for it in items:
        errs, warns, nv, nv_all = check(it["expr"])
        h = expr_hash(it["expr"])
        if dupes and it["tag"] in tags:
            errs.append("tag already in ledger/drafts")
        if it["tag"] in seen_tags:
            errs.append("tag repeated in this file")
        if h in hashes or h in seen_hash:
            errs.append(f"same code as {hashes.get(h) or seen_hash.get(h)}")
        seen_tags.add(it["tag"])
        seen_hash[h] = it["tag"]
        results.append({"tag": it["tag"], "ok": not errs, "vars": nv_all, "errors": errs, "warnings": warns})
    failed = sum(not r["ok"] for r in results)
    if as_json:
        print(json.dumps(results, indent=1))
    else:
        for r in results:
            print(f"{'PASS' if r['ok'] else 'FAIL'} {r['tag']} (vars={r['vars']})"
                  + "".join(f"\n  - {e}" for e in r["errors"])
                  + "".join(f"\n  ~ {w}" for w in r["warnings"]))
        print(f"{len(items) - failed}/{len(items)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
