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

## 7. Methods borrowed from research
Man Group AlphaGPT (idea -> implement -> evaluate pod, same bar as humans, idea/code consistency checks), AlphaAgent
(originality and complexity regularisers), RD-Agent(Q) (bandit over directions, cost < $10 per run), Alpha Jungle
(avoid overused formula parts), QuantaAlpha (repair the weak step of a near-miss), the WorldQuant BRAIN skill
(self-correlation on daily PnL before submitting), Novy-Marx & Velikov (banding), Garleanu & Pedersen (partial
trading). Links: `knowledge/autoresearch-survey.md`, `knowledge/repair-playbook.md`.

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
