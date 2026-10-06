# AUTORESEARCHER: program for the local master (Claude Desktop)

Background: `knowledge/autoresearch-survey.md` (Man Group AlphaGPT, AlphaAgent, RD-Agent(Q), Alpha Jungle,
QuantaAlpha, the WorldQuant BRAIN skill, Karpathy autoresearch). This file is our version of Karpathy's
`program.md`: a fixed evaluation harness, cheap deterministic filters, an LLM research pod, and a loop that does
not stop to ask.

## 0. Ownership (read first)
There is exactly ONE runner (`window.R`, runner v3) in ONE Chrome tab. It is the only thing allowed to start
simulations. Claude in Chrome can only drive tabs inside the calling session's own tab group, so whoever owns the
tab owns the runner.

Handover (Oct 6): the cloud chat is retiring from Chrome. Abhinav moves the Trexsim tab into the Desktop session's
tab group (drag it onto the group), or uses Plan B below. Then the Desktop session:
1. Finds the tab, checks `window.R`, `R.counts()`, `R.cur()`, and seconds since `R.lastTick`.
2. Runs `localStorage.R3_owner = 'desktop ' + new Date().toISOString()`. From then on, any other Claude that sees
   R3_owner set to another owner must not touch the tab.
3. Writes `Runner owner: Desktop (since <time>)` at the top of `reports/status.md` and pushes.

Plan B (if dragging fails): Abhinav CLOSES the old Trexsim tab first (two live runners would overwrite each
other). The Desktop session then opens https://www.trexsim.com/trexsim/pysim/alphalist in its own group and
rebuilds the runner: `eval(localStorage.R3_code)` or paste `runner/runner.js`, then `RUNNER()`. Job state survives
in `localStorage.R3_jobs`. A Slow job that was running keeps running on the server, and the runner picks up its
result by id.

Never: open a second runner, reload or navigate the runner tab, edit `R.cfg` / `R.promoteOk` / `R.submitOk`,
delete submissions, type credentials, or simulate by hand on the portal while the runner works.

## 1. Architecture
| Layer | What | Cost |
|---|---|---|
| Harness (fixed) | `window.R`: queue -> Slow sim -> metrics -> auto-submit if Slow IR >= .072, eligible, recency IR >= .04, best-year share <= .5 | free (simulator time) |
| In-page tools | `runner/px.js` (`window.PX`): daily-PnL correlation with our submissions; blend prediction from finished parts | free |
| Local tools | `tools/check_alpha.py`, `make_queue.py`, `ledger_sync.py`, `families.py`, `mutate.py`, plus B1-B3 below | free |
| LLM pod | Scout (ideas + sources), Writer (thesis -> code), Critic (alignment, look-ahead, sign, originality) | the only token cost |
| Memory | `handoff/MEMORY.md`, `knowledge/lessons.md`, `alphas/ledger.md`, `ideas/backlog.md`, `reports/families.md` | free |

## 2. Build tasks (do these once, before running cycles; each has a test)
- B0. Paste `runner/px.js` into the runner tab. Test: `PX.own('T_LATE_s3_w2')` returns about `{T_LATE_w3: .99, ...}`.
  Note: PX correlation reads .04-.08 HIGHER than the portal's figure, so it is a conservative filter.
- B1. `tools/originality.py` (AlphaAgent originality / Alpha Jungle subtree avoidance): parse each draft's code
  into a normalised token or AST set (variables + operators + windows, ignoring comments). Report the max Jaccard
  overlap with (a) every alpha already in `alphas/drafts/*.json` that has a ledger row and (b) our submitted
  alphas. Reject > .8 and warn > .6. Test: a copy of T_COMP7 with one window changed is rejected.
