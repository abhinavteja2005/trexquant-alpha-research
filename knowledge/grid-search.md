# Pruned grid search over alpha combinations (Oct 7)

Why: all 8 submissions are combinations of a fast price/volume pattern with slow characteristics; the space of
such combinations is large (`tools/grid.py --list`: 384, 339 after pruning) but the simulator runs only ~60-100 Slow
jobs a day. So the search must prune before it simulates, and promote only winners.

## Method (tools/grid.py)
| Stage | What | Cost |
|---|---|---|
| Space | 8 base legs (VWAP-gap reversal, Alpha #2/15/26/44/50/53/54) x 8 partner sets (accruals, issuance, balance-sheet composite, current liabilities, pairs) x weight {1, 1.5, 2} x {no, size} neutralisation | free |
| Static pruning | <= 10 variables, `check_alpha` (dtype, windows, look-ahead), skip base/partner pairs already submitted (they now collide with our own submissions), skip tags already tried | free |
| Prior ranking | base IR alone (registry) + diversity bonus for new partner families; at most 4 combos per base per batch | free |
| Rung 0 | top 30 queued as Slow | simulator |
| Promotion (successive halving) | results with Slow IR >= .065 -> `grid.py --expand TAG` generates neighbours (other weights, + one partner, size neutralisation); everything else stops | simulator |
| Optional pre-screen | `PX.blend` in the runner tab predicts a blend's IR from finished parts' PnL (no simulation); used when both parts already ran alone | free |

## Multiple-testing guard
Every generated combo is counted (`alphas/grid_state.json`, "trials"). Selecting the best of many backtests inflates
its Sharpe (Deflated Sharpe Ratio), so the report states trials per submission and we look at OOS1 (2017-21) and
recency IR for every candidate. The portal decides eligibility; these checks tell us which submissions are robust.

## Sources (found via web search; pages not opened from this environment)
- Li, Jamieson, DeSalvo, Rostamizadeh & Talwalkar, "Hyperband: A Novel Bandit-Based Approach to Hyperparameter
  Optimization", JMLR 18(185), 2018: https://jmlr.org/papers/v18/16-558.html (successive halving: allocate the expensive
  evaluation to many configurations cheaply, keep only the best for more budget).
- Bailey & Lopez de Prado, "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and
  Non-Normality", Journal of Portfolio Management 2014: https://papers.ssrn.com/abstract=2460551
- Yu et al., "Generating Synergistic Formulaic Alpha Collections via Reinforcement Learning", KDD 2023:
  https://arxiv.org/abs/2306.12964 (mine alphas for how they combine, not one by one; code: github.com/yutiansut/alphagen)
- Kakushadze, "101 Formulaic Alphas", 2016: https://arxiv.org/abs/1601.00991 (base legs)
