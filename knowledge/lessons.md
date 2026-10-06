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

## Oct 6 morning (overnight Slow results)
- Reversal+fundamental blends: Slow IR .085-.096 (OOS1 up to .116) but all collide with pool #605850 (corr .70-.74, its irtvr .169). Dead end unless irtvr >= .203.
- Best near miss: S_LATEVOL_sbc_iss_fcf_w2 (volatile-close reversal + stock pay + issuance + FCF at 2x): IR .075, corr .527 to #570604 (irtvr .099; ours .102, need .119). Variants queued (w3, 3-day smoothing, +accruals, sub-industry).
- Slow fundamental composites have tiny turnover, so they pass the IR/sqrt(TVR) test (COMP5 .226 vs .169x1.2) but IR is .05. Accruals+asset growth: IR .067, OOS1 .095, irtvr .298, but corr .879 to #567998 (irtvr .273). Bigger composites queued (COMP7, COMP5b, COMP7_sub).
- Textbook anomalies are dead or negative in-sample 2008-2021 at daily IR: 52-week high, BAB, value x quality, EPS drift, sub-industry lead-lag, MAX, high-volume premium, tug of war (all |IR| < .03).
- Oct 6 ~09:00: FIRST 3 SUBMISSIONS: T_LATE_w3, T_LATE_accr_w2, T_COMP7. All pass through the IR/sqrt(TVR) >= 1.2x route, not corr <= .5. Recipe: make low-turnover slow signals carry most of the risk (2-3x weight or alone) and use a reversal base that is not the crowded VWAP gap.
- Our own submissions are now in the pool: new variants of the same recipe hit them at .86-.96. Each new alpha must differ from T_COMP7 (irtvr .366), T_LATE_w3 and T_LATE_accr_w2 too.
- Upgrade batch U_ queued: size+volatility factor-neutralization of the best rejected blends (cs_factorneut with sz, vo), and a fundamental-CHANGE composite (Piotroski/Soliman: dROA, dCFO/assets, -dleverage, dasset turnover, dgross margin) alone and with the VWAPT reversal.
- Oct 6 10:40: U_PRICE2_szvo (P_VWAPT + heavy-volume late-day composite, size/vol cs_factorneut): IR .093, TVR .998, corr .704 to #570310 (irtvr .099 -> need .119). Neutralizing size+vol on the 2-signal price blend kept IR (.092 -> .093) and cut corr (.753 -> .704); on P_VWAPT alone it cost IR (.083 -> .051).
- Plan to beat #570310: (a) U_PRICE2_w10 (10-day windows) and U_PRICE2_s3 (3-day position average) for lower TVR; (b) when U_FMOM5 finishes, PX.blend([['U_PRICE2_szvo',1],['U_FMOM5',w]]) for w in .5-1.5; if PX predicts IR >= .085 and own-corr < .55, write it as one alpha (variable cap: drop the range term from p2 and keep 2-3 FMOM pieces). `subindustry` counts as a variable.
- The runner tab title is now "RUNNER - do not reload". The alphalist table in that tab does not refresh; view results in a different tab.
- Oct 6 11:00 BUG FOUND: the live runner in the tab is an older build that IGNORES a job's preset j.lb: Slow lookback came from R.lookback(expr) = 140 for any ts_fill alpha (260 cap otherwise). In Slow mode an alpha only sees `lookback` days of data, so ts_delay(x, 250) was ALWAYS NaN at lb 140. Consequences: the issuance (shsout 250d) and asset-growth parts of every filing blend were inactive, including in T_COMP7, T_LATE_w3 and T_LATE_accr_w2 (their comments describe issuance, but it contributed nothing). U_FMOM5 came back empty (IR 0, TVR 0).
- Fix (live, 11:00): R.lookback is wrapped to return j.wlb when a queued job has it; all queued Slow jobs got wlb = max(runner rule, min(j.lb, 330)). Lookbacks above 260 are untested on the portal; Q_FROG twice failed at "loading_data" (cause unknown). If 330 fails, use 260 with 120-day changes instead (U_FMOM5_d120).
- If the runner is ever rebuilt, use runner/runner.js from the repo (respects j.lb), NOT localStorage.R3_code (the old build).
- Oct 6 11:45: portal maximum Slow lookback = 300 ("Lookback cannot exceed 300"; U_FMOM5_lb330 rejected). `bool - bool` crashes a sim at "loading_data" (R_PRICE2_band; likely Q_FROG too): cast flags with 1.0*(...).
- U_FMOM5_d120 (half-year fundamental changes, lb 260): IR .028, TVR .064, corr .49 (< .5!). Weak but uncorrelated: a candidate blend partner. U_PRICE2_s3 (3-day mean): IR .072, TVR .545, irtvr .097 vs bar .119, corr .703: smoothing alone is not enough.
- Self-learned regime gates (Abhinav's idea): replay on real PnL shows reversal PnL has almost no streakiness (10-day block autocorr .03-.08), so stop-losses hurt reversal alphas, but a 60-day strategy-momentum switch helped P_VWAPT (.083 -> .093) and S_VWAPT_rnd_iss_gpa (.096 -> .101), and stop10re5 / mom20 helped accruals (.067 -> .074 / .076), each in BOTH halves. Queued G_ jobs to test in Slow.
- Oct 6 14:00: dtype rules: cs_indneut needs INTEGER group codes (use industry*0 for one all-stock group); ts_*/cs_* need float32 (cast flags with (close/close)*flag). All 4 gates and the weekly rebalance failed on these; reruns queued (G_*b, G_VWAPT_mom60ind, R_RIG_weekly2).
- U_VWAPT_FMOM_w2 (VWAPT reversal + 5 fundamental CHANGES at 1:2): pool corr .436 (< .5) at IR .055: the first genuinely uncrowded blend. 1:1 version queued to lift IR. EWMA repair: IR .085, irtvr .097 (bar .119). 0/1 banding raises turnover (1.93). Desktop's VP_ volatility ideas: IR <= .023 but corr .17-.50.
- Oct 6 14:50: GATES DON'T PAY HERE. In-code gates ran after the dtype fix: G_ACCR_mom20b IR .067 -> .073 (as replayed) but TVR .05 -> .48 (each switch liquidates/re-enters the whole book), killing the IR/sqrt(TVR) route; G_VWAPT_mom60b .071 vs replay .093 (the in-code shadow return differs from the portal's PnL). Stop testing on/off gates on fast alphas; for slow alphas they destroy the low-turnover advantage.
- Oct 6 14:45 KEY DISCOVERY: fundamental-CHANGE signals are NEGATIVELY correlated with our reversal blends (U_FMOM5_d120 vs U_PRICE2_szvo -.37; vs R_PRICE2_ewm -.40; U_VWAPT_FMOM_w2 vs U_PRICE2_szvo -.15) and ~0 with our submissions. PX.blend predicts PRICE2 + 0.5 x FMOM IR .106, 1:1 IR .096. Queued X_PL_FM4_w1/_w05 and X_VW_FM5_w1/_w05 (10 variables each). This "anti-correlated partner" route is the most promising lead.

