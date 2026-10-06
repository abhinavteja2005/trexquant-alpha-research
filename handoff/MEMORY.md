# MEMORY: state and playbook (updated Oct 6, 10:15 IST by the cloud chat)

Read this first. It supersedes the Oct 5 handoff. Details: `knowledge/lessons.md`, `alphas/ledger.md`.

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
1. NEW slow composites that are NOT T_COMP7: fundamental CHANGES (Piotroski/Soliman: dROA, dCFO/assets, -dleverage, dturnover, dmargin: U_FMOM5 running), ratio-group signals (ebit_yield, cash_to_total_assets_ratio, times_interest_earned_ratio, dividend/payout, sell_and_admin_exp_to_net_sales_ratio, net_debt_to_ebitda), edgar items not yet used. Aim: IR > .072, TVR < .1, corr < .5 to T_COMP7.
2. New reversal bases (not VWAP gap, not LATEVOL) x a NEW slow composite at 2-3x weight.
3. Desktop cycle-1 families (vol-of-vol, coskew, downside beta, trade size, MAX): if any has Slow IR > .03 with low pool corr, use it as a blend partner.
4. Before queueing a blend, estimate its corr with our 3 submissions from daily PnL (fetch `/trexsim/pysim/alpha/<id>/?format=json`, `simresdata`); skip anything > .5 unless its irtvr will clear 1.2x.

## Rules
- One runner, one tab. Only `window.R` starts simulations. Never reload or navigate the runner tab; use another tab to browse. If `window.R` is missing, rebuild from `localStorage.R3_code` or `runner/runner.js` (state survives in `localStorage.R3_jobs`).
- Add jobs with `R.add([{tag, base, expr}])`, then set `state:'squeued'` and an explicit `lb` (60 price-only, 300 with 250-day windows, 400 with ts_fill + 250-day delays), then `R.save()`.
- Never edit `R.cfg`, `R.promoteOk` or `R.submitOk`. Auto-submit (approved): Slow IR >= .072, portal-eligible, recency IR >= .04, best-year share <= .5. Never delete submissions. Never type credentials.
- Slow runs take 5-25 min. Keep the Chrome window visible; if `R.lastTick` is > 90 s old, call `R.tick()`.
