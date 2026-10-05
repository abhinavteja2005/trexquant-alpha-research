# Alpha draft file format (shared by Writer, critic, tools and Operator)

One alpha per file: `alphas/drafts/<cycle>/<TAG>.py`. TAG = `[A-Z0-9_]+`, unique across `alphas/ledger.md` and all drafts.

```
# Tag: VOLSKEW_L_w20
# Family: INTRA-SKEW                      (short family label, used for saturation stats)
# Base: VOLSKEW                           (runner `base`; variants of one idea share a base)
# Thesis: Stocks whose last-hour return skew is high are lottery-like and underperform next day (one sentence).
# Source: https://... (real URL; add "(search-verified)" if it was seen in search results but not opened)
# Horizon: 1-5d   Sign: short high skew
# VARS: skew_last_hour, volume_last_hour  (every DATA variable used, comma-separated, <= 10)
s = ts_mean(skew_last_hour, 20)            # 20-day mean of last-hour return skew
alpha = -cs_rank(s)                         # short high-skew names; final value is the alpha
```

Rules (enforced by `tools/lint.py`; the critic rejects on any failure):
1. Header lines Tag, Family, Base, Thesis, Source, VARS present; Source starts with `http`.
2. Every non-blank code line has a trailing `# comment`.
3. VARS lists <= 10 data variables, and every lower-case identifier in the code that is not a local name, a known operator or a Python keyword appears in VARS.
4. Integer windows passed to ts_* / decay / delta operators are in {3, 5, 10, 20, 40, 60, 120, 250} (252 tolerated only for annual lags).
5. Banned: `trading_days_until_next_earnings_announcement` (look-ahead), any negative shift / future index, raw price or volume levels as the signal (use ratios, returns, ranks, z-scores).
6. The last code line assigns `alpha = ...` (UNVERIFIED portal convention; the Operator confirms it against an existing runner job in cycle 1 and fixes the convention here if it differs).

## Syntax status (Oct 5)
- Known from runner history: cs_rank, ts_fill, cs_factorneut(x, [..]), at_nan2zero, np.where, z-scoring, ts_mean-style `op(x, window)`. Saved custom ops: delta, decay_linear, ts_argmax, ts_argmin.
- Known variable names: vwap_last_hour, earnings_yield, ev_to_t12m_ebit, price_to_book_ratio. Other names are best guesses until `knowledge/variables.json` is exported from the portal (Operator task, cycle 1).
- The in-browser packet validator checks every identifier against the portal's real variable list (`R.varset`) before anything is queued, so a wrong guess costs no simulation.
