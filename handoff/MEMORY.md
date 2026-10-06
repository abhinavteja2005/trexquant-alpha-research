# MEMORY: state and playbook

## LATEST (Oct 6, 17:10 IST): RUNNER TAB CLOSED FOR HANDOVER (Plan B)
- The cloud chat ran R.save() (168 jobs: 13 Slow + 25 Fast queued, Y_PLsz_ACC_w07 in flight as sid 698181), stopped its runner and closed the tab. Desktop: open https://www.trexsim.com/trexsim/pysim/alphalist in your group, paste runner/runner.js (NOT localStorage.R3_code), call RUNNER(), check R.counts() and R.cur(), set R3_owner. The repo runner honours each job's j.lb (all queued jobs carry lb <= 300), so the old wlb patch is not needed.

## State at 16:45
- SUBMITTED: 4. T_LATE_accr_w2, T_COMP7, T_LATE_w3 (IR/sqrt(TVR) route) and U_VWAPT_FMOM_w1 (corr .466 route; submitted manually by Abhinav; marked `submitted` in the runner).
- BEST LEAD: anti-correlated partners. Price-reversal blends (IR ~.093) are blocked by #570310 / #604930 (bar .173). Partners whose daily PnL moves AGAINST them cut turnover and correlation:
  fundamental changes (now blocked by our own #695151) and ACCRUALS (corr -.215; replay predicts IR ~.12). Running: Y_PLsz_ACC_w07, Y_PLsz_ACC_w12, Y_PLewm_ACC_w1, Y_VW_ACC_w1. Read them first; if one passes, apply the same partner to the other near-misses (`PX.triage`), and keep scanning for new partners with `PX.pair` against our blocked bases (corr < -.05 and own-corr < .5).
- RETIRED: on/off regime gates (switching raises turnover .05 -> .48); banding with 0/1 flags.
- PORTAL RULES LEARNED TODAY: max lookback 300; cs_indneut needs integer group codes (`industry*0`); ts_*/cs_* need float32 (cast flags as `(close/close)*flag`); `bool - bool` crashes; the 1.2x bar applies against EVERY pool alpha above .5, not just the top one.
- Everything is logged: `alphas/registry.md|csv` (every alpha + status), `reports/RESEARCH_REPORT.md` (changelog), `knowledge/repairs.md`, `knowledge/lessons.md`.

## Earlier state (Oct 6, 10:15)

Read this first, then `handoff/AUTORESEARCHER.md` (the build-and-loop program, including the runner OWNERSHIP handover). It supersedes the Oct 5 handoff. Details: `knowledge/lessons.md`, `alphas/ledger.md`.

## State
- SUBMITTED: 3. Target 100.
  | Tag | Slow IR | TVR | IR/sqrt(TVR) | How it qualified |
  |---|---|---|---|---|
  | T_LATE_accr_w2 | .092 | .328 | .161 | corr .824 to #684336, but irtvr .161 >= 1.2 x .105 |
  | T_COMP7 | .083 | .051 | .366 | corr .786 to #685104, irtvr .366 >= 1.2 x .161 |
  | T_LATE_w3 | .073 | .486 | .105 | corr .506 to #665632, irtvr .105 >= 1.2 x .078 |
  Expressions: `alphas/drafts/oct6-am.json`.
- Runner (Chrome tab, `window.R`) at 10:15 IST: U_ upgrade batch (5 Slow) running, then the local master's 14 cycle-1 Slow jobs (VP_, REG_, ID_, ANOM_), then 25 A101 Fast screens. `alphas/queue/next.json` HAS BEEN LOADED; do not load it again.
- Phase 1 (Fast vs Slow) is DONE. Answer: Fast is a different, noisier simulation. Same alpha's Fast vs Slow daily PnL correlate .34; Fast pool-correlation reads far too low (.48 -> .78). Judge correlation ONLY in Slow. Use Fast at most as a rough IR screen.

## What works (the recipe)
1. The IR/sqrt(TVR) route beats the corr <= .5 route. Almost every decent signal is > .5 correlated with someone. Low turnover wins: a slow composite with TVR .05 has IR/sqrt(TVR) ~.3-.37.
2. Slow accounting composites (z-scored ranks, at_nan2zero sum, ts_fill, lb 400): T_COMP7 = stock-based pay/mktcap, -net issuance (shsout 250d), FCF/mktcap, -accruals, -asset growth, R&D/mktcap, gross profit/assets. IR .083.
3. Reversal base + slow signals at 2-3x weight: the slow part carries most risk, so TVR falls to .3-.5 and IR stays .07-.09. The best base is the "volatile close" last-hour reversal (LATEVOL); the VWAP-gap base (VWAPT) is crowded (#605850, #570310).
4. Every alpha needs a `# Thesis:` and `# Source:` line plus a comment on each line. Use `tools/check_alpha.py`.

## What fails (do not repeat)
- Plain price reversals (VWAP gap, last-hour composite): Slow IR .065-.09 but pool corr .70-.84.
- Reversal + R&D/gross profit blends: IR up to .096 but .70-.74 to #605850 (irtvr .169; need .203).
- Textbook anomalies at daily IR in 2008-2021: 52-week high, BAB, value x quality, EPS drift, sub-industry lead-lag, MAX, high-volume premium, tug of war, realized skew, VIX beta, signed jumps: all |IR| < .03.
- Size+volatility cs_factorneut on a reversal (U_VWAPT_szvo): corr .78 -> .61, but IR .083 -> .051.
- Close variants of our own submissions: .86-.96 correlated with them -> rejected. OUR SUBMISSIONS ARE IN THE POOL.
- Never use trading_days_until_next_earnings_announcement.

## Next directions (ranked)
0. REPAIR near-misses first (`knowledge/repair-playbook.md`, `PX.triage`, log in `knowledge/repairs.md`). Pending repair tests queued at 11:15: U_PRICE2_s3, U_FMOM5_d120, U_FMOM5_lb330, R_PRICE2_band, R_PRICE2_ewm, R_RIG_weekly.
1. NEW slow composites that are NOT T_COMP7: fundamental CHANGES (Piotroski/Soliman: dROA, dCFO/assets, -dleverage, dturnover, dmargin: U_FMOM5 running), ratio-group signals (ebit_yield, cash_to_total_assets_ratio, times_interest_earned_ratio, dividend/payout, sell_and_admin_exp_to_net_sales_ratio, net_debt_to_ebitda), edgar items not yet used. Aim: IR > .072, TVR < .1, corr < .5 to T_COMP7.
2. New reversal bases (not VWAP gap, not LATEVOL) x a NEW slow composite at 2-3x weight.
3. Desktop cycle-1 families (vol-of-vol, coskew, downside beta, trade size, MAX): if any has Slow IR > .03 with low pool corr, use it as a blend partner.
4. Before queueing a blend, paste `runner/px.js` and use `PX.blend` / `PX.own` (reads ~.04-.08 above the portal's number, so it is conservative). Otherwise estimate its corr with our 3 submissions from daily PnL (fetch `/trexsim/pysim/alpha/<id>/?format=json`, `simresdata`); skip anything > .5 unless its irtvr will clear 1.2x.

## Rules
- One runner, one tab. Only `window.R` starts simulations. Never reload or navigate the runner tab; use another tab to browse. If `window.R` is missing, rebuild from `localStorage.R3_code` or `runner/runner.js` (state survives in `localStorage.R3_jobs`).
- Add jobs with `R.add([{tag, base, expr}])`, then set `state:'squeued'` and an explicit `lb` (60 price-only, 300 with 250-day windows, 400 with ts_fill + 250-day delays), then `R.save()`.
- Never edit `R.cfg`, `R.promoteOk` or `R.submitOk`. Auto-submit (approved): Slow IR >= .072, portal-eligible, recency IR >= .04, best-year share <= .5. Never delete submissions. Never type credentials.
- Slow runs take 5-25 min. Keep the Chrome window visible; if `R.lastTick` is > 90 s old, call `R.tick()`.
