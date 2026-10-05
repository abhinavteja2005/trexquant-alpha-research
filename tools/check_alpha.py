"""Static checker for Trexsim alpha drafts. Run before queueing anything.

Usage:
  python tools/check_alpha.py drafts.json        # [{tag, base, expr}, ...]
  python tools/check_alpha.py alpha.txt          # one alpha's code
Exit code 1 if any alpha fails.

Rejects: unknown variables, > 10 variables, the forbidden earnings variable,
missing '# Thesis:' / '# Source:' lines, raw price/volume levels, and
windows outside ALLOWED_WINDOWS.
"""
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
# Operators whose LAST integer argument is a lookback window.
WINDOWED = re.compile(r"^(ts_\w+|decay_linear|delta)$")
# Level variables: price, volume or size in raw units. Must appear in a ratio,
# a rank/correlation over time, or a log, never as a bare level.
LEVEL = re.compile(
    r"^(open|high|low|close|volume|mktcap|shsout|shsfloat|cashdvd|close_spx|close_vix"
    r"|(open|high|low|close)_price_(first|last)_hour|vwap_(first|last)_hour"
    r"|volume_(first|last)_hour|number_of_trades_(first|last)_hour)$")
SCALE_FREE = re.compile(r"/|ts_corr|ts_rank|ts_zscore|\blog\(")
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def strip_comment(line):
    return line.split("#", 1)[0]


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
    errs = []
    lines = expr.splitlines()
    if not any(l.strip().startswith("# Thesis:") for l in lines):
        errs.append("missing '# Thesis:' line")
    if not any(l.strip().startswith("# Source:") for l in lines):
        errs.append("missing '# Source:' line")

    code_lines = [strip_comment(l) for l in lines]
    code = "\n".join(code_lines)
    if not re.search(r"^\s*alpha\s*=", code, re.M):
        errs.append("no 'alpha =' assignment")

    local = set(re.findall(r"^\s*([A-Za-z_]\w*)\s*=(?!=)", code, re.M))
    used, unknown = set(), set()
    for m in IDENT.finditer(code):
        name = m.group()
        if m.start() > 0 and (code[m.start() - 1].isdigit() or code[m.start() - 1] == "."):
            continue  # part of a number like 1e5 or an attribute
        if code[m.end():].lstrip().startswith("("):
            continue  # function / operator call
        if name in local or keyword.iskeyword(name) or name in {"True", "False", "None"}:
            continue
        (used if name in VARS else unknown).add(name)

    if unknown:
        errs.append("unknown variables: " + ", ".join(sorted(unknown)))
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
        if ints and int(ints[-1]) not in ALLOWED_WINDOWS:
            errs.append(f"{m.group(1)} window {ints[-1]} not in {sorted(ALLOWED_WINDOWS)}")

    return errs, len(used)


def main(path):
    p = Path(path)
    if p.suffix == ".json":
        items = json.loads(p.read_text(encoding="utf-8"))
    else:
        items = [{"tag": p.stem, "expr": p.read_text(encoding="utf-8")}]
    failed = 0
    for it in items:
        errs, nv = check(it["expr"])
        failed += bool(errs)
        print(f"{'FAIL' if errs else 'PASS'} {it['tag']} (vars={nv})" + "".join(f"\n  - {e}" for e in errs))
    print(f"{len(items) - failed}/{len(items)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
