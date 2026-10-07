# TrexQuant Alpha Factory: research report

Author: Abhinav (with Claude as research assistant). A living report: every research cycle appends a dated entry to
the Changelog at the bottom. Every alpha, good or bad, is in `alphas/registry.md` / `alphas/registry.csv`.

## 1. The problem
- **Competition:** Trexquant Alpha Generation Competition on the Trexsim portal. An alpha is Python code that outputs
  a stocks x dates matrix of positions for the US TOP1000. The portal de-means it, neutralises it by industry,
  scales it to $1M long / $1M short, and simulates daily PnL (delay 0, end-of-day trading, 2007-2021 in-sample).
- **To qualify:** Slow-mode daily IR > 0.07 (about 1.1 annual Sharpe), and correlation <= 0.5 to EVERY alpha already
  submitted by ANY participant. The exception: IR/sqrt(turnover) >= 1.2x every alpha it exceeds 0.5 with. Plus at
  most 10 data variables, documentation as code comments, and a cap of 100 submissions.
- **Judged on:** quantity, quality and diversity, plus documentation.
- **My constraints:** final-year student time, about $50 of AI credit, one simulation at a time on the portal.

## 2. Approach in one paragraph
I built an automated research loop modelled on how quant pods work, and on published AI alpha researchers (Man
Group's AlphaGPT, AlphaAgent, Microsoft RD-Agent(Q), Alpha Jungle, QuantaAlpha, Karpathy's autoresearch).
1. Agents propose sourced hypotheses and write documented alpha code.
2. A critic checks that the code matches the idea.
3. A browser-side runner simulates candidates on the portal one at a time and records the metrics.
4. Only candidates that meet every rule are auto-submitted.
5. Deterministic tools triage near-misses and repair them.
6. Every result feeds a lessons file that steers the next cycle.

## 3. Timeline
| When | Phase | What happened | Key numbers |
|---|---|---|---|
| Oct 5 pm | Manual baseline | ~60 classic alphas tested by hand in Fast mode: reversal, momentum, fundamentals. Learned the portal rules and the correlation tool | Best: intraday reversal composite, Fast IR .090 but pool corr .649. Fundamentals alone IR < .045 |
| Oct 5 pm | Portal reverse-engineering | Found the simulate / result / eligibility / submit API calls; reproduced the portal's correlation (Pearson of daily PnL, last 500 days) | One simulation per user; >= 2 s between requests |
| Oct 5 night | Runner v3 | JavaScript runner inside the logged-in tab: queue, serial simulation, metrics, IS/OOS split, recency-weighted IR, best-year share, auto-promote to Slow, auto-submit under user-approved rules. Survives hidden tabs (sync XHR) and reloads (localStorage) | 50+ blends of 6 reversal bases x slow fundamental companions |
| Oct 5 21:00 | First "eligible" blends fail | Two blends that looked eligible in Fast failed in Slow | c3_rnd_earn Fast .094 / .56 -> Slow .082 / .688 |
| Oct 5 21:00 | Look-ahead guard | Dropped `trading_days_until_next_earnings_announcement` (possible future information) and skipped 12 jobs | |
| Oct 5 23:15 | **Diagnosis: Fast != Slow** | Same alpha, same dates: Fast vs Slow daily PnL correlate only .34. Fast pool-correlation is far too low (.48 -> .78) | Decision: judge correlation only in Slow |
| Oct 5-6 night | Exploration | 27 Slow runs: price/intraday reversals, reversal + fundamentals, 10 textbook anomalies from papers | Reversal blends IR .085-.096 but corr .70-.74; textbook anomalies abs(IR) < .03 |
| Oct 6 07:00 | **First 3 submissions** | Made the slow, low-turnover part carry most of the risk (2-3x weight) on a less crowded reversal base. All 3 passed via the IR/sqrt(TVR) exception | T_LATE_accr_w2 IR .092; T_COMP7 IR .083 (TVR .05, irtvr .366); T_LATE_w3 IR .073 |
| Oct 6 10:00 | Research on AI researchers | Surveyed AlphaGPT and peers; designed the cost-aware loop (`knowledge/autoresearch-survey.md`) | Bottleneck = simulator (~60-100 Slow runs/day), not ideas |
| Oct 6 10:30 | Repair science | Turnover-reduction literature (banding, partial trading, weekly rebalancing) turned into a repair playbook + triage tool | e.g. P_VWAPT needs TVR 1.05 -> .49 or corr .78 -> .5 |
| Oct 6 11:00 | **Bug found: lookback** | The live runner ignored per-job lookbacks, so in Slow every 250-day delay was empty (issuance and asset-growth parts inactive) | Patched live; fundamental-change composite re-queued |

