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


CMP = re.compile(r"<=|>=|==|!=|<|>")


def top_level(text, chars):
    """Split text at depth-0 occurrences of single-char operators in `chars` (keeps the operators)."""
    parts, depth, cur = [], 0, ""
    for i, ch in enumerate(text):
        depth += ch == "("
        depth -= ch == ")"
        prev = text[:i].rstrip()
        binary = prev and prev[-1] not in "(,=*/+-<>&|" and not re.search(r"\d[eE]$", prev)  # not unary/1e-5
        if depth == 0 and ch in chars and binary:
            parts += [cur, ch]
            cur = ""
        else:
            cur += ch
    return parts + [cur]


def strip_parens(t):
    """Remove redundant outer parentheses: '((a > b))' -> 'a > b', but not '(a) * (b)'."""
    while t.startswith("(") and t.endswith(")"):
        depth = 0
        for k, ch in enumerate(t):
            depth += ch == "("
            depth -= ch == ")"
            if depth == 0 and k < len(t) - 1:
                return t
        t = t[1:-1].strip()
    return t


def is_bool(text, flags):
    """True if `text` evaluates to a numpy bool matrix: a comparison, a known flag, or a product of those."""
    t = strip_parens(text.strip())
    if re.fullmatch(r"[A-Za-z_]\w*", t):
        return t in flags
    prod = [x for x in top_level(t, "*&|") if x not in "*&|"]
    if len(prod) > 1:
        return all(is_bool(x, flags) for x in prod)
    depth0 = t
    while re.search(r"\([^()]*\)", depth0):
        depth0 = re.sub(r"\([^()]*\)", "", depth0)  # comparisons inside (...) or calls don't count
    return bool(CMP.search(depth0))  # comparisons bind loosest: any depth-0 one makes a bool


def bool_errors(code_lines):
    """Portal dtype rules (lessons Oct 6): bool - bool crashes; ts_*/cs_* reject bool inputs."""
    errs, flags = [], set()
    for i, line in enumerate(code_lines, 1):
        m = re.match(r"\s*([A-Za-z_]\w*)\s*=(?!=)(.*)", line)
        rhs = m.group(2) if m else line
        texts = [rhs] + [a for c in re.finditer(r"\w+\s*\(", rhs) for a in call_args(rhs, c.end() - 1)]
        for t in texts:
            seq = top_level(t, "+-")
            for k in range(1, len(seq) - 1, 2):
                if seq[k] == "-" and is_bool(seq[k - 1], flags) and is_bool(seq[k + 1], flags):
                    errs.append(f"line {i}: bool - bool crashes the portal; cast with (close/close)*(...) first")
        for c in re.finditer(r"\b((?:ts|cs)_\w+)\s*\(", rhs):
            args = call_args(rhs, c.end() - 1)
            if args and is_bool(args[0], flags):
                errs.append(f"line {i}: {c.group(1)} on a true/false flag fails (float32 only); use (close/close)*(...)")
        if m:
            name = m.group(1)
            (flags.add if is_bool(rhs, flags) else flags.discard)(name)
    return errs


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
    errs += list(dict.fromkeys(bool_errors(code_lines)))  # nested call args can repeat a finding
    # Rule A: ts_delay lag must be in ALLOWED_WINDOWS | {1,2,3,4}
    ALLOWED_LAGS = ALLOWED_WINDOWS | {1, 2, 3, 4}
    for m in re.finditer(r"ts_delay\s*\(", code):
        args = call_args(code, m.end() - 1)
        if len(args) > 1 and args[-1].lstrip().startswith("-"):
            errs.append("ts_delay with a negative lag (forward bias)")
        if len(args) > 1 and re.fullmatch(r"\d+", args[-1].strip()):
            lag = int(args[-1].strip())
            if lag not in ALLOWED_LAGS:
                errs.append(f"ts_delay lag {lag} not in {sorted(ALLOWED_LAGS)}")

    # Rule B: cs_indneut group argument must involve a group variable
    for m in re.finditer(r"cs_indneut\s*\(", code):
        args = call_args(code, m.end() - 1)
        if len(args) >= 2:
            group_arg = args[1].strip()
            # Resolve the group arg: if it's a local variable, look up its assignment
            resolved = group_arg
            if re.fullmatch(r"[A-Za-z_]\w*", group_arg):
                assign = re.search(rf"^\s*{re.escape(group_arg)}\s*=(?!=)\s*(.+)", code, re.M)
                if assign:
                    resolved = assign.group(1).strip()
            # Check if any group variable name appears in the resolved expression
            if not any(re.search(r'\b' + g + r'\b', resolved) for g in GROUPS):
                errs.append(f"cs_indneut group '{group_arg}' must use a group variable (industry/subindustry/sector); "
                            f"use industry*0 for one all-stock group")

    # Rule C: lookback warning — compute minimum lookback needed
    max_lag, max_win = 0, 0
    has_ts_fill = bool(re.search(r"\bts_fill\s*\(", code))
    for m in re.finditer(r"ts_delay\s*\(", code):
        args = call_args(code, m.end() - 1)
        if len(args) > 1 and re.fullmatch(r"\d+", args[-1].strip()):
            max_lag = max(max_lag, int(args[-1].strip()))
    for m in re.finditer(r"([A-Za-z_]\w*)\s*\(", code):
        if not WINDOWED.match(m.group(1)):
            continue
        args = call_args(code, m.end() - 1)
        ints = [a for a in args[1:] if re.fullmatch(r"\d+", a)]
        if ints:
            max_win = max(max_win, int(ints[-1]))
    min_lb = max(max_lag, max_win) + (70 if has_ts_fill else 0) + 20
    if min_lb > 300:
        warns.append(f"minimum lookback ~{min_lb} exceeds portal max 300; alpha may fail in Slow mode")

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
