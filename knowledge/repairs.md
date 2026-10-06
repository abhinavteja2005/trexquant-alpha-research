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
| Oct 6 | G_VWAPT_mom60, G_RIG_mom60, G_ACCR_mom20, G_ACCR_stop10 | P_VWAPT, S_VWAPT_rnd_iss_gpa, Q_ACCR_AG | self-learned regime gate (replay-screened) | | FAILED: cs_indneut(x, close/close) needs integer group; fix: industry*0. Gates also RETIRED: switching raises TVR .05->.48 | | no |
| Oct 6 | R_PRICE2_ewm | U_PRICE2_szvo | EWMA (ts_mean_exp 10, 0.7) | .093 / .998 / .704@570310 | .085 / .778 / .726@570310 | .097 vs .119 | no |
| Oct 6 | R_PRICE2_band2 | U_PRICE2_szvo | banding with 0/1 flags | .093 / .998 / .704 | .018 / 1.932 / .111 | flags flip: turnover UP | no |
| Oct 6 | U_ILLIQ_rig_szvo | S_ILLIQ_rnd_iss_gpa | size+vol factorneut | .092 / .645 / .701@605850 | .078 / .382 / .626@601796 | .126 vs .169 | no |
| Oct 6 | U_VWAPT_FMOM_w2 | VWAPT + fundamental change | 1:2 blend | | .055 / .341 / .436@595355 (corr < .5!) | IR too low | no -> w1 queued |
| Oct 6 | G_* (4), R_RIG_weekly | see above | gates / weekly | | FAILED: dtype (integer group codes; float32 flags) -> reruns queued | | no |
| Oct 6 | G_VWAPT_mom60b | P_VWAPT | in-code 60-day strategy-momentum gate | .083 / 1.047 / .782@570310 | .071 / 1.135 / .658@604930 | replay predicted .093; real .071 | no |
| Oct 6 | G_ACCR_mom20b | Q_ACCR_AG | in-code 20-day gate | .067 / .051 / .879@567998 | .073 / .481 / .673@673102 | IR up, but TVR .05 -> .48 (switching) | no |
| Oct 6 | G_VWAPT_mom60ind | P_VWAPT | per-industry gate | .083 / 1.047 / .782 | .065 / 1.092 / .682@570310 | worse | no |
| pending | X_PL_FM4_w1/_w05, X_VW_FM5_w1/_w05 | U_PRICE2_szvo / P_VWAPT + U_FMOM5_d120 | anti-correlated blend (PnL corr -.37 / -.18), predicted IR .082-.106 | | | | |
| Oct 6 | U_VWAPT_FMOM_w1 | U_VWAPT_FMOM_w2 | more reversal weight (1:1 instead of 1:2) | .055 / .341 / .436@595355 | .070 / .525 / .466@659499 | eligible (corr < .5) | YES (manual) |
| Oct 6 | X_PL_FM4_w1 | U_PRICE2_szvo + U_FMOM5_d120 | anti-correlated partner 1:1 | .093 / .998 / .704@570310 | .093 / .689 / .637@604930 | .112 vs .173 | no |
| Oct 6 | X_PL_FM4_w05 | U_PRICE2_szvo + U_FMOM5_d120 | partner at 0.5 | .093 / .998 / .704 | .094 / .851 / .737@604930 | .102 vs .173 | no |
| Oct 6 | X_VW_FM5_w1 | P_VWAPT + U_FMOM5_d120 | partner 1:1 | .083 / 1.047 / .782 | .086 / .677 / .799@695151 (own) | .105 vs .116 | no |
| Oct 6 | VWAPV_fcf_iss_w2, RETL_fcf_iss_w2, OVN_fcf_iss_w2 | reversal + fcf + issuance | blend (2x slow weight) | | FAILED (Fast timeout): ts_delay(shsout, 252) — lag 252 not allowed; fix: 250 | | no |
| pending | Y_PLsz_ACC_w07/_w12, Y_PLewm_ACC_w1, Y_VW_ACC_w1 | price reversal + accruals | anti-correlated partner (PnL corr -.215), replay IR .115-.124 | | | | |
| pending | R_RIGwk_k15, R_RIGwk_k2, R_RIGwk_w10, R_RIGwk_w10k15 | R_RIG_weekly2 (#703370) | slow 1.5x / 2x, 10-day reversal, both | .075 / .259 / .584@601796 (irtvr .147, bar .169) | | need TVR <= .197 or corr < .5 | |
| Oct 6 | R_RIGwk_k15 (#704754) | R_RIG_weekly2 | slow part 1.5x | .075 / .259 / .584@601796 | .068 / .200 / .633@601796 | irtvr .153 vs .169; IR < .07 (more slow weight: TVR -23%, IR -9%, corr UP) | no |
| pending | R_RIAwk, R_RIAwk_w10 | R_RIG_weekly2 | swap gross profit for accruals partner (+10-day reversal) | .075 / .259 / .584@601796 | | | |
| Oct 7 | R_RIAwk (#705948, inferred) | R_RIG_weekly2 | gross profit -> accruals | .075 / .259 / .584@601796 | .080 / .248 / .573@601796 | irtvr .161 vs .169 (needs TVR .224) | no |
| pending | R_RIAwk_w10, R_RIAwk_a15, R_RIAwk_r07, R_IAwk_szvo | R_RIAwk | 10-day reversal; accruals 1.5x; reversal 0.7x; drop R&D + vol neutral | .080 / .248 / .573 | | | |
