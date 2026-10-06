# Alpha registry (every alpha, good or bad)

Machine-readable copy: `alphas/registry.csv`. Regenerate from the runner each cycle (`tools/ledger_sync.py`).
Expressions: `expr_file` points to `alphas/drafts/*.json`; others live in the runner (`localStorage.R3_jobs`) and `ideas/backlog.md`.

Status counts (Oct 6, 14:50 IST): FAST ONLY (not Slow-tested): 49, REJECTED: IR below .072: 29, QUEUED (Fast screen): 25, REJECTED: correlation (IR ok): 17, QUEUED (Slow): 16, SKIPPED (look-ahead variable dropped): 12, FAILED (cs_indneut needs integer group): 4, FAILED (Fast timeout): 3, SUBMITTED: 3, FAILED (portal error): 1, EMPTY (lookback bug; rerun queued): 1, FAILED (portal: lookback > 300): 1, FAILED (bool - bool crash): 1, FAILED (bool to ts_delay: needs float32): 1, RUNNING: 1

Not in the table: ~60 Fast-only alphas from Oct 5 afternoon (pre-runner; e.g. c_intra Fast IR .090 / corr .649, c3_rnd_earn Fast .094 -> Slow .082 / corr .688), summarised in `knowledge/lessons.md` and `alphas/ledger.md`.

