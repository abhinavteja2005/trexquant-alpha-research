# TrexQuant Alpha Factory: run book

Folders: `knowledge/` (portal facts, lessons) · `ideas/` (backlog with sources) · `alphas/` (ledger of every alpha tested) · `reports/` (status, analyses) · `runner/` (the in-browser runner) · `handoff/` (memory and role briefs from the previous master chat).

## One cycle
1. Read `handoff/MEMORY.md`, `knowledge/lessons.md`, `reports/status.md`, and the tails of `alphas/ledger.md` and `ideas/backlog.md`.
2. Operator: in the user's Chrome Trexsim tab, make sure `window.R` (runner v3) is alive. If it isn't, run `eval(localStorage.getItem('R3_code'))`, or paste `runner/runner.js` and call `RUNNER()`. Tick it, read `R.report()`, and append new rows to the ledger.
3. Learn: add 1-3 bullets with numbers to `knowledge/lessons.md`.
4. If fewer than 25 alphas are queued: the Scout researches sourced ideas, and the Writer turns them into documented alphas. The Operator queues them with `window.R.add([{tag, base, expr}])`.
5. Overwrite `reports/status.md` (25 lines max) and commit.

## Runner facts
- States: queued -> fsim -> fdone | squeued -> ssim -> sdone | subq -> submitted | subfail. skipped = deliberately excluded.
- Promotion to Slow: Fast IR >= 0.078, recency IR >= 0.04, best-year share <= 0.5, and (eligible or pool corr <= 0.55).
- Slow lookback: the job's own `lb` if set; else 260 if the code contains 252, 140 if it contains ts_fill, otherwise 2 x max window + 15.
- Fast run takes 1-2 min. Slow run takes 4-45 min. Only one simulation runs at a time.
