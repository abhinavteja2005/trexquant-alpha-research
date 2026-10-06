# Crash forensics (Oct 6)

All 12 undiagnosed crashes from `alphas/crashes/pending.json`, root-caused and mapped to checker rules.

| Tag | Stage | Class | Root cause (line) | Rule added | Fixed form | Origin (tool/file) |
|---|---|---|---|---|---|---|
| VWAPV_fcf_iss_w2 | FAILED (Fast timeout) | timeout/heavy | `ts_delay(shsout, 252)` -- lag 252 not in allowed set | Rule A: ts_delay lag check | Change 252 to 250 | crashes/exprs.json |
| RETL_fcf_iss_w2 | FAILED (Fast timeout) | timeout/heavy | `ts_delay(shsout, 252)` -- lag 252 not in allowed set | Rule A: ts_delay lag check | Change 252 to 250 | crashes/exprs.json |
| OVN_fcf_iss_w2 | FAILED (Fast timeout) | timeout/heavy | `ts_delay(shsout, 252)` -- lag 252 not in allowed set | Rule A: ts_delay lag check | Change 252 to 250 | crashes/exprs.json |
| Q_FROG | FAILED (portal error at loading_data) | dtype | `ts_mean(ret1 < 0, 250)` -- bool flag to ts_mean | Existing: bool_errors | Cast with `(close/close)*(ret1 < 0)` | oct6-night.json |
| U_FMOM5 | EMPTY (lookback bug) | lookback | Runner bug ignored j.lb; lb=140 made ts_delay(x,250) all NaN | None (runner bug, patched) | Same expression with wlb=300 | oct6-upgrades.json |
| U_FMOM5_lb330 | FAILED (portal: lookback > 300) | lookback | Queued with lb=330; portal max is 300 | Rule C: lookback warning (warns, not errors) | Use lb=300 (cap at portal max) | crashes/exprs.json |
| R_PRICE2_band | FAILED (bool - bool crash at loading_data) | dtype | `at_zero2nan(hl - hs)` where hl, hs are bool flags | Existing: bool_errors | Use `(q*0+1)*(cond)` float32 cast | crashes/exprs.json |
| R_RIG_weekly | FAILED (bool to ts_delay) | dtype | `ts_delay(f0, 1)` where f0 is a bool comparison | Existing: bool_errors | Cast f0 with `(day_of_the_week*0+1)*(cond)` | crashes/exprs.json |
| G_VWAPT_mom60 | FAILED (cs_indneut needs integer group) | group-code | `cs_indneut(x, one)` where `one = close/close` (float32, not integer) | Rule B: cs_indneut group check | Use `industry*0` instead of `close/close` | crashes/exprs.json |
| G_RIG_mom60 | FAILED (cs_indneut needs integer group) | group-code | `cs_indneut(x, one)` where `one = close/close` | Rule B: cs_indneut group check | Use `industry*0` instead of `close/close` | crashes/exprs.json |
| G_ACCR_mom20 | FAILED (cs_indneut needs integer group) | group-code | `cs_indneut(x, one)` where `one = close/close` | Rule B: cs_indneut group check | Use `industry*0` instead of `close/close` | crashes/exprs.json |
| G_ACCR_stop10 | FAILED (cs_indneut needs integer group) | group-code | `cs_indneut(x, one)` where `one = close/close` | Rule B: cs_indneut group check | Use `industry*0` instead of `close/close` | crashes/exprs.json |