| Tag | Family | Batch | Status | Slow IR | TVR | IR/sqrt(TVR) | Corr @ blocker | Bar | OOS1 | Fast IR / corr |
|---|---|---|---|---|---|---|---|---|---|---|
| INTRA_rnd_earn_w3 | INTRA | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.076 / 0.647 |
| VWAPV_rnd_earn_w2 | VWAPV | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.076 / 0.656 |
| RETL_rnd_earn_w2 | RETL | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.075 / 0.594 |
| OVN_rnd_earn_w2 | OVN | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.06 / 0.573 |
| D3_rnd_earn_w2 | D3 | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.063 / 0.673 |
| RANGE_rnd_earn_w2 | RANGE | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.067 / 0.619 |
| INTRA_rnd_sbc_w3 | INTRA | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.082 / 0.565 |
| VWAPV_rnd_sbc_w2 | VWAPV | Oct 5 21:00 runner v3 blend grid | REJECTED: IR below .072 | 0.052 | 0.583 | 0.068 | 0.6 @631112 | 0.145 | 0.056 | 0.078 / 0.476 |
| RETL_rnd_sbc_w2 | RETL | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.071 / 0.508 |
| OVN_rnd_sbc_w2 | OVN | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.046 / 0.509 |
| D3_rnd_sbc_w2 | D3 | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.055 / 0.7 |
| RANGE_rnd_sbc_w2 | RANGE | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.063 / 0.603 |
| INTRA_fcf_earn_w3 | INTRA | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| VWAPV_fcf_earn_w2 | VWAPV | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| RETL_fcf_earn_w2 | RETL | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| OVN_fcf_earn_w2 | OVN | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| D3_fcf_earn_w2 | D3 | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| RANGE_fcf_earn_w2 | RANGE | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| INTRA_sbc_earn_w3 | INTRA | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| VWAPV_sbc_earn_w2 | VWAPV | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| RETL_sbc_earn_w2 | RETL | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| OVN_sbc_earn_w2 | OVN | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| D3_sbc_earn_w2 | D3 | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| RANGE_sbc_earn_w2 | RANGE | Oct 5 21:00 runner v3 blend grid | SKIPPED (look-ahead variable dropped) |  |  |  |  |  |  |  |
| INTRA_gpa_iss_w3 | INTRA | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.067 / 0.718 |
| VWAPV_gpa_iss_w2 | VWAPV | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.061 / 0.706 |
| RETL_gpa_iss_w2 | RETL | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.071 / 0.638 |
| OVN_gpa_iss_w2 | OVN | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.053 / 0.683 |
| D3_gpa_iss_w2 | D3 | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.067 / 0.646 |
| RANGE_gpa_iss_w2 | RANGE | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.065 / 0.697 |
| INTRA_fcf_iss_w3 | INTRA | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.053 / 0.71 |
| VWAPV_fcf_iss_w2 | VWAPV | Oct 5 21:00 runner v3 blend grid | FAILED (Fast timeout) |  |  |  |  |  |  |  |
| RETL_fcf_iss_w2 | RETL | Oct 5 21:00 runner v3 blend grid | FAILED (Fast timeout) |  |  |  |  |  |  |  |
| OVN_fcf_iss_w2 | OVN | Oct 5 21:00 runner v3 blend grid | FAILED (Fast timeout) |  |  |  |  |  |  |  |
| D3_fcf_iss_w2 | D3 | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.058 / 0.721 |
| RANGE_fcf_iss_w2 | RANGE | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.051 / 0.715 |
| INTRA_rnd_fcf_w3 | INTRA | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.084 / 0.556 |
| VWAPV_rnd_fcf_w2 | VWAPV | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.076 / 0.548 |
| RETL_rnd_fcf_w2 | RETL | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.071 / 0.505 |
| OVN_rnd_fcf_w2 | OVN | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.045 / 0.512 |
| D3_rnd_fcf_w2 | D3 | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.056 / 0.647 |
| RANGE_rnd_fcf_w2 | RANGE | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.065 / 0.57 |
| P_CI_s3 | CI | Oct 5 22:00 price/intraday | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.054 / 0.598 |
| P_CI_volcond | CI | Oct 5 22:00 price/intraday | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.091 / 0.612 |
| P_CI_lowvol | CI | Oct 5 22:00 price/intraday | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.07 / 0.443 |
| P_VWAPV_s3 | VWAPV | Oct 5 22:00 price/intraday | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.058 / 0.379 |
| P_VWAPT | VWAPT | Oct 5 22:00 price/intraday | REJECTED: correlation (IR ok) | 0.083 | 1.047 | 0.081 | 0.782 @570310 | 0.119 | 0.085 | 0.098 / 0.48 |
| P_RETL_small | RETLS | Oct 5 22:00 price/intraday | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.049 / 0.441 |
| P_VWAPV_sub | VWAPV | Oct 5 22:00 price/intraday | REJECTED: IR below .072 | 0.065 | 1.007 | 0.065 | 0.839 @570310 | 0.119 | 0.078 | 0.09 / 0.478 |
| P_VWAPV_illiq | VWAPV | Oct 5 22:00 price/intraday | REJECTED: IR below .072 | 0.069 | 1.032 | 0.068 | 0.701 @604930 | 0.173 | 0.088 | 0.083 / 0.461 |
| P_RANGE_volcond | RANGEV | Oct 5 22:00 price/intraday | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.067 / 0.719 |
| P_A101 | A101 | Oct 5 22:00 price/intraday | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | -0.051 / 0.844 |
| P_FIRST_LAST | FL | Oct 5 22:00 price/intraday | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.046 / 0.424 |
| V_RSJ | RSJ | Oct 5 22:05 volatility | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.025 / 0.829 |
| V_RSKEW | RSKEW | Oct 5 22:05 volatility | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | -0.015 / 0.277 |
| V_VIXBETA | VIXB | Oct 5 22:05 volatility | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.019 / 0.705 |
| V_VOLSHOCK | VSHOCK | Oct 5 22:05 volatility | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.025 / 0.457 |
| V_LATEVOL_REV | LVREV | Oct 5 22:05 volatility | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.07 / 0.479 |
| INTRA_rnd_iss_w3 | INTRA | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.064 / 0.727 |
| VWAPV_rnd_iss_w2 | VWAPV | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.057 / 0.699 |
| RETL_rnd_iss_w2 | RETL | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.068 / 0.689 |
| OVN_rnd_iss_w2 | OVN | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.05 / 0.759 |
| D3_rnd_iss_w2 | D3 | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.064 / 0.707 |
| RANGE_rnd_iss_w2 | RANGE | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.061 / 0.731 |
| FUND5 | FUND | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.05 / 0.666 |
| TUGOFWAR | TOW | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0.007 / 0.568 |
| PEAD | PEAD | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | -0.003 / 0.461 |
| SUBIND_MOM | SUBMOM | Oct 5 21:00 runner v3 blend grid | FAST ONLY (not Slow-tested) |  |  |  |  |  |  | 0 / 0.655 |
| S_VWAPT_rnd_sbc_gpa | VWAPT | Oct 5 23:00 Slow blends | REJECTED: correlation (IR ok) | 0.09 | 0.655 | 0.111 | 0.72 @605850 | 0.203 | 0.099 |  |
| S_ALLPOS_price | MIX | Oct 5 23:00 Slow blends | REJECTED: correlation (IR ok) | 0.092 | 0.951 | 0.095 | 0.753 @604930 | 0.173 | 0.078 |  |
| S_VWAPT_rnd_iss_gpa | VWAPT | Oct 5 23:00 Slow blends | REJECTED: correlation (IR ok) | 0.096 | 0.741 | 0.112 | 0.739 @605850 | 0.203 | 0.114 |  |
| S_ILLIQ_rnd_iss_gpa | VWAPV | Oct 5 23:00 Slow blends | REJECTED: correlation (IR ok) | 0.092 | 0.645 | 0.114 | 0.701 @605850 | 0.203 | 0.117 |  |
| S_VWAPT_rnd_sbc_gpa_w2 | VWAPT | Oct 5 23:00 Slow blends | REJECTED: correlation (IR ok) | 0.085 | 0.463 | 0.125 | 0.695 @605850 | 0.203 | 0.087 |  |
| S_VWAPT_sbc_iss_fcf_w2 | VWAPT | Oct 5 23:00 Slow blends | REJECTED: IR below .072 | 0.067 | 0.545 | 0.09 | 0.682 @605850 | 0.203 | 0.054 |  |
| S_COMP5_slow | COMP | Oct 5 23:00 Slow blends | REJECTED: IR below .072 | 0.05 | 0.049 | 0.226 | 0.571 @605850 | 0.203 | 0.05 |  |
| S_CI_sbc_iss_fcf_w2 | CI | Oct 5 23:00 Slow blends | REJECTED: correlation (IR ok) | 0.078 | 0.512 | 0.109 | 0.646 @605850 | 0.203 | 0.052 |  |
| S_BL1_subind | VWAPT | Oct 5 23:00 Slow blends | REJECTED: correlation (IR ok) | 0.088 | 0.695 | 0.106 | 0.715 @605850 | 0.203 | 0.079 |  |
| S_VWAPT_vol_iss | VWAPT | Oct 5 23:00 Slow blends | REJECTED: IR below .072 | 0.053 | 0.406 | 0.084 | 0.772 @669233 | 0.233 | 0.035 |  |
| S_LATEVOL_sbc_iss_fcf_w2 | LVREV | Oct 5 23:00 Slow blends | REJECTED: correlation (IR ok) | 0.075 | 0.54 | 0.102 | 0.527 @570604 | 0.119 | 0.034 |  |
| Q_52WH | 52WH | Oct 6 00:55 new families | REJECTED: IR below .072 | -0.02 | 0.168 | -0.049 | 0.662 @579357 | 0.198 | -0.002 |  |
| Q_FROG | FROG | Oct 6 00:55 new families | FAILED (portal error) |  |  |  |  |  |  |  |
| Q_TUGOFWAR | OVN | Oct 6 00:55 new families | REJECTED: IR below .072 | 0.027 | 0.3 | 0.049 | 0.594 @579357 | 0.198 | 0.018 |  |
| Q_HVRP | HVRP | Oct 6 00:55 new families | REJECTED: IR below .072 | -0.012 | 0.899 | -0.012 | 0.34 @577441 |  | 0.042 |  |
| Q_VALxQUAL | QV | Oct 6 00:55 new families | REJECTED: IR below .072 | -0.003 | 0.041 | -0.014 | 0.657 @576233 | 0.164 | -0.025 |  |
| Q_ACCR_AG | ACCR | Oct 6 00:55 new families | REJECTED: IR below .072 | 0.067 | 0.051 | 0.298 | 0.879 @567998 | 0.328 | 0.095 |  |
| Q_BAB | BAB | Oct 6 00:55 new families | REJECTED: IR below .072 | -0.018 | 0.06 | -0.072 | 0.681 @628834 | 0.192 | -0.022 |  |
| Q_MAX_RETAIL | MAX | Oct 6 00:55 new families | REJECTED: IR below .072 | 0.002 | 0.259 | 0.004 | 0.611 @628834 | 0.192 | -0.015 |  |
| Q_LEADLAG | LL | Oct 6 00:55 new families | REJECTED: IR below .072 | -0.03 | 0.682 | -0.036 | 0.613 @642093 | 0.148 | -0.04 |  |
| Q_EPSMOM | EMOM | Oct 6 00:55 new families | REJECTED: IR below .072 | -0.021 | 0.086 | -0.071 | 0.387 @667066 |  | -0.016 |  |
| T_LATE_w3 | LVREV | Oct 6 07:00 near-miss variants | SUBMITTED | 0.073 | 0.486 | 0.105 | 0.506 @665632 | 0.094 | 0.031 |  |
| T_LATE_s3_w2 | LVREV | Oct 6 07:00 near-miss variants | REJECTED: IR below .072 | 0.061 | 0.439 | 0.092 | 0.959 @684336 | 0.126 | 0.034 |  |
| T_LATE_accr_w2 | LVREV | Oct 6 07:00 near-miss variants | SUBMITTED | 0.092 | 0.328 | 0.161 | 0.824 @684336 | 0.126 | 0.062 |  |
| T_LATE_sub_w2 | LVREV | Oct 6 07:00 near-miss variants | REJECTED: correlation (IR ok) | 0.079 | 0.571 | 0.105 | 0.895 @684336 | 0.126 | 0.032 |  |
| T_COMP7 | COMP | Oct 6 07:00 near-miss variants | SUBMITTED | 0.083 | 0.051 | 0.366 | 0.786 @685104 | 0.193 | 0.076 |  |
| T_COMP5b | COMP | Oct 6 07:00 near-miss variants | REJECTED: IR below .072 | 0.069 | 0.053 | 0.301 | 0.888 @685741 | 0.439 | 0.058 |  |
| T_COMP7_sub | COMP | Oct 6 07:00 near-miss variants | REJECTED: IR below .072 | 0.057 | 0.053 | 0.248 | 0.865 @685741 | 0.439 | 0.068 |  |
| U_VWAPT_szvo | VWAPT | Oct 6 09:50 upgrades | REJECTED: IR below .072 | 0.051 | 1.01 | 0.051 | 0.612 @570310 | 0.119 | 0.086 |  |
| U_PRICE2_szvo | MIX | Oct 6 09:50 upgrades | REJECTED: correlation (IR ok) | 0.093 | 0.998 | 0.093 | 0.704 @570310 | 0.119 | 0.1 |  |
| U_VWAPT_rig_szvo | VWAPT | Oct 6 09:50 upgrades | REJECTED: correlation (IR ok) | 0.099 | 0.742 | 0.115 | 0.701 @605850 | 0.203 | 0.127 |  |
| U_FMOM5 | FMOM | Oct 6 09:50 upgrades | EMPTY (lookback bug; rerun queued) | 0 | 0 | 0 | 0 |  |  |  |
| U_PRICE2_w10 | MIX | Oct 6 09:50 upgrades | REJECTED: correlation (IR ok) | 0.08 | 0.848 | 0.087 | 0.61 @570310 | 0.119 | 0.112 |  |
| U_PRICE2_s3 | MIX | Oct 6 09:50 upgrades | REJECTED: correlation (IR ok) | 0.072 | 0.545 | 0.097 | 0.703 @570310 | 0.119 | 0.108 |  |
| U_FMOM5_d120 | FMOM | Oct 6 09:50 upgrades | REJECTED: IR below .072 | 0.028 | 0.064 | 0.112 | 0.492 @595355 |  | 0.03 |  |
| U_FMOM5_lb330 | FMOM | Oct 6 09:50 upgrades | FAILED (portal: lookback > 300) |  |  |  |  |  |  |  |
| R_PRICE2_band | MIX | Oct 6 11:15 repair tests | FAILED (bool - bool crash) |  |  |  |  |  |  |  |
| R_PRICE2_ewm | MIX | Oct 6 11:15 repair tests | REJECTED: correlation (IR ok) | 0.085 | 0.778 | 0.097 | 0.726 @570310 | 0.119 | 0.105 |  |
| R_RIG_weekly | VWAPT | Oct 6 11:15 repair tests | FAILED (bool to ts_delay: needs float32) |  |  |  |  |  |  |  |
| U_ILLIQ_rig_szvo | VWAPV | Oct 6 09:50 upgrades | REJECTED: correlation (IR ok) | 0.078 | 0.382 | 0.126 | 0.626 @601796 | 0.169 | 0.08 |  |
| U_VWAPT_FMOM_w2 | VWAPT | Oct 6 09:50 upgrades | REJECTED: IR below .072 | 0.055 | 0.341 | 0.095 | 0.436 @595355 |  | 0.035 |  |
| VP_VOV_D60 | VP | Oct 6 local cycle 1 | REJECTED: IR below .072 | -0.01 | 0.073 | -0.038 | 0.17 @686926 |  | 0.012 |  |
| VP_VOV_INTRA | VP | Oct 6 local cycle 1 | REJECTED: IR below .072 | 0.017 | 0.151 | 0.044 | 0.242 @664006 |  | 0.006 |  |
| VP_COSK_60 | VP | Oct 6 local cycle 1 | REJECTED: IR below .072 | 0.023 | 0.17 | 0.055 | 0.445 @642093 |  | 0.018 |  |
| VP_COSK_RESID120 | VP | Oct 6 local cycle 1 | REJECTED: IR below .072 | 0.004 | 0.123 | 0.01 | 0.503 @579357 |  | 0.012 |  |
| VP_RESREV_VIX | VP | Oct 6 local cycle 1 | REJECTED: IR below .072 | 0.02 | 0.851 | 0.022 | 0.833 @574490 |  | 0.002 |  |
| REG_VR_FLIP | REG | Oct 6 local cycle 1 | QUEUED (Slow) |  |  |  |  |  |  |  |
| REG_VR_SMOOTH | REG | Oct 6 local cycle 1 | QUEUED (Slow) |  |  |  |  |  |  |  |
| REG_PKCC_REV | REG | Oct 6 local cycle 1 | QUEUED (Slow) |  |  |  |  |  |  |  |
| REG_DNBETA_ASYM | REG | Oct 6 local cycle 1 | QUEUED (Slow) |  |  |  |  |  |  |  |
| REG_DNBETA_250 | REG | Oct 6 local cycle 1 | QUEUED (Slow) |  |  |  |  |  |  |  |
| ID_TSIZE_SHIFT | ID | Oct 6 local cycle 1 | QUEUED (Slow) |  |  |  |  |  |  |  |
| ID_TSIZE_FLOW | ID | Oct 6 local cycle 1 | QUEUED (Slow) |  |  |  |  |  |  |  |
| ANOM_MAX20 | ANOM | Oct 6 local cycle 1 | QUEUED (Slow) |  |  |  |  |  |  |  |
| ANOM_MAX_VOLADJ | ANOM | Oct 6 local cycle 1 | QUEUED (Slow) |  |  |  |  |  |  |  |
| A101_002 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_003 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_004 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_006 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_009 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_012 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_014 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_015 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_018 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_020 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_022 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_026 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_030 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_033 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_034 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_035 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_038 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_040 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_041 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_043 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_044 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_050 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_053 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_054 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| A101_055 | A101 | Oct 6 101-alphas | QUEUED (Fast screen) |  |  |  |  |  |  |  |
| R_PRICE2_band2 | MIX | Oct 6 11:45 repair tests | REJECTED: IR below .072 | 0.018 | 1.932 | 0.013 | 0.111 @690060 |  | 0.008 |  |
| G_VWAPT_mom60 | VWAPT | Oct 6 11:45 regime gates | FAILED (cs_indneut needs integer group) |  |  |  |  |  |  |  |
| G_RIG_mom60 | VWAPT | Oct 6 11:45 regime gates | FAILED (cs_indneut needs integer group) |  |  |  |  |  |  |  |
| G_ACCR_mom20 | ACCR | Oct 6 11:45 regime gates | FAILED (cs_indneut needs integer group) |  |  |  |  |  |  |  |
| G_ACCR_stop10 | ACCR | Oct 6 11:45 regime gates | FAILED (cs_indneut needs integer group) |  |  |  |  |  |  |  |
| G_VWAPT_mom60b | VWAPT | Oct 6 14:00 reruns (dtype fixes) | REJECTED: IR below .072 | 0.071 | 1.135 | 0.066 | 0.658 @604930 | 0.173 | 0.073 |  |
| G_ACCR_mom20b | ACCR | Oct 6 14:00 reruns (dtype fixes) | REJECTED: correlation (IR ok) | 0.073 | 0.481 | 0.105 | 0.673 @673102 | 0.409 | 0.109 |  |
| G_VWAPT_mom60ind | VWAPT | Oct 6 14:00 reruns (dtype fixes) | REJECTED: IR below .072 | 0.065 | 1.092 | 0.062 | 0.682 @570310 | 0.119 | 0.056 |  |
| U_VWAPT_FMOM_w1 | VWAPT | Oct 6 14:00 reruns (dtype fixes) | RUNNING |  |  |  |  |  |  |  |
| G_ACCR_stop10b | ACCR | Oct 6 14:00 reruns (dtype fixes) | SKIPPED (gates retired: switching raises turnover) |  |  |  |  |  |  |  |
| G_RIG_mom60b | VWAPT | Oct 6 14:00 reruns (dtype fixes) | SKIPPED (gates retired: switching raises turnover) |  |  |  |  |  |  |  |
| R_RIG_weekly2 | VWAPT | Oct 6 14:00 reruns (dtype fixes) | QUEUED (Slow) |  |  |  |  |  |  |  |
| X_PL_FM4_w1 | MIXF | Oct 6 14:45 anti-correlated blends | QUEUED (Slow) |  |  |  |  |  |  |  |
| X_PL_FM4_w05 | MIXF | Oct 6 14:45 anti-correlated blends | QUEUED (Slow) |  |  |  |  |  |  |  |
| X_VW_FM5_w1 | MIXF | Oct 6 14:45 anti-correlated blends | QUEUED (Slow) |  |  |  |  |  |  |  |
| X_VW_FM5_w05 | MIXF | Oct 6 14:45 anti-correlated blends | QUEUED (Slow) |  |  |  |  |  |  |  |
