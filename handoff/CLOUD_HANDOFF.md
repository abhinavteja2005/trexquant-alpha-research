# CLOUD HANDOFF from the local master (Claude Desktop, Oct 5-6) — read this first

You are the new MASTER of TrexQuant Alpha Factory, running as a claude.ai/code cloud session. The local
Desktop session (which built the toolchain below) is retired to save Abhinav's Pro weekly limit.
Read order: this file -> `handoff/MEMORY.md` (LATEST) -> `handoff/AUTORESEARCHER.md` -> `handoff/cycle.md`
-> `knowledge/repair-playbook.md` (Portal facts) -> tail of `knowledge/lessons.md` -> `CLAUDE.md` (hard rules).

## 0. First action: verify billing (user's request)
Abhinav moved to the cloud because he believes his $100 credit pays for cloud sessions and the local session
was eating his Pro plan (5-hour 64%, weekly 47% on Oct 6). Ask him to compare, after ~30 min of your work:
claude.ai -> Billing (credit balance should DROP) and claude.ai/settings/usage (Pro meters should stay FLAT).
If the Pro meters still move, tell him plainly and switch to the lean model policy (section 6).
Note: `handoff/MEMORY.md` says an earlier claude.ai chat did NOT draw the credit, so this is unverified.

## 1. Competition state (Oct 6, 16:45 IST)
- SUBMITTED 4/100: T_LATE_w3, T_LATE_accr_w2, T_COMP7 (IR/sqrt(TVR) route), U_VWAPT_FMOM_w1 (corr .466, manual).
- ~150 alphas tested; full list with status in `alphas/registry.md|csv` (cloud chat) and `alphas/ledger.md` (local).
- Best lead (cloud chat): anti-correlated partners (accruals) blended into blocked reversals; 4 Y_ blends were running.
- Fast mode is NOT a cheap copy of Slow (daily PnL corr .34; Fast pool-corr reads far too low). Judge in Slow only.

## 2. What the local master did
| When | What | Where |
|---|---|---|
| Oct 5 | Phase 0 checks: git push OK, subagents OK (Opus/Sonnet), internet OK, Chrome+Trexsim OK | reports in chat |
| Oct 5 | Variables (253 unique of 255) and the 32 builtin + 4 custom operators from `/trexsim/pysim/api/builtin_operators/` | `knowledge/variables.json`, `knowledge/operators.md` |
| Oct 5 | Official tutorial (Google Doc linked in the portal sidebar): Fast!=Slow causes = short lookback, forward bias, corporate adjustments on non-dimensionless inputs; 0 is not "no position" | `knowledge/lessons.md` |
| Oct 5 | 25 hand-translated 101 Formulaic Alphas (dimensionless, allowed windows) | `tools/alpha101.py` -> `alphas/drafts/a101.json` |
| Oct 5 | Cycle 1 (Opus): 8 sourced idea cards + 14 non-reversal drafts: vol-of-vol, coskewness, VIX-gated residual reversal, variance-ratio regime, Parkinson-vs-close vol, downside beta, trade size, MAX | `ideas/backlog.md`, `alphas/drafts/c1.json` |
| Oct 5 | Queue file for the shared runner (LOADED by the cloud chat; do not load again) | `alphas/queue/next.json` |
| Oct 6 | Stage 1 build (Sonnet builders + 2 Opus reviews, 17 defects fixed) | `tools/*.py` (below) |
| Oct 6 | Portal dtype rules wired into the checker; Q_FROG's crash cause found (ts_mean of a flag) | `tools/check_alpha.py` |
| Oct 6 | Crash forensics harness + recovered code of 10 crashed jobs that were never saved in the repo | `tools/crash_report.py`, `alphas/crashes/` |

## 3. Toolchain (all in `tools/`, stdlib Python; run from repo root)
| Tool | Purpose | Tested |
|---|---|---|
| check_alpha.py | Static gate: unknown vars/operators, >10 vars, forbidden earnings var, Thesis/Source lines, raw levels, windows {3,5,10,20,40,60,120,250} (delta lag 1-2 ok), negative ts_delay, dup tag/code vs ledger+drafts, **bool - bool**, **ts_*/cs_* on a true/false flag** | yes; `test_checker.py` 15/15 |
| test_checker.py | Regression suite over `tests/checker_cases.json` (every known crash must stay caught) | yes |
| originality.py | AlphaAgent-style similarity vs tested/submitted drafts; REJECT > .8, WARN > .6; code-skeleton clones rejected; deliberate repairs skip their parent | yes |
| bandit.py | Thompson sampling over families -> `reports/next_slots.md` (30% explore) | yes |
| repair.py | Playbook repairs: band, ewm, weekly, w10, szvo, slow2x, slow3x, multihorizon, winsor, gate; lookback = nested need +70 ts_fill +20, cap 300; refuses failing/no-op/duplicate variants | yes (2 Opus reviews) |
| mutate.py | Near-miss variants (sub-industry, smoothing, volume/vol tilt, tails, window grid, data swaps) | yes |
| ledger_sync.py | Runner snapshot (JS printed by the script) -> `alphas/ledger.md` + `alphas/runner-export.json`; Slow corr cell = `corr@blocker (irtvr vs bar)`; submitted = YES | yes on synthetic data |
| families.py | Family scoreboard -> `reports/families.md` | yes |
| make_queue.py | Drafts -> `alphas/queue/next.json` (SLOW: squeued + lb, FAST: queued) | yes |
| crash_report.py | Failed/empty jobs -> `alphas/crashes/pending.json` with code; prints a read-only JS snippet to recover code from localStorage | yes |

