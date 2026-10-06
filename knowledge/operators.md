# Trexsim operators (from /trexsim/pysim/api/builtin_operators/, Oct 5)

Alpha code is Python over (stocks x dates) matrices. Comparisons give numpy BOOL matrices:
- `bool - bool` crashes the sim; ts_*/cs_* reject bool (and float64) inputs: they need float32.
- Cast a flag with `(close/close)*(cond)` or, to avoid an extra variable, `(x*0 + 1)*(cond)` with any float32
  matrix x already in the alpha (float32); never `1.0*cond` (float64). Sign: `f = close/close`,
  `f*(x > 0) - f*(x < 0)`. Ternary: `c = f*(cond)`, then `c*a + (1 - c)*b`.
- Python `abs()` works. Avoid `np.*` until one sim confirms it. cs_indneut groups must be integer codes
  (`industry*0` = one all-stock group). Slow lookback max is 300.

## Builtin (32)
| Operator | What it does |
|---|---|
| at_nan2zero(A) / at_zero2nan(A) | NaN/inf -> 0 / 0 -> NaN. Blend with `at_zero2nan(at_nan2zero(a)+at_nan2zero(b))` |
| at_signlog(A) / at_signsqrt(A) | sign-preserving log1p / sqrt |
| cs_rank(A) | cross-sectional rank each day |
| cs_zscore(A) / cs_scale(A) | cross-sectional z-score / scale to [1,2] |
| cs_winsor(A, pct, remove_extreme) | winsorize or remove tails |
| cs_remove_middle(A, pct) | keep only tails (pct=0.8 drops middle 80%) |
| cs_indneut(A, group) | demean within group (industry/subindustry/sector) |
| cs_factorneut(A, [f1,f2], int_factors=[...]) | neutralize to style factors |
| cs_harmonic_mean(A), cs_booksize(A,b), cs_poslimit(A,lim), cs_shrink_balance(A) | portfolio shaping |
| ts_mean, ts_median, ts_sum, ts_std, ts_skew, ts_max, ts_min, ts_harmonic_mean (A, days) | rolling stats |
| ts_rank(A, days) | rank of today within past days, scaled 1..2 |
| ts_zscore(A, days), ts_std_normalized(A, days), ts_norm(A, days) | rolling standardize / center |
| ts_mean_exp(A, days, exp_factor) | exponentially weighted mean |
| ts_corr_binary(A, B, days) | rolling per-stock correlation (beta-like with close_spx/ret1_spx) |
| ts_delay(A, days) | value `days` ago (never negative: forward bias) |
| ts_diff(A, n) | n-th difference over time |
| ts_fill(A) | forward fill (sparse fundamentals) |

## Custom (saved in the user's portal)
delta(A, d), decay_linear(A, d), ts_argmax(A, d), ts_argmin(A, d)

## Tutorial: why Fast != Slow
1. Insufficient Slow lookback (ts_mean(x,30) needs >= 31 days; ts_fill needs the last report inside the lookback).
2. Forward bias (anything that peeks ahead; also data revised later).
3. Corporate-action adjustments on non-dimensionless inputs (raw price/volume/shares levels).
Also: 0 is NOT "no position" (median is subtracted) - use NaN via at_zero2nan.