## Oct 6 (local master): static dtype checks
- tools/check_alpha.py now rejects `bool - bool` and ts_*/cs_* applied to a true/false flag (portal crashes). Run over all drafts it flags only Q_FROG (`ts_mean` of a flag at line 5), which explains its two "loading_data" failures.
- A101_012 and A101_030 used `(x>0)-(x<0)` (bool - bool) and A101_009 summed bool flags; fixed in alphas/drafts/a101.json with float32 casts. The copies already loaded into the runner are the OLD code: expect 012/030 to crash; re-queue the fixed versions under new tags (A101_012b, A101_030b) once the runner is ours.
- Float32 cast without an extra variable: `(x*0 + 1)*(cond)` with any float32 matrix x already in the alpha.
- repair.py: Slow lookback = nested window/lag need (+70 ts_fill, +20), capped at 300; band uses a weighted book (0/1 flags raised TVR to 1.93).
- Oct 6 15:40: 4th SUBMISSION, U_VWAPT_FMOM_w1 (VWAPT late-day reversal + 5 one-year fundamental changes, 1:1; lb 300): Slow IR .070, TVR .525, corr .466 (uncorrelated route), OOS1 .057, recency .062, best-year .18. Submitted manually by Abhinav (the runner's own bar is IR >= .072). The fundamental-change family is now in the pool, so new FMOM blends will be compared with it.
- X_PL_FM4_w1 (price blend + 4 half-year changes, 1:1): IR .093 (replay predicted .096), TVR .998 -> .689, corr .704 -> .637 but now to #604930 (bar .173). Anti-correlated partners cut turnover and correlation as predicted, not yet enough for this base.
- Oct 6 16:40: the portal requires the 1.2x IR/sqrt(TVR) bar against EVERY pool alpha above .5 correlation, not just the top one (X_PL_FM4_w1 is .758 to our own #695151 AND .637 to #604930, whose bar is .173). Our 4th submission (#695151) now blocks further fundamental-change blends (X_VW_FM5_w1 .799; PX own-corr .62-.68 for FMOM partners).
- New partner scan (PX.pair vs U_PRICE2_szvo over all finished alphas): accruals (Q_ACCR_AG) corr -.215; replay U_PRICE2_szvo + accruals: w.5 IR .122, w1 .123, w1.5 .115, own-corr <= .47. Queued Y_ blends (10 variables).

## Oct 6 (cloud session): crash forensics
- 12 crashes diagnosed. Three new checker rules added: (A) ts_delay lag must be in {1,2,3,4,5,10,20,40,60,120,250}; (B) cs_indneut group must use industry/subindustry/sector; (C) warn if min lookback > 300.
- ts_delay(shsout, 252) caused 3 Fast timeouts (VWAPV/RETL/OVN_fcf_iss_w2). Lag 252 is not 250 — always use allowed windows.
- Gate template `cs_indneut(x, close/close)` crashed all 4 G_ alphas: float32 is not an integer group code. Fix: `cs_indneut(x, industry*0)`. The repair-playbook gate template has been updated.
- Regime gates RETIRED as a technique: on/off switching raises TVR from .05 to .48, destroying the IR/sqrt(TVR) route (G_ACCR_mom20b). In-code gates also underperform replay predictions (G_VWAPT_mom60b: predicted .093, real .071).