## 4. Potential issues to VERIFY (not yet proven on the portal)
1. **Expressions in the runner but not in the repo.** The cloud chat queued many jobs directly (R_, G_, U_, X_, Y_ ...). Rule from now on: every queued expr is first saved in `alphas/drafts/*.json`. Recover missing code with the `crash_report.py` snippet pattern (code only, comments stripped).
2. **Two record files**: `alphas/ledger.md` (ledger_sync) and `alphas/registry.md|csv` (cloud chat). Unify: make ledger_sync also regenerate registry.csv, or retire one.
3. **ledger_sync on real data**: only tested on synthetic snapshots. First real sync: check that the existing hand-written rows are updated, not duplicated.
4. **New repair templates untested on the portal**: band (weighted book, float32 flags via `(q*0 + 1)*cond`) and weekly (`(day_of_the_week*0 + 1)*cond`). Run one each and confirm they don't crash.
5. **dtype edge cases not yet covered by the checker**: int64/float64 into ts_*/cs_* (e.g. `1 - flag`, `1.0*flag`), cs_indneut/cs_factorneut group arguments that are not integer codes, lb > 300 or lb < need. The Crash Analyst should add these (section 5).
6. **A101_012 and A101_030** in the runner are the OLD code (bool - bool) and will crash; A101_009 also used bool sums. Fixed versions are in `a101.json`: queue as A101_012b, A101_030b, A101_009b.
7. **repair.py minor gap**: w10 only swaps windows that are a call's last argument (ts_mean_exp(x, 5, .7) untouched).
8. `np.*` was never verified on the portal; the tools avoid it.
9. Cycle-1 (14 Slow) and A101 (25 Fast) results: still queued at 16:40; check them, run `ledger_sync`, `families`, `bandit`.

## 5. Paused / to continue (in this order)
1. **Billing check** (section 0).
2. **Browser connection + runner takeover** (section 7). Nothing in Chrome until Abhinav says "the tab is yours".
3. **Crash Analyst (Opus)** — was stopped before writing anything. Run `python tools/crash_report.py`, then the
   brief "Brief: Crash Analyst" in `handoff/cycle.md` on `alphas/crashes/pending.json` (12 crashes: 3 Fast timeouts,
   Q_FROG, U_FMOM5 empty, U_FMOM5_lb330, R_PRICE2_band, R_RIG_weekly, 4 G_ gates). Deliver `knowledge/crashes.md`,
   the rules in 4.5, FAIL+PASS cases, `test_checker` green, all drafts re-checked. Then review its checker changes
   with a separate Opus reviewer (this caught 17 defects last time).
4. **Stage 2 of AUTORESEARCHER.md**: R3_owner, status line, `runner/px.js` B0 test, `PX.triage(.065)` audit,
   record the pending repair tests in `knowledge/repairs.md`, B3 blend search.
5. **First full cycle** (cycle.md + AUTORESEARCHER section 3) WITH a separate blind Critic (never run yet),
   then the daily Analyst. Ask Abhinav once about a scheduled task after a full cycle works.

## 6. Agents and models (agreed with Abhinav)
| Role | Model |
|---|---|
| Master + runner operator (you, inline) | Opus |
| Scout, Writer, Critic (separate, blind), Crash Analyst, Code Reviewer, daily Analyst | Opus |
| Builder (mechanical tool code; always followed by an Opus review) | Sonnet |
| Sync, repairs, mutations, bandit, originality, queue files | scripts, no LLM |
Lean policy if billing turns out to hit the Pro plan: Opus only for Scout/Writer/Critic/Crash Analyst, Sonnet for
reviews and analysis, max 1-2 Opus pods per 5-hour window. Subagent briefs point to files; outputs are short.

## 7. Browser connection (Claude in Chrome) and the runner
- Chrome work ONLY in Abhinav's own Chrome on his Windows ASUS laptop. A Mac linked to the account belongs to a
  friend: never use it. Load the tools in ONE ToolSearch call (see the claude-in-chrome server instructions), then
  `list_connected_browsers`; pick the Windows one (`select_browser`) if more than one is listed.
- Claude in Chrome only controls tabs inside THIS session's tab group. The runner (`window.R`, v3) lives in the tab
  titled **"RUNNER - do not reload"**. Abhinav must drag that tab into the new session's tab group (or Plan B in
  AUTORESEARCHER.md section 0: close it, open alphalist in your group, paste `runner/runner.js` — NOT
  `localStorage.R3_code` — and call `RUNNER()`; job state survives in `localStorage.R3_jobs`).
- On takeover: check `window.R`, `R.counts()`, `R.cur()`, seconds since `R.lastTick` (`R.tick()` if > 90 s),
  `R._lbPatched` (re-apply the lookback patch from lessons Oct 6 11:00 if missing), then set
  `localStorage.R3_owner = 'cloud ' + new Date().toISOString()` and put "Runner owner: Cloud (since ...)" at the top
  of `reports/status.md`.
- Never reload or navigate the runner tab; use another tab to browse. Never edit `R.cfg`, `R.promoteOk`,
  `R.submitOk`. One runner only. Never type credentials; if Trexsim is logged out, stop and tell Abhinav.
- The Chrome privacy filter redacts anything URL-like in JS results, so full expressions (with `# Source:` URLs)
  cannot be read back: keep expressions in the repo; read code-only (comments stripped) when recovering.
- JS results are truncated around ~1000 characters per string: return arrays of short strings.
- Chrome freezes hidden tabs: Abhinav keeps the Chrome window visible; if `R.lastTick` is stale call `R.tick()`.
- Useful portal endpoints: `/trexsim/pysim/api/builtin_operators/`, `/trexsim/pysim/api/data_description_browser/`,
  `/trexsim/pysim/alpha/<id>/?format=json`; the tutorial is the Google Doc linked from the portal sidebar
  (export as txt via `/document/d/<id>/export?format=txt` inside a docs.google.com tab).
