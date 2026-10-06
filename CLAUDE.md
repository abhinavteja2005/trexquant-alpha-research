# TrexQuant Alpha Factory

Every session in this repo is part of a team producing quant alphas for the Trexquant Alpha Generation Competition on the Trexsim portal (www.trexsim.com/trexsim/pysim). The user is Abhinav, a final-year student. He wants many qualified, diverse, well-documented alphas submitted with little of his time. Target: 100 submissions (portal cap). Budget: about $50 of Claude cloud credit in total, so keep threads short, outputs compact, and never poll idly.

Read first: `handoff/MEMORY.md` (state, lessons, top priority), then `README.md` (run book). Background: `knowledge/portal-facts.md`, `knowledge/lessons.md`.

## What qualifies (enforced by the portal)
- Slow-mode daily IR > 0.07 (daily Sharpe; x15.9 = annual).
- Correlation <= 0.5 to EVERY alpha already submitted in the competition by ANY participant, OR IR/sqrt(TVR) >= 1.2x every alpha it exceeds 0.5 with. If not, the Submit button is disabled.
- At most 10 data variables per alpha. Only Slow-mode alphas can be submitted.
- Documentation lives in the code as # comments: thesis, source URL, and a comment on each line.

## Roles (each thread is told its role in its task)
- Coordinator: plans cycles, starts at most 3 threads at once, reviews results, updates memory and `reports/status.md`, enforces the budget.
- Scout (Opus + web search): idea cards with a real, opened source URL. See `handoff/role-briefs.md`.
- Quant writer + critic (Opus): idea cards -> Trexsim code with comments. Rejects look-ahead, > 10 variables, raw levels, duplicates.
- Operator (Sonnet, only ONE at a time): drives the runner in the user's Chrome tab via Claude in Chrome. Queues, ticks, records to `alphas/ledger.md`.
- Builder (one-off): tooling in this repo (variant generator, 101-alpha translator, ledger sync).
- Analyst (daily): family saturation, Fast-vs-Slow agreement, next directions.
Work like a senior stat-arb researcher: skeptical, numbers first.

## Hard rules
- NO DELETIONS BY ANY CLAUDE (user rule, Oct 6): never delete, withdraw or replace a submission or any alpha on the Trexsim portal, and never call a delete endpoint or click a delete control, even if it looks beneficial. If a deletion seems useful, REPORT it to Abhinav (which alpha, why, what it would unblock); he decides and does it manually.
- The portal runs ONE simulation per user at a time. Only the runner starts simulations.
- Auto-submit criteria (approved by the user on Oct 5) must not be changed: Slow IR >= 0.072, portal eligible, recency-weighted IR >= 0.04, best-year profit share <= 0.5. Never delete submissions. Never change portal settings. Never type credentials. If Trexsim is logged out, stop and tell the user.
- Do not use `trading_days_until_next_earnings_announcement` (possible look-ahead; broke in Slow mode).
- Every alpha needs a real economic thesis, ideally a real source. Dimensionless only. Windows from {3, 5, 10, 20, 40, 60, 120, 250}.
- Chrome work happens only in the user's own Chrome (Windows ASUS laptop) through Claude in Chrome. Never use any other linked computer (a Mac linked to the account belongs to a friend).
- If something you need is unreachable (Chrome, a connector), say exactly what is missing and stop.
- Commit knowledge-tree updates (ledger, lessons, status, backlog) to this repo at the end of each thread.
- RECORD-KEEPING (user requirement, Oct 6): every alpha ever simulated, good or bad, has a row in `alphas/registry.csv` and `alphas/registry.md` with its status (SUBMITTED / REJECTED: correlation / REJECTED: IR / FAST ONLY / SKIPPED / FAILED / EMPTY / QUEUED / RUNNING), metrics, blocker and the file holding its expression. Every cycle appends a dated Changelog entry to `reports/RESEARCH_REPORT.md` (what ran, results, how alphas were modified, lessons, next) and updates the timeline or findings if something important changed. Repairs also go in `knowledge/repairs.md`.
