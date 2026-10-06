# Auto-researcher cycle (manual: "run a cycle")

Lean target: ~20 new drafts per cycle, <= 5 per family. Expressions live ONLY in `alphas/drafts/*.json`
(the Chrome filter redacts them in the runner), metrics come from the runner, joined on tag.

## Steps
1. `git pull`. Read `knowledge/lessons.md` (tail), `reports/families.md`, `ideas/backlog.md` (tail).
2. Operator (master, inline): in the Trexsim tab, check `window.R` (v3) is alive; run the JS printed by
   `python tools/ledger_sync.py`; save the lines to `alphas/snapshots/<YYYYMMDD-HHMM>.txt`;
   `python tools/ledger_sync.py <snapshot>` then `python tools/families.py`.
3. In parallel (one message), with the briefs below:
   - Scout (Opus): 6-8 new idea cards.
   - Writer+Critic (Opus): ~12 drafts from the newest untested cards -> `alphas/drafts/c<N>.json`.
   - Mutator: `python tools/mutate.py --auto --max 4` (deterministic, no agent needed); a Sonnet agent
     only if there are near-misses without expressions to rewrite.
4. `python tools/check_alpha.py alphas/drafts/<file>.json` on every new file. Fix or drop FAILs.
5. Operator queues PASS drafts: `window.R.add([{tag, base, expr}, ...])` in batches of <= 10
   (under-tested families first, <= 5 per family). Never touch R.cfg / submitOk / promoteOk.
6. Add 1-3 numeric lessons to `knowledge/lessons.md`, overwrite `reports/status.md`, commit + push,
   report 5 lines: submitted, eligible, best new alpha, what failed, next focus.

## Brief: Scout (Opus)
Quant research scout for the Trexsim competition (US TOP1000, delay 0, industry-neutral, daily IR > .07,
pool corr <= .5). Read `knowledge/variables.json`, `knowledge/operators.md`, `ideas/backlog.md`,
`reports/families.md`, `knowledge/lessons.md` tail. Find 6-8 ideas NOT already in the backlog, each
buildable from the variables (no options data exists: only market VIX/SPX). Prefer uncrowded data:
first/last-hour skew, std, information ratio, trade counts/size; volatility structure; calendar;
sourced anomalies. Open every source URL you cite. Append cards to `ideas/backlog.md` under a
`## Cycle <N>` heading: name | thesis | source URL | variables | horizon | sign | why uncrowded.
Return only the card names. Do not edit any other file.

## Brief: Writer + Critic (Opus)
Alpha engineer and skeptical reviewer. Turn the newest `## Cycle <N>` cards in `ideas/backlog.md`
into ~12 Trexsim alphas in `alphas/drafts/c<N>.json`: `[{tag, base, family, expr, source_url}]`.
Rules: first lines `# Thesis: ...` and `# Source: <url>`; every code line has a `# comment`; last
assignment is `alpha = ...`; only operators in `knowledge/operators.md` (ternary: `c*a + (1-c)*b`);
<= 10 variables; dimensionless (divide price/volume by price/volume); windows {3,5,10,20,40,60,120,250};
no `trading_days_until_next_earnings_announcement`; no negative ts_delay; NaN (at_zero2nan) for
"no position", not 0. Tags: UPPER_SNAKE, unique, family prefix. Run
`python tools/check_alpha.py alphas/drafts/c<N>.json` and fix until all PASS. As critic, drop
anything that is plain 1-5 day reversal without a twist (crowded, pool corr .5-.85).
Return: tag list + one line per dropped idea.

## Brief: Crash Analyst (Opus; run whenever `tools/crash_report.py` lists undiagnosed crashes)
Role: forensic engineer. A crash means OUR code is wrong (alpha, template, tool or runner), not bad luck.
Input: `alphas/crashes/pending.json` (tag, status/state, portal error text incl. simulation_stage, lb/wlb,
expression or code-only expression). Read `knowledge/operators.md`, `knowledge/repair-playbook.md` (Portal facts),
`knowledge/lessons.md`, `tools/check_alpha.py`, `tools/repair.py`, `tools/alpha101.py`, `runner/runner.js`.
For each crash: (1) root cause, pinned to a line of the alpha and, if a tool generated it, to file:line of the
tool; classify: dtype | group-code | lookback | syntax/name | operator-misuse | timeout/heavy | runner-bug |
portal-transient | unknown; (2) a minimal reproduction; (3) a static rule that would have caught it, added to
`tools/check_alpha.py`, plus a FAIL case (and a PASS case for the fixed form) in `tests/checker_cases.json`;
`python tools/test_checker.py` must pass and every file in alphas/drafts must still pass check_alpha
(--no-dupes) unless it really has the bug; (4) the fixed expression; (5) one row per crash in
`knowledge/crashes.md`: | Tag | Stage | Class | Root cause (line) | Rule added | Fixed form | Origin (tool/file) |.
Do not commit, do not use a browser. Return: crashes diagnosed, rules added, and any tool bug found.
