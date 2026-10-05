# Lessons (append-only; newest at the bottom)

## Oct 5 afternoon (~60 Fast alphas)
- The correlation pool is all participants' submissions; plain reversal ideas are 0.5-0.85 correlated with what's already in it.
- Daily IR comes mostly from short-term reversal: intraday composite c_intra .090, last-hour return .069, VWAP gap .076.
- cs_factorneut(x, [cs_rank(ret1), cs_rank(ret5)]) leaves IR ~0.
- Slow fundamentals: IR/sqrt(TVR) .12-.20 but daily IR < .045 (R&D/mktcap .043, GPA .036, FCF .028, issuance .024).
- decay_linear 10 kills reversal IR (.090 -> .037). Industry-level signals are cancelled by industry neutralization.
- Blend recipe (reversal + 2 slow companions) keeps Fast IR ~.075-.09 and lowers TVR and correlation.

## Oct 5 night (runner v3)
- With the earnings companion: INTRA w3 .076, VWAPV .076, RETL .075 (Fast-eligible via override); OVN .060, D3 .063, RANGE .067.
- INTRA+rnd+sbc w3: Fast .082 but corr .565 (override failed).
- FAST != SLOW: c3_rnd_earn Fast .094/corr .56 -> Slow .082/corr .688. VWAPV_rnd_sbc_w2 Fast .078/corr .476 -> Slow .052 (lookback 140). Blends with ts_fill fundamentals are suspect in Slow until diagnosed.
- Dropped trading_days_until_next_earnings_announcement (possible look-ahead).

## Oct 5 late (local master): from the official tutorial and operator API
- Tutorial's three causes of Fast != Slow: (1) Slow lookback too short for the longest window/ts_fill gap, (2) forward bias, (3) corporate-action adjustments on non-dimensionless inputs (raw price/volume/shares). Hypothesis for VWAPV_rnd_sbc_w2 (Slow lb 140): quarterly ts_fill fundamentals may have no report inside 140 days for some names -> test lb 300 in Phase 1.
- 0 is not "no position" (median is subtracted): use at_zero2nan. Blend with at_zero2nan(at_nan2zero(a)+at_nan2zero(b)).
- Operator list: knowledge/operators.md (32 builtins + delta, decay_linear, ts_argmax, ts_argmin). No covariance/log/sign builtins: use ts_corr_binary, at_signlog, (x>0)-(x<0).
- Expressions cannot be read back from the runner through Claude in Chrome (privacy filter on URLs): alphas/drafts/*.json is the expression store; tools/ledger_sync.py joins metrics by tag.
