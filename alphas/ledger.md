# Alpha ledger (append-only)

F = Fast, S = Slow. corr = max correlation to the competition pool. E = eligible.

| Time (IST) | Tag | Family | F IR | F TVR | F IR/sqrtTVR | F corr | F E | S IR | S corr | S E | State | Submitted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Oct 5 pm | c_intra | INTRA | .090 | .585 | .118 | .649 | no | | | | fdone | no |
| Oct 5 pm | c3_rnd_earn | INTRA+rnd+earn | .094 | .471 | .137 | .560 | yes | .082 | .688 | no | sdone | no |
| Oct 5 pm | c3_r3f2e | INTRA+rnd+earn | .084 | .341 | .145 | .589 | yes | | | | fdone | no |
| Oct 5 21:00 | INTRA_rnd_earn_w3 | INTRA | .076 | .304 | .137 | .647 | yes | | | | fdone | no |
| Oct 5 21:00 | VWAPV_rnd_earn_w2 | VWAPV | .076 | .406 | .120 | .656 | yes | | | | fdone | no |
| Oct 5 21:00 | RETL_rnd_earn_w2 | RETL | .075 | .361 | .125 | .594 | yes | | | | fdone | no |
| Oct 5 21:00 | OVN_rnd_earn_w2 | OVN | .060 | .359 | .100 | .573 | no | | | | fdone | no |
| Oct 5 21:00 | D3_rnd_earn_w2 | D3 | .063 | .447 | .095 | .673 | no | | | | fdone | no |
| Oct 5 21:00 | RANGE_rnd_earn_w2 | RANGE | .067 | .369 | .109 | .619 | no | | | | fdone | no |
| Oct 5 21:00 | INTRA_rnd_sbc_w3 | INTRA | .082 | .356 | .137 | .565 | no | | | | fdone | no |
| Oct 5 21:00 | VWAPV_rnd_sbc_w2 | VWAPV | .078 | .522 | .107 | .476 | yes | .052 | .600 | no | sdone | no |
| Oct 5 23:10 | P_CI_s3 | INTRA | .054 | .384 | .088 | .598 | no | | | | fdone | no |
| Oct 5 23:10 | P_CI_volcond | INTRA | .091 | .897 | .096 | .612 | no | | | | fdone | no |
| Oct 5 23:10 | P_CI_lowvol | INTRA | .070 | .646 | .087 | .443 | no | | | | fdone | no |
| Oct 5 23:10 | P_VWAPV_s3 | VWAPV | .058 | .733 | .067 | .379 | no | | | | fdone | no |
| Oct 5 23:10 | P_VWAPT | VWAPV | .098 | .919 | .103 | .480 | yes | .083 | .782 | no | sdone | no |
| Oct 5 23:10 | P_RETL_small | RETL | .049 | .621 | .062 | .441 | no | | | | fdone | no |
| Oct 5 23:10 | P_VWAPV_sub | VWAPV | .090 | .902 | .094 | .478 | yes | .065 | .839 | no | sdone | no |
| Oct 5 23:10 | P_VWAPV_illiq | VWAPV | .083 | .910 | .087 | .461 | yes | .069 | .701 | no | sdone | no |
| Oct 5 23:10 | P_RANGE_volcond | RANGE | .067 | .901 | .070 | .719 | no | | | | fdone | no |
| Oct 5 23:10 | P_A101 | A101 | -.051 | 1.362 | -.044 | .844 | no | | | | fdone | no |
| Oct 5 23:10 | P_FIRST_LAST | FL | .046 | .629 | .058 | .424 | no | | | | fdone | no |
| Oct 5 23:10 | V_RSJ | VOL | .025 | .274 | .048 | .829 | no | | | | fdone | no |
| Oct 5 23:10 | V_RSKEW | VOL | -.015 | .270 | -.028 | .277 | no | | | | fdone | no |
| Oct 5 23:10 | V_VIXBETA | VOL | .019 | .114 | .057 | .705 | no | | | | fdone | no |
| Oct 5 23:10 | V_VOLSHOCK | VOL | .025 | .491 | .035 | .457 | no | | | | fdone | no |
| Oct 5 23:10 | V_LATEVOL_REV | RETL | .070 | .794 | .079 | .479 | yes | | | | fdone | no |
| Oct 5 23:50 | S_VWAPT_rnd_sbc_gpa | VWAPT+rnd+sbc+gpa | | | | | | .090 | .720 | no | sdone | no |
| Oct 6 00:40 | S_ALLPOS_price | VWAPT+CI+LATEVOL | | | | | | .092 | .753 | no | sdone | no |
| Oct 6 00:55 | S_VWAPT_rnd_iss_gpa | VWAPT+rnd+iss+gpa | | | | | | .096 | .739 | no | sdone | no |
| Oct 6 night | S_ILLIQ_rnd_iss_gpa | VWAPV+rnd+iss+gpa | | | | | | .092 | .701 | no | sdone | no |
| Oct 6 night | S_VWAPT_rnd_sbc_gpa_w2 | VWAPT+rnd+sbc+gpa | | | | | | .085 | .695 | no | sdone | no |
| Oct 6 night | S_VWAPT_sbc_iss_fcf_w2 | VWAPT+sbc+iss+fcf | | | | | | .067 | .682 | no | sdone | no |
| Oct 6 night | S_COMP5_slow | COMP | | | | | | .050 | .571 | no (irtvr .226 OK, IR low) | sdone | no |
| Oct 6 night | S_CI_sbc_iss_fcf_w2 | CI+sbc+iss+fcf | | | | | | .078 | .646 | no | sdone | no |
| Oct 6 night | S_BL1_subind | VWAPT+rnd+sbc+gpa | | | | | | .088 | .715 | no | sdone | no |
| Oct 6 night | S_VWAPT_vol_iss | VWAPT+RSJ+VIXB+iss | | | | | | .053 | .772 | no | sdone | no |
| Oct 6 night | S_LATEVOL_sbc_iss_fcf_w2 | LVREV+sbc+iss+fcf | | | | | | .075 | .527 | no (NEAR MISS) | sdone | no |
| Oct 6 night | Q_52WH | 52WH | | | | | | -.020 | .662 | no | sdone | no |
| Oct 6 night | Q_FROG | FROG | | | | | | | | | sfail (loading_data), requeued lb 520 | no |
| Oct 6 night | Q_TUGOFWAR | OVN | | | | | | .027 | .594 | no | sdone | no |
| Oct 6 night | Q_HVRP | HVRP | | | | | | -.012 | .340 | no | sdone | no |
| Oct 6 night | Q_VALxQUAL | QV | | | | | | -.003 | .657 | no | sdone | no |
| Oct 6 night | Q_ACCR_AG | ACCR | | | | | | .067 | .879 | no (irtvr .298) | sdone | no |
| Oct 6 night | Q_BAB | BAB | | | | | | -.018 | .681 | no | sdone | no |
| Oct 6 night | Q_MAX_RETAIL | MAX | | | | | | .002 | .611 | no | sdone | no |
| Oct 6 night | Q_LEADLAG | LL | | | | | | -.030 | .613 | no | sdone | no |
| Oct 6 night | Q_EPSMOM | EMOM | | | | | | -.021 | .387 | no | sdone | no |
