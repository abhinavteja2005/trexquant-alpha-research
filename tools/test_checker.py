"""Regression suite for tools/check_alpha.py: every known portal crash must stay caught, and known-good
patterns must keep passing. Cases live in tests/checker_cases.json:
  [{"name", "code", "expect": "FAIL"|"PASS", "match": "<substring of the expected error>", "origin"}]
`code` has no Thesis/Source lines; they are added here. The Crash Analyst adds a case for every new crash.
Usage: python tools/test_checker.py   (exit 1 on any regression)
"""
import json
import sys
from pathlib import Path

from check_alpha import check

ROOT = Path(__file__).resolve().parent.parent
HEAD = "# Thesis: test case\n# Source: test case\n"


def main():
    cases = json.loads((ROOT / "tests" / "checker_cases.json").read_text(encoding="utf-8"))
    bad = 0
    for c in cases:
        code = "\n".join(l if "#" in l else l + "  # c" for l in c["code"].splitlines())
        errs = check(HEAD + code)[0]
        hit = [e for e in errs if c.get("match", "") in e] if c["expect"] == "FAIL" else errs
        ok = bool(hit) if c["expect"] == "FAIL" else not errs
        bad += not ok
        if not ok:
            print(f"REGRESSION {c['name']} (expected {c['expect']}{' ~ ' + c['match'] if c.get('match') else ''})"
                  + "".join(f"\n  - {e}" for e in errs))
    print(f"{len(cases) - bad}/{len(cases)} checker cases OK")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
