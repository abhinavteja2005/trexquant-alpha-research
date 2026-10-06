# Repair log (append one row per repaired variant; used to choose techniques by measured success)

| Date | Variant | Parent | Technique | Parent IR / TVR / corr@id | Variant IR / TVR / corr@id | irtvr vs bar | Submitted |
|---|---|---|---|---|---|---|---|
| Oct 6 | S_VWAPT_rnd_sbc_gpa_w2 | S_VWAPT_rnd_sbc_gpa | slow part 2x | .090 / .655 / .72@605850 | .085 / .463 / .695@605850 | .125 vs .203 | no |
| Oct 6 | T_LATE_w3 | S_LATEVOL_sbc_iss_fcf_w2 | slow part 3x | .075 / .540 / .527@570604 | .073 / .486 / .506@665632 | .105 vs .078 | YES |
| Oct 6 | T_LATE_accr_w2 | S_LATEVOL_sbc_iss_fcf_w2 | + accruals signal | .075 / .540 / .527 | .092 / .328 / .824@684336 | .161 vs .105 | YES |
| Oct 6 | T_LATE_s3_w2 | S_LATEVOL_sbc_iss_fcf_w2 | ts_mean 3 smoothing | .075 / .540 | .061 / .439 / .959 own | - | no |
| Oct 6 | S_BL1_subind | S_VWAPT_rnd_sbc_gpa | sub-industry neutral | .090 / .655 / .72 | .088 / .695 / .715 | .106 vs .203 | no |
| Oct 6 | U_VWAPT_szvo | P_VWAPT | size+vol factorneut | .083 / 1.047 / .782@570310 | .051 / 1.010 / .612@570310 | - | no |
| Oct 6 | U_PRICE2_szvo | S_ALLPOS_price (minus LATEVOL) | size+vol factorneut | .092 / .951 / .753@604930 | .093 / .998 / .704@570310 | .093 vs .119 | no |
| Oct 6 | U_PRICE2_w10 | U_PRICE2_szvo | 5 -> 10-day windows | .093 / .998 / .704 | .080 / .848 / .610@570310 | .087 vs .119 | no |
| Oct 6 | U_VWAPT_rig_szvo | S_VWAPT_rnd_iss_gpa | size+vol factorneut | .096 / .741 / .739@605850 | .099 / .742 / .701@605850 | .115 vs .203 | no |
| pending | U_PRICE2_s3, R_PRICE2_band, R_PRICE2_ewm, R_RIG_weekly | see playbook | 3-day mean, banding, EWMA, weekly rebalance | | | | |
| Oct 6 | U_PRICE2_s3 | U_PRICE2_szvo | ts_mean 3 smoothing | .093 / .998 / .704@570310 | .072 / .545 / .703@570310 | .097 vs .119 | no |
| Oct 6 | U_FMOM5_d120 | U_FMOM5 (empty) | 120-day changes, lb 260 | empty | .028 / .064 / .492@595355 | IR too low | no |
| Oct 6 | R_PRICE2_band | U_PRICE2_szvo | banding | | CRASHED (bool - bool) -> rerun R_PRICE2_band2 | | no |
| Oct 6 | U_FMOM5_lb330 | U_FMOM5 | lookback 330 | | REJECTED by portal: max lookback 300 | | no |
| pending | G_VWAPT_mom60, G_RIG_mom60, G_ACCR_mom20, G_ACCR_stop10 | P_VWAPT, S_VWAPT_rnd_iss_gpa, Q_ACCR_AG | self-learned regime gate (replay-screened) | | | | |