- B2. `tools/bandit.py` (RD-Agent's Thompson sampling, simplified): for each family in the ledger, hit = Slow IR
  >= .065 AND (eligible OR corr <= .6). Draw from Beta(hits+1, misses+1) and allocate the next N slots in
  proportion, keeping >= 30% for families with < 3 tests (exploration). Output: `reports/next_slots.md`. Test: runs
  on the current ledger and gives COMP/LVREV-type families more slots than 52WH or BAB.
- B3. Extend the cycle with a "blend search" step: when two finished alphas each have Slow IR >= .04 and
  `PX.pair` corr < .4, try `PX.blend([[a,1],[b,w]])` for w in {.5, 1, 2, 3}. Queue the real blend only if the
  predicted IR >= .08 and every `ownCorr` < .55. Write the blend as one documented alpha (both theses, both
  sources).
- B4. Fill gaps in `tools/ledger_sync.py` so it records Slow metrics (ir, tvr, irtvr, corr, corrId, corrIrTvr,
  oos1, rw, best, vt) and the `submitted` state. Test: the 3 submissions appear in the ledger with `YES`.

## 3. The cycle (Karpathy-style; do not ask Abhinav whether to continue)
Trigger: Slow queue (`squeued` + `ssim`) < 8 jobs. A normal day needs 3-5 cycles; the simulator runs ~60-100 Slow
jobs a day.
1. Sync: `git pull`; snapshot runner -> `ledger_sync.py`; `families.py`; `bandit.py`.
2. Learn: for each new Slow result note IR, irtvr, corrId and the bar it needed (1.2 x corrIrTvr). Add 1-3 numeric
   lessons. If something was submitted, run `PX.own` on it and record its correlations with the others.
3. Generate ~20 drafts, in this priority order (cheapest first):
   a. Deterministic: `mutate.py --auto` on near-misses (IR >= .065, or irtvr within 15% of its bar), and the B3
      blend search. No LLM needed.
   b. LLM pod, in parallel, sized to the bandit slots:
      - Scout (Opus): 6-8 idea cards with an opened source URL, in families the bandit favours or has not yet
        explored. MEMORY.md "Next directions" comes first.
      - Writer (Opus): cards -> `alphas/drafts/c<N>.json`.
      - Critic (Opus, separate agent, has not seen the Writer's reasoning): for each draft check (i) the code
        implements the thesis with the right sign (Man Group's consistency check), (ii) no look-ahead, (iii) it is
        dimensionless, (iv) it is simple (drop drafts with > 6 code lines unless justified, as in AlphaAgent's
        complexity control). Return keep or drop with one line per draft.
4. Filter: `check_alpha.py` -> `originality.py` -> drop duplicates. Expect ~15 survivors.
5. Queue: `make_queue.py SLOW:<file>` -> `R.add`, then set `squeued` + explicit `lb`, then `R.save()`. At most 5 per
   family. Never Fast for correlation questions.
6. Log: commit and push the ledger, lessons, drafts and `reports/status.md`. Report to Abhinav in 5 lines.

Keep / discard (the metric): an alpha is KEPT if the runner submits it. A near-miss is kept as a mutation parent.
Everything else is logged and dropped. At equal score, simpler wins.

## 4. Budget rules (minimal credit)
- No LLM polling. Between cycles, check the runner with one short JS call every 20-30 min, or not at all if a
  scheduled task drives the cycles.
- Subagent briefs are short and point to files; agents return file paths and one-line summaries, not dumps.
- Use Opus for the Scout, Writer and Critic (user requirement). Use Sonnet or plain scripts for sync, queueing and
  the ledger.
- One cycle should cost roughly 100-200k tokens. If a cycle produces 0 kept or near-miss alphas twice in a row,
  switch family focus (bandit) before spending more.
- If Claude Desktop supports a local scheduled task, propose one to Abhinav ("run one cycle per
  handoff/AUTORESEARCHER.md", every 3 hours) and create it only after he says yes.

## 5. Stop conditions
100 submissions; Abhinav says stop; Trexsim logged out (stop and tell him); the runner errors twice in a row
(stop and tell him); the plan budget is near its limit (tell him).
