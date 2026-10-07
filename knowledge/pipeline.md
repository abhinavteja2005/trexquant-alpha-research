# The TrexQuant auto-researcher: full pipeline (Oct 7) and how it compares with published systems

## 1. Pipeline, end to end
```
            CLOUD (Opus master, every 3 h, credit)                                LAPTOP (Sonnet operator, every 30 min)
 results ─▶ 1 SYNC     ledger_sync / registry_sync: every alpha + metrics          ◀── snapshot of runner jobs (IR, TVR, corr, blocker, OOS)
            2 DIVERSITY diversity.py: legs of our submissions; saturated legs
                        (>= 3 uses) are banned; skip queued look-alikes
            3 REPAIR   near-misses (IR >= .065, not saturated) -> <= 3 variants:
                        cut turnover / drop the leg shared with the blocker / add partner
            4 COMBINE  weak-signal ensembles (WSE_) + grid.py (base x partner x
                        weight x neutralisation, successive-halving promotion)
            5 GENERATE sweep.py (fields x templates; paused) / LLM Scout-Writer
                        + blind Critic (once a day at most)
            6 FILTER   check_alpha (dtype, windows, look-ahead, <= 10 vars),
                        originality.py, diversity.py
            7 QUEUE    next.json (jobs) + ops.json (front order, skips, PX requests) ──▶ loads queue at the front, applies skips
                                                                                         RUNNER (JS in Chrome): one Slow sim at a time
                                                                                         auto-submit if portal-eligible AND own-PnL corr <= .7
            8 RECORD   registry, repairs.md, lessons.md, RESEARCH_REPORT changelog       flags ELIGIBLE / HELD for Abhinav
```

## 2. Comparison with published auto-researchers (survey: `knowledge/autoresearch-survey.md`)
| Idea in the literature | Where it lives here | Match |
|---|---|---|
| Idea -> implement -> evaluate pod with human-grade acceptance (Man Group AlphaGPT; Alpha-GPT 2023) | Scout -> Writer -> blind Critic; the portal is the evaluator (same rule as for humans) | yes |
| Results fed back into the next hypotheses (Alpha-GPT review step; RD-Agent(Q) feedback with a task-code-result knowledge base) | only for repairs; the LLM Writer does NOT see the result table when proposing new families | **gap**: open loop, and LLM families went 0/19 |
| Originality / redundancy regulariser (AlphaAgent; Alpha Jungle subtree avoidance; RD-Agent dedup) | originality.py (code), diversity.py (legs), runner hold at own-PnL corr > .7 | yes |
| Hypothesis-to-code alignment and complexity control (AlphaAgent) | blind Critic; check_alpha; <= 10 variables | partly (no explicit complexity score) |
| Bandit choosing what to work on (RD-Agent(Q) Thompson sampling) | bandit.py exists (families) but the slot split between repair / grid / composite / LLM is set by hand | **gap** |
| Search guided by backtest results (Alpha Jungle MCTS; AlphaGen RL; QuantaAlpha evolution: fix the weak step of a near-miss) | repairs (fix the weak step), grid --expand (local search around winners) | partly: a few dozen evaluations a day, not thousands |
| Mine alphas for how they combine (AlphaGen "synergistic collections"; Kakushadze "combine a billion alphas") | partner blends, SWC composites, weak-signal ensembles | yes |
| Cheap proxy before the expensive evaluation (successive halving; wq-alpha-research PnL pre-screen) | static filters; PX.blend in-page prediction (rarely used) | partly |
| Multiple-testing honesty (Deflated Sharpe) | trial counts, OOS1 and recency on every result | yes |

## 3. Why ours differs, and what that implies
- The published systems evaluate thousands of formulas a day on cheap local backtests; ours gets ~60-100 portal
  simulations a day, so RL/MCTS-style search is not affordable and pruning before simulation matters most.
- Their objective is IC/Sharpe; ours is pass/fail against a pool of 500+ other participants' alphas plus our own
  diversity rule, so a good alpha can still be worthless here. Measured yield (Oct 7): combining and repairing proven
  pieces 8/9 submissions; blind generation (sweep 0/88, LLM families 0/19).
- Next steps toward the published designs: (1) close the loop: give the LLM Writer the results table (what failed,
  why, which data are unused) as RD-Agent and Alpha-GPT do; (2) let a bandit split simulator slots across sources by
  measured yield; (3) use PX.blend to pre-screen blends before simulating them.
