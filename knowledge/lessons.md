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

## Oct 5 23:15 (P_/V_ batches; retired master): FAST IS NOT SLOW
- Root cause of the Fast-vs-Slow puzzle: the same alpha's Fast and Slow daily PnL (same dates, 2008-02..2021-12) correlate only 0.34 (P_VWAPT; lag 0, ~0 at other lags). Fast is a different, noisier simulation, not a cheaper copy.
- Fast pool-correlation is systematically too LOW: P_VWAPT .48 -> Slow .78; P_VWAPV_sub .48 -> .84; P_VWAPV_illiq .46 -> .70. Never trust Fast corr; judge correlation only in Slow. Fast is at best a rough IR filter.
- Slow IR of the price-only VWAP-gap reversals is fine (.065-.083, OOS1 .078-.088, best-year <= .25) but they are .70-.84 correlated with the pool and .89-.92 with each other: one crowded family.
- Volatility ideas (RSJ, realized skew, VIX beta, vol shock) have Fast IR < .03; usable only as blend partners. A101 sign is reversed (IR -.051) and pool-correlated (.84).
- To dilute a base with pool corr c to < .5 you need independent partners carrying more risk than the base: c/sqrt(1+w^2) < .5 -> w > 1.25 for c = .78, and partners with IR ~.05 to keep blend IR > .072.
- Queued straight to Slow (lb 300): S_VWAPT_rnd_sbc_gpa, S_VWAPT_rnd_iss_gpa, S_ILLIQ_rnd_iss_gpa (base + 3 equal-weight slow companions).
- Oct 5 23:50: S_VWAPT_rnd_sbc_gpa (equal weights, Slow lb 300): IR .090, TVR .655, OOS1 .099, rw .101, best-year .17, but pool corr .72 to #605850 (a different pool alpha than P_VWAPT's #570310, whose irtvr .169 > ours .111). Its PnL is only .68 correlated with P_VWAPT, so the pool already holds reversal+fundamental blends. Testing double companion weight and less common companions (sbc, iss, fcf).
- The runner stalled ~20 min while the Chrome window was hidden; R.tick() restarted it. Keep the Trexsim window visible overnight.