## 4. How the alphas got better (the evolution)
1. **Single signals:** short-term reversal had the IR (.08-.09) but was crowded (corr .65-.85 with others' submissions).
2. **Blends:** adding slow fundamental companions cut Fast correlation, but Fast was misleading.
3. **Slow-only judgement:** real correlations were .70-.78, so the reversal-heavy blends stayed blocked by a few pool
   alphas (#570310, #605850, #604930).
4. **Changing the route:** instead of fighting for corr <= .5, use IR/sqrt(TVR). Low-turnover signals win that test.
   Weighting the slow part 2-3x lowered turnover from ~.65 to .33-.49 at IR .073-.092, and gave the first 3
   submissions.
5. **Repairs:** for each near-miss, compute the exact gap (target turnover or correlation) and apply a known
   technique: banding, partial trading, weekly rebalancing, longer windows, size/volatility neutralisation, or an
   unrelated partner. Log every before/after in `knowledge/repairs.md`.

## 5. Findings (numbers first)
- Daily IR in this market comes mostly from short-term reversal; plain reversal is crowded.
- Slow accounting composites trade little (TVR ~.05), so IR/sqrt(TVR) reaches .3-.37 even at IR .08.
- Textbook anomalies (52-week high, betting against beta, value x quality, earnings drift, MAX, high-volume premium,
  tug of war, realised skew, VIX beta) earn |IR| < .03 at daily horizon in 2008-2021.
- Size+volatility neutralisation kept a 2-signal blend's IR (.093) and cut its corr (.753 -> .704), but cost a single
  reversal 38% of its IR.
- Longer windows (5 -> 10 days): corr -.09, IR -14%, TVR -15%.
- Our own submissions join the pool: close variants were rejected at .86-.96. Diversity must be designed in.

## 6. Mistakes and fixes (honest log)
| Mistake | Impact | Fix |
|---|---|---|
| Trusted Fast-mode correlation | Promoted blends that failed in Slow | Measured Fast vs Slow PnL (.34); Slow-only judgement |
| Earnings-date variable | Possible look-ahead | Dropped it; 12 jobs skipped |
| Runner ignored per-job lookback | 250-day pieces empty in Slow; one alpha came back with no positions | Live patch (`wlb`); docs and checks updated |
| Hidden Chrome tab froze timers | Runner stalled up to 20 min | Sync XHR ticks; keep the window visible |
| Polled by sleeping in the chat | Blocked the conversation | Queue-and-leave; scripts check results |
| ts_delay(shsout, 252) instead of 250 | 3 Fast timeouts | Checker Rule A: ts_delay lags must be in allowed set |
| cs_indneut(x, close/close) | 4 gate crashes (needs integer group) | Checker Rule B + fixed template to industry*0 |
| Queued with lookback 330 | Portal max is 300 | Checker Rule C: warn if min lookback > 300 |

## 7. Methods borrowed from research
Man Group AlphaGPT (idea -> implement -> evaluate pod, same bar as humans, idea/code consistency checks), AlphaAgent
(originality and complexity regularisers), RD-Agent(Q) (bandit over directions, cost < $10 per run), Alpha Jungle
(avoid overused formula parts), QuantaAlpha (repair the weak step of a near-miss), the WorldQuant BRAIN skill
(self-correlation on daily PnL before submitting), Novy-Marx & Velikov (banding), Garleanu & Pedersen (partial
trading), Hyperband/successive halving (Li et al., JMLR 2018) for the pruned combination grid, the Deflated Sharpe Ratio (Bailey & Lopez de Prado 2014) for counting trials, and synergistic alpha collections (Yu et al., KDD 2023). Links: `knowledge/autoresearch-survey.md`, `knowledge/repair-playbook.md`, `knowledge/grid-search.md`.

## 8. Interview talking points
- Framed a vague goal ("many good alphas") as a constrained optimisation: IR > .07, correlation to a moving pool, a
  turnover-adjusted exception, a serial simulator, and a budget.
- Found that the cheap test (Fast) disagreed with the real one (Slow), proved it with a PnL correlation of .34, and
  changed the whole pipeline to rely on the real test.
- Turned a correlation wall into a turnover problem: the IR/sqrt(TVR) exception made low-turnover designs the winning
  strategy, which produced the first submissions.
- Built engineering for an awkward environment: an in-browser runner with persistence, rate-limit handling and
  auto-submit under explicit rules.
- Kept research discipline: sourced hypotheses, look-ahead guards, out-of-sample splits, multiple-testing caps, and a
  log of every alpha, including failures.

## Changelog (append one entry per cycle: date, what ran, results, lessons, next)
- **Oct 6 11:30:** 3 submitted. 148 alphas logged (49 Fast-only, 33 rejected in Slow, 12 skipped, 4 failed, 1 empty,
  46 queued/running). Repair tests queued: banding, EWMA, weekly rebalance, 3-day mean, fundamental-change composite
  (fixed lookback). Next: hand the runner to the local Claude Desktop, audit near-misses, repair first.
- **Oct 6 11:50: self-learned regime gates.** Rejected the "don't trade before 2010" idea as hindsight (hard-coded
  dates = look-ahead). Built Abhinav's better version instead: the alpha computes its own shadow return every day and
  stands aside after a bad stretch. Theory (Kaminski & Lo 2014) says this only helps if returns are streaky. We tested
  that first by replaying each rule on real PnL (`PX.gate`): reversal alphas are barely streaky (block autocorr
  .03-.08), so stop-losses hurt them. A 60-day strategy-momentum switch improved P_VWAPT (.083 -> .093) and the best
  reversal+fundamental blend (.096 -> .101), and stop-loss / 20-day momentum improved accruals (.067 -> .074 / .076),
  all in both halves of the sample. 4 gated alphas queued. Also learned: portal lookback max is 300; `bool - bool`
  crashes a sim; fundamental-change composite (120-day) IR .028 but corr .49.
- **Oct 6 14:00: first gate runs failed on data types, plus a promising uncrowded blend.** All 4 gated alphas and the weekly rebalance failed: the portal needs integer group codes for cs_indneut and float32 inputs for built-in operators. Fixed and re-queued (plus a per-industry gate variant). Repair results: EWMA IR .085 / IR/sqrt(TVR) .097 (bar .119); banding with on/off flags backfired (turnover 1.93). Highlight: reversal + fundamental-change composite (U_VWAPT_FMOM_w2) is only .436 correlated with the pool, the first blend under .5, but IR .055. A 1:1 version is queued to lift IR. Local cycle-1 volatility ideas: low IR but low correlation (blend-partner candidates).
- **Oct 6 14:50: anti-correlated partners (key discovery); gates retired.** Abhinav flagged five rejected alphas as "close". Triage gave each a gap: the price-reversal blends need IR/sqrt(TVR) .119 (have .087-.097), the illiquid blend needs .169 (has .126), and the reversal + fundamental-change blend has corr .436 but IR .055. Checking how they relate: fundamental-change signals are NEGATIVELY correlated with the reversal blends (-.15 to -.40) and ~0 with our submissions. A replay of mixes predicts IR .096-.106 for price-reversal + fundamental-change. That beats either part, because negatively correlated returns cancel noise (the core idea of combining alphas, Kakushadze 2016). 4 such blends queued, trimmed to 10 variables. The self-learned gates ran after the dtype fix but failed in practice: switching on/off trades the whole book (turnover .05 -> .48), and the in-code shadow return did not match the replay. Gates are retired for now (documented as a negative result).
- **Oct 6 15:40: 4th submission (reversal + fundamental change).** U_VWAPT_FMOM_w1 qualified through the uncorrelated route: corr .466 to the pool, IR .070, turnover .525, robust out of sample (OOS1 .057, recency .062, best-year .18). Abhinav submitted it by hand, ahead of competitors who might take the slot (the runner's own safety bar is IR .072). Story: a 1:2 reversal/fundamental blend had corr .436 but IR .055; moving to 1:1 raised IR to .070 while keeping corr under .5. Also: price blend + fundamental change (1:1) kept IR .093 and cut turnover (.998 -> .689) and correlation (.704 -> .637), as the replay predicted, but not yet below the new blocker's bar.
- **Oct 6 16:40: partner search.** The fundamental-change partner worked as predicted (IR held at ~.09, turnover and correlation fell), but our own 4th submission now blocks that family, and the portal applies the 1.2x bar against every pool alpha above .5 (#604930 needs .173). A systematic scan of all finished alphas for a NEW negatively correlated partner found accruals (corr -.215 with the price blend); the replay predicts price + accruals IR .12, about 30% above either part, with low overlap with our submissions. 4 accrual-partner blends queued.
- **Oct 6 (cloud session): crash forensics.** Moved to a cloud session (saves Pro plan usage). Crash Analyst diagnosed all 12 undiagnosed crashes: 3 Fast timeouts (lag 252 instead of 250), 1 Q_FROG (ts_mean on bool flag), 1 empty (runner lookback bug), 1 lb>300, 1 bool-bool (banding), 1 bool-to-ts_delay (weekly), 4 cs_indneut group-code. Added 3 new checker rules (ts_delay lag, cs_indneut group, lookback warning), 5 test cases (20/20 pass), created knowledge/crashes.md. Fixed gate template in repair-playbook (close/close -> industry*0). Gates retired as a technique (switching raises TVR, kills IR/sqrt(TVR)). Next: reviewer feedback, Chrome takeover, sync, first full cycle.
- **Oct 6 17:30: handover and new directions.** The cloud chat saved the 168-job queue and closed its runner tab, so the local Claude Desktop session can rebuild the runner and own it (Plan B). We decided not to delete submission #695151: its would-be replacements are also blocked by another participant's alpha (#604930, bar .173). New idea cards (`ideas/cards-oct6-new-families.md`):
  - market making: fade uninformed flow and follow informed flow, using within-hour smoothness (information ratio) and trade size (Easley, Lopez de Prado & O'Hara 2012; Barber, Odean & Zhu 2009);
  - closing-auction pressure;
  - residual reversal (Blitz et al. 2013);
  - slow momentum partners: residual momentum, the dtype-fixed frog-in-the-pan, volume-confirmed momentum.
- **Oct 6 17:20: 5 submitted; cloud chat retires.** Abhinav submitted a 5th alpha by hand through the IR/sqrt(TVR) route; Desktop will identify it (most likely the first accrual-partner blend). Hard rule added: no Claude may delete or withdraw any alpha or submission; deletion ideas are reported to Abhinav. The local Claude Desktop session now owns the runner and runs the auto-researcher loop (`handoff/AUTORESEARCHER.md`). The cloud chat stays available for second opinions only.
- **Oct 6 18:30: work split between cloud and laptop.** Billing check passed (cloud sessions draw the credit, not the Pro weekly limit), so research moved to a cloud session. A cloud container cannot drive Chrome, so the runner is now operated by a short Sonnet session on the laptop (`handoff/OPERATOR.md`): it rebuilds the runner, exports a metrics snapshot, runs requested in-page PnL checks (PX), applies skips and loads `alphas/queue/next.json`. The cloud master does everything else on a schedule. Also fixed: `make_queue.py` gave 250-day alphas a 520-day lookback (portal max 300); dtype-fixed A101_009/012/030 re-tagged as *b.
- **Oct 6 22:00: results of the new families, and a strategy change to a FIELD SWEEP.** All 17 queued alphas ran (laptop loop every 30 min worked). Accrual-partner blends are the strongest family: Y_PLsz_ACC_w12 IR .116 (irtvr .138 vs bar .144 against our own 5th submission, .979 corr: needs ~9% less turnover), Y_PLewm_ACC_w1 .101, Y_VW_ACC_w1 .091. The 14 new-family / scraped alphas all failed on IR (best MM1_TOXREV .059; MM2_SIZEREV .042 but pool corr .12, a partner candidate; momentum, liquidity, fundamentals, hour-seasonality -.01 to .035). Lesson: hand-picked textbook anomalies rarely reach daily IR .07 here. The leaders' 500+ submissions point to breadth: correlation is measured on PnL, so alphas built on DIFFERENT DATA are often uncorrelated. Only ~45 of 253 fields had ever been used. New tool `tools/sweep.py` applies 5 standard dimensionless templates (level, 6-month change, deviation from own history; two intraday templates) to the ~190 unused fields (fundamentals scaled by assets/price, ratios, intraday skew/std), sign +1 first and flipped if IR <= -.04. Zero LLM cost per alpha; batch 1 (40 Slow) queued at the front. Next: hit rate by class/template; repair any sweep alpha with IR >= .06; lower-turnover Y_PLsz_ACC_w12.
- **Oct 7 00:10 (scheduled cycle): repairs of #703370 and the accrual blend.** R_RIG_weekly2 (#703370; IR .075, TVR .259, irtvr .147 vs bar .169 at corr .584 to #601796) was repaired by raising the slow-signal weight: 1.5x gave IR .068 / TVR .200 / irtvr .153 / corr .633 (#704754), 2x gave .063 / .164 / .156 / .647. Turnover fell as planned but IR fell and correlation ROSE (the blocker shares the fundamental leg), so more slow weight is the wrong lever here. Queued instead: gross profit swapped for accruals (R_RIAwk, R_RIAwk_w10). Code of the Y_ accrual blends recovered from the runner; Y_PLsz_ACC_w12 (IR .116, irtvr .138 vs own-bar .144) gets accrual weight 1.6x / 2x (Y_PLsz_ACC_w16/_w20) to cut turnover ~10-20%. Sweep batch 1 (40) waiting behind them; no sweep results yet. New `tools/registry_sync.py` rebuilds alphas/registry.csv|md from all snapshots (230 alphas: 5 submitted, 46 rejected on IR, 26 on correlation, 49 Fast-only, 11 failed, 1 empty, 14 skipped, 78 queued). Laptop offline since 23:42 IST.
- **Oct 7 morning: 2 more submissions (7 total) and the first sweep results.** Overnight the repair queue paid off: R_RIAwk_a15 (reversal + R&D + issuance + accruals at 1.5x, weekly; IR .085, TVR .226, irtvr .179 vs bar .169, corr .54) and Y_PLsz_ACC_w16 (accrual weight 1.6x; IR .118, TVR .624) were auto-submitted. Lessons: swapping the leg shared with the blocker (gross profit -> accruals) raised IR (.075 -> .080) where adding slow weight had lowered it; then more accrual weight cut turnover without IR loss. Abhinav changed the auto-submit rule to "submit everything the portal marks eligible" (runner + CLAUDE.md). Sweep batch 1 (40 "level" alphas on balance-sheet items / assets): best IR .052 (current liabilities), most |IR| < .035, turnover ~.03, mostly low pool correlation. Alone they don't qualify, but they are ideal composite ingredients: 3 composites of the sign-consistent legs (signs checked out of sample) queued first, then sweep batch 2 (next templates). The queue had run empty at 06:42; refilled with 43 Slow jobs.
- **Oct 7 09:10 (cycle): first composite near-miss.** SWC_BS9 (9 balance-sheet legs from sweep batch 1, equal weight): IR .063, turnover .029, pool corr .477 (below .5, so the uncorrelated route is open), OOS1 .108. It needs only IR > .07, so 3 variants (+ accruals leg, 7 legs, 7 legs + accruals) are queued first. A101_054_S (Abhinav's Fast pick): Slow IR .112 but corr .995 to a pool alpha (it IS Alpha #54) -- its accrual/smoothing variants are queued. A101_044_S: IR .067, corr .602 -> accrual-partner repair queued.
- **Oct 7 ~10:00: analysis of our 8 submissions.** Routes: only U_VWAPT_FMOM_w1 (corr .466) qualified through corr <= .5; the other 7 through IR/sqrt(TVR) >= 1.2x the blocker. Ingredients: 7 of 8 contain a short-term reversal leg and 5 of 8 contain the accrual leg (T_LATE_accr_w2, Y_PLsz_ACC_w07/_w16, R_RIAwk_a15, A101_054_acc); only T_COMP7 is a pure slow composite. Robustness: OOS1 (2017-21) holds or improves for the accrual blends (Y_ .13-.14 vs IS .11-.12; R_RIAwk_a15 .077), T_COMP7 .076; weaker for T_LATE_w3 (.031 vs .073, decaying), U_VWAPT_FMOM_w1 (.057) and A101_054_acc (.064 vs .137, best-year share .32). Redundancy: Y_PLsz_ACC_w16 is .94 correlated with Y_PLsz_ACC_w07. Plan: (1) the accrual partner works on any fresh reversal pattern -> 5 more A101 + accrual blends queued; (2) diversify away from reversal+accruals (judged on diversity, and our own accrual submissions will start blocking new ones): balance-sheet composites (SWC_*) and the field sweep; (3) use different slow partners (balance-sheet composite legs) instead of accruals for the next reversal blends.
- **Oct 7 ~10:30: pruned grid search.** Abhinav asked for a systematic search over many combinations. `tools/grid.py` enumerates base pattern x slow partners x weight x neutralisation (384 combos, 339 after static pruning: variable cap, checker, already-submitted pairs), ranks by prior, queues the top 30 (rung 0), and promotes only results with IR >= .065 to their neighbours (successive halving, Hyperband). Trials are counted for a Deflated-Sharpe-style honesty check. Method and sources: `knowledge/grid-search.md`.
- **Oct 7 ~11:00: diversity guard (Abhinav).** #716550 (SWC_BS5_acc, 9th submission) was the 7th submission containing the accrual leg. Leg usage across 9 submissions: accruals 7, late-hour reversal 4, issuance 4, VWAP-gap 4, stock pay 3, FCF 3. New rules: `tools/diversity.py` maps each alpha to its legs, marks legs in >= 3 submissions as saturated and skips queued jobs whose risk is a saturated leg or whose legs match a submission (37 of 77 queued jobs skipped); the grid no longer generates such combos (384 -> 84). The runner now holds (does not auto-submit) any eligible alpha whose daily PnL is > .7 correlated with one of our own submissions and flags it for Abhinav. Next research must come from new data and new patterns (field sweep, untried A101 bases with new partners, new idea families).
- **Oct 7 12:10 (cycle).** No new near-misses; this morning's sweep "level" results all |IR| < .04 (template retired to last place). Queue refilled with sweep batch 3 (40, 6-month change / own-history templates on unused fields) and grid batch 2 (15, unsaturated A101 patterns x balance-sheet partners; 45 grid trials so far). Diversity check: 35 old saturated jobs skipped, all 55 new jobs kept. Runner reload for the .7 own-correlation hold is still waiting for Abhinav's OK on the laptop. Daily Opus round started: 8 alphas on new data only (intraday distribution stats, macro betas, event x stock traits, balance-sheet ratio changes).
- **Oct 7 ~14:30: pipeline audit (Abhinav: "it doesn't look like it is helping").** Yield by source, from the registry: repairs and partner blends of proven legs -> 7 of 9 submissions from ~40 Slow runs (~17%); A101 translation + partner 1/8; sweep composite 1/6; single-field sweep 0 of 88 Slow runs (no result above IR .05); LLM-generated new families (scraped cards, MM/MO cards, new-data cards) 0 of 19 (best .059). Conclusion: the generators that start from scratch are not paying; value comes from combining and repairing proven pieces, which the diversity rule now restricts. Changes: (1) single-field sweep PAUSED and its 32 queued jobs skipped (it burned simulator time); (2) weak-signal ensembles (WSE_) built from the best low-correlation, out-of-sample-positive legs the sweep and LLM did find (solvency/cash-flow changes: interest coverage, cash ratio, cash, dividends, net cash flow; + 2 balance-sheet levels) -- the SWC_BS5_acc route without saturated legs; (3) the grid (combinations of unsaturated A101 patterns with balance-sheet partners) runs next, never tested yet; (4) LLM budget goes to repairing near-misses and designing composites, not blind scouting.
