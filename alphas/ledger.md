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
| Oct 5 21:00 | VWAPV_rnd_sbc_w2 | VWAPV | .078 | .522 | .107 | .476 | yes | .052 | .600@631112 (irtvr .068 vs bar .145) | no | sdone | no |
| Oct 5 23:10 | P_CI_s3 | INTRA | .054 | .384 | .088 | .598 | no | | | | fdone | no |
| Oct 5 23:10 | P_CI_volcond | INTRA | .091 | .897 | .096 | .612 | no | | | | fdone | no |
| Oct 5 23:10 | P_CI_lowvol | INTRA | .070 | .646 | .087 | .443 | no | | | | fdone | no |
| Oct 5 23:10 | P_VWAPV_s3 | VWAPV | .058 | .733 | .067 | .379 | no | | | | fdone | no |
| Oct 5 23:10 | P_VWAPT | VWAPV | .098 | .919 | .103 | .480 | yes | .083 | .782@570310 (irtvr .081 vs bar .119) | no | sdone | no |
| Oct 5 23:10 | P_RETL_small | RETL | .049 | .621 | .062 | .441 | no | | | | fdone | no |
| Oct 5 23:10 | P_VWAPV_sub | VWAPV | .090 | .902 | .094 | .478 | yes | .065 | .839@570310 (irtvr .065 vs bar .119) | no | sdone | no |
| Oct 5 23:10 | P_VWAPV_illiq | VWAPV | .083 | .910 | .087 | .461 | yes | .069 | .701@604930 (irtvr .068 vs bar .173) | no | sdone | no |
| Oct 5 23:10 | P_RANGE_volcond | RANGE | .067 | .901 | .070 | .719 | no | | | | fdone | no |
| Oct 5 23:10 | P_A101 | A101 | -.051 | 1.362 | -.044 | .844 | no | | | | fdone | no |
| Oct 5 23:10 | P_FIRST_LAST | FL | .046 | .629 | .058 | .424 | no | | | | fdone | no |
| Oct 5 23:10 | V_RSJ | VOL | .025 | .274 | .048 | .829 | no | | | | fdone | no |
| Oct 5 23:10 | V_RSKEW | VOL | -.015 | .270 | -.028 | .277 | no | | | | fdone | no |
| Oct 5 23:10 | V_VIXBETA | VOL | .019 | .114 | .057 | .705 | no | | | | fdone | no |
| Oct 5 23:10 | V_VOLSHOCK | VOL | .025 | .491 | .035 | .457 | no | | | | fdone | no |
| Oct 5 23:10 | V_LATEVOL_REV | RETL | .070 | .794 | .079 | .479 | yes | | | | fdone | no |
| Oct 5 23:50 | S_VWAPT_rnd_sbc_gpa | VWAPT+rnd+sbc+gpa |  |  |  |  |  | .090 | .720@605850 (irtvr .111 vs bar .203) | no | sdone | no |
| Oct 6 00:40 | S_ALLPOS_price | VWAPT+CI+LATEVOL |  |  |  |  |  | .092 | .753@604930 (irtvr .095 vs bar .173) | no | sdone | no |
| Oct 6 00:55 | S_VWAPT_rnd_iss_gpa | VWAPT+rnd+iss+gpa |  |  |  |  |  | .096 | .739@605850 (irtvr .112 vs bar .203) | no | sdone | no |
| Oct 6 night | S_ILLIQ_rnd_iss_gpa | VWAPV+rnd+iss+gpa |  |  |  |  |  | .092 | .701@605850 (irtvr .114 vs bar .203) | no | sdone | no |
| Oct 6 night | S_VWAPT_rnd_sbc_gpa_w2 | VWAPT+rnd+sbc+gpa |  |  |  |  |  | .085 | .695@605850 (irtvr .125 vs bar .203) | no | sdone | no |
| Oct 6 night | S_VWAPT_sbc_iss_fcf_w2 | VWAPT+sbc+iss+fcf |  |  |  |  |  | .067 | .682@605850 (irtvr .090 vs bar .203) | no | sdone | no |
| Oct 6 night | S_COMP5_slow | COMP |  |  |  |  |  | .050 | .571@605850 (irtvr .226 vs bar .203) | no | sdone | no |
| Oct 6 night | S_CI_sbc_iss_fcf_w2 | CI+sbc+iss+fcf |  |  |  |  |  | .078 | .646@605850 (irtvr .109 vs bar .203) | no | sdone | no |
| Oct 6 night | S_BL1_subind | VWAPT+rnd+sbc+gpa |  |  |  |  |  | .088 | .715@605850 (irtvr .106 vs bar .203) | no | sdone | no |
| Oct 6 night | S_VWAPT_vol_iss | VWAPT+RSJ+VIXB+iss |  |  |  |  |  | .053 | .772@669233 (irtvr .084 vs bar .233) | no | sdone | no |
| Oct 6 night | S_LATEVOL_sbc_iss_fcf_w2 | LVREV+sbc+iss+fcf |  |  |  |  |  | .075 | .527@570604 (irtvr .102 vs bar .119) | no | sdone | no |
| Oct 6 night | Q_52WH | 52WH |  |  |  |  |  | -.020 | .662@579357 (irtvr -.049 vs bar .198) | no | sdone | no |
| Oct 6 night | Q_FROG | FROG |  |  |  |  |  |  |  |  | sfail | no |
| Oct 6 night | Q_TUGOFWAR | OVN |  |  |  |  |  | .027 | .594@579357 (irtvr .049 vs bar .198) | no | sdone | no |
| Oct 6 night | Q_HVRP | HVRP |  |  |  |  |  | -.012 | .340@577441 | no | sdone | no |
| Oct 6 night | Q_VALxQUAL | QV |  |  |  |  |  | -.003 | .657@576233 (irtvr -.014 vs bar .164) | no | sdone | no |
| Oct 6 night | Q_ACCR_AG | ACCR |  |  |  |  |  | .067 | .879@567998 (irtvr .298 vs bar .328) | no | sdone | no |
| Oct 6 night | Q_BAB | BAB |  |  |  |  |  | -.018 | .681@628834 (irtvr -.072 vs bar .192) | no | sdone | no |
| Oct 6 night | Q_MAX_RETAIL | MAX |  |  |  |  |  | .002 | .611@628834 (irtvr .004 vs bar .192) | no | sdone | no |
| Oct 6 night | Q_LEADLAG | LL |  |  |  |  |  | -.030 | .613@642093 (irtvr -.036 vs bar .148) | no | sdone | no |
| Oct 6 night | Q_EPSMOM | EMOM |  |  |  |  |  | -.021 | .387@667066 | no | sdone | no |
| Oct 6 am | T_LATE_w3 | LVREV+sbc+iss+fcf (3x) |  |  |  |  |  | .073 | .506@665632 (irtvr .105 vs bar .094) | yes | submitted | YES |
| Oct 6 am | T_LATE_accr_w2 | LVREV+sbc+iss+fcf+accr (2x) |  |  |  |  |  | .092 | .824@684336 own (irtvr .161 vs bar .126) | yes | submitted | YES |
| Oct 6 am | T_COMP7 | COMP7 fundamentals |  |  |  |  |  | .083 | .786@685104 own (irtvr .366 vs bar .193) | yes | submitted | YES |
| Oct 6 am | T_LATE_s3_w2 | LVREV |  |  |  |  |  | .061 | .959@684336 own (irtvr .092 vs bar .126) | no | sdone | no |
| Oct 6 am | T_LATE_sub_w2 | LVREV |  |  |  |  |  | .079 | .895@684336 own (irtvr .105 vs bar .126) | no | sdone | no |
| Oct 6 am | T_COMP5b | COMP |  |  |  |  |  | .069 | .888@685741 own (irtvr .301 vs bar .439) | no | sdone | no |
| Oct 6 am | T_COMP7_sub | COMP |  |  |  |  |  | .057 | .865@685741 own (irtvr .248 vs bar .439) | no | sdone | no |
| Oct 6 10:10 | U_VWAPT_szvo | VWAPT size+vol neutral |  |  |  |  |  | .051 | .612@570310 (irtvr .051 vs bar .119) | no | sdone | no |
| Oct 6 18:02 | RETL_rnd_sbc_w2 | RETL | .071 | .406 | .112 | .508 | no |  |  |  | fdone | no |
| Oct 6 18:02 | OVN_rnd_sbc_w2 | OVN | .046 | .395 | .072 | .509 | no |  |  |  | fdone | no |
| Oct 6 18:02 | D3_rnd_sbc_w2 | D3 | .055 | .549 | .074 | .700 | no |  |  |  | fdone | no |
| Oct 6 18:02 | RANGE_rnd_sbc_w2 | RANGE | .063 | .417 | .098 | .603 | no |  |  |  | fdone | no |
| Oct 6 18:02 | INTRA_gpa_iss_w3 | INTRA | .067 | .202 | .149 | .718 | no |  |  |  | fdone | no |
| Oct 6 18:02 | VWAPV_gpa_iss_w2 | VWAPV | .061 | .315 | .108 | .706 | no |  |  |  | fdone | no |
| Oct 6 18:02 | RETL_gpa_iss_w2 | RETL | .071 | .273 | .136 | .638 | no |  |  |  | fdone | no |
| Oct 6 18:02 | OVN_gpa_iss_w2 | OVN | .053 | .269 | .103 | .683 | no |  |  |  | fdone | no |
| Oct 6 18:02 | D3_gpa_iss_w2 | D3 | .067 | .364 | .111 | .646 | no |  |  |  | fdone | no |
| Oct 6 18:02 | RANGE_gpa_iss_w2 | RANGE | .065 | .285 | .122 | .697 | no |  |  |  | fdone | no |
| Oct 6 18:02 | INTRA_fcf_iss_w3 | INTRA | .053 | .204 | .118 | .710 | no |  |  |  | fdone | no |
| Oct 6 18:02 | VWAPV_fcf_iss_w2 | VWAPV |  |  |  |  |  |  |  |  | ftimeout | no |
| Oct 6 18:02 | RETL_fcf_iss_w2 | RETL |  |  |  |  |  |  |  |  | ftimeout | no |
| Oct 6 18:02 | OVN_fcf_iss_w2 | OVN |  |  |  |  |  |  |  |  | ftimeout | no |
| Oct 6 18:02 | D3_fcf_iss_w2 | D3 | .058 | .357 | .097 | .721 | no |  |  |  | fdone | no |
| Oct 6 18:02 | RANGE_fcf_iss_w2 | RANGE | .051 | .279 | .096 | .715 | no |  |  |  | fdone | no |
| Oct 6 18:02 | INTRA_rnd_fcf_w3 | INTRA | .084 | .342 | .143 | .556 | no |  |  |  | fdone | no |
| Oct 6 18:02 | VWAPV_rnd_fcf_w2 | VWAPV | .076 | .496 | .108 | .548 | no |  |  |  | fdone | no |
| Oct 6 18:02 | RETL_rnd_fcf_w2 | RETL | .071 | .390 | .114 | .505 | yes |  |  |  | fdone | no |
| Oct 6 18:02 | OVN_rnd_fcf_w2 | OVN | .045 | .380 | .073 | .512 | no |  |  |  | fdone | no |
| Oct 6 18:02 | D3_rnd_fcf_w2 | D3 | .056 | .527 | .077 | .647 | no |  |  |  | fdone | no |
| Oct 6 18:02 | RANGE_rnd_fcf_w2 | RANGE | .065 | .401 | .102 | .570 | no |  |  |  | fdone | no |
| Oct 6 18:02 | INTRA_rnd_iss_w3 | INTRA | .064 | .220 | .136 | .727 | no |  |  |  | fdone | no |
| Oct 6 18:02 | VWAPV_rnd_iss_w2 | VWAPV | .057 | .337 | .098 | .699 | no |  |  |  | fdone | no |
| Oct 6 18:02 | RETL_rnd_iss_w2 | RETL | .068 | .291 | .126 | .689 | no |  |  |  | fdone | no |
| Oct 6 18:02 | OVN_rnd_iss_w2 | OVN | .050 | .285 | .093 | .759 | no |  |  |  | fdone | no |
| Oct 6 18:02 | D3_rnd_iss_w2 | D3 | .064 | .388 | .102 | .707 | no |  |  |  | fdone | no |
| Oct 6 18:02 | RANGE_rnd_iss_w2 | RANGE | .061 | .303 | .111 | .731 | no |  |  |  | fdone | no |
| Oct 6 18:02 | FUND5 | FUND5 | .050 | .045 | .236 | .666 | no |  |  |  | fdone | no |
| Oct 6 18:02 | TUGOFWAR | TUGOFWAR | .007 | .290 | .012 | .568 | no |  |  |  | fdone | no |
| Oct 6 18:02 | PEAD | PEAD | -.003 | .908 | -.003 | .461 | no |  |  |  | fdone | no |
| Oct 6 18:02 | SUBIND_MOM | SUBIND | .000 | .854 | .000 | .655 | no |  |  |  | fdone | no |
| Oct 6 18:02 | U_PRICE2_szvo | MIX |  |  |  |  |  | .093 | .704@570310 (irtvr .093 vs bar .119) | no | sdone | no |
| Oct 6 18:02 | U_VWAPT_rig_szvo | VWAPT |  |  |  |  |  | .099 | .701@605850 (irtvr .115 vs bar .203) | no | sdone | no |
| Oct 6 18:02 | U_FMOM5 | FMOM |  |  |  |  |  | .000 | .000 | no | sdone | no |
| Oct 6 18:02 | U_PRICE2_w10 | U |  |  |  |  |  | .080 | .610@570310 (irtvr .087 vs bar .119) | no | sdone | no |
| Oct 6 18:02 | U_PRICE2_s3 | U |  |  |  |  |  | .072 | .703@570310 (irtvr .097 vs bar .119) | no | sdone | no |
| Oct 6 18:02 | U_FMOM5_d120 | U |  |  |  |  |  | .028 | .492@595355 | no | sdone | no |
| Oct 6 18:02 | U_FMOM5_lb330 | U |  |  |  |  |  |  |  |  | sfail | no |
| Oct 6 18:02 | R_PRICE2_band | R |  |  |  |  |  |  |  |  | sfail | no |
| Oct 6 18:02 | R_PRICE2_ewm | R |  |  |  |  |  | .085 | .726@570310 (irtvr .097 vs bar .119) | no | sdone | no |
| Oct 6 18:02 | R_PRICE2_band2 | R |  |  |  |  |  | .018 | .111@690060 | no | sdone | no |
| Oct 6 18:02 | R_RIG_weekly | R |  |  |  |  |  |  |  |  | sfail | no |
| Oct 6 18:02 | G_VWAPT_mom60 | G |  |  |  |  |  |  |  |  | sfail | no |
| Oct 6 18:02 | G_ACCR_mom20 | G |  |  |  |  |  |  |  |  | sfail | no |
| Oct 6 18:02 | G_ACCR_stop10 | G |  |  |  |  |  |  |  |  | sfail | no |
| Oct 6 18:02 | G_RIG_mom60 | G |  |  |  |  |  |  |  |  | sfail | no |
| Oct 6 18:02 | U_ILLIQ_rig_szvo | VWAPV |  |  |  |  |  | .078 | .626@601796 (irtvr .126 vs bar .169) | no | sdone | no |
| Oct 6 18:02 | U_VWAPT_FMOM_w2 | VWAPT |  |  |  |  |  | .055 | .436@595355 | no | sdone | no |
| Oct 6 18:02 | VP_VOV_D60 | VP_VOLOFVOL |  |  |  |  |  | -.010 | .170@686926 | no | sdone | no |
| Oct 6 18:02 | VP_VOV_INTRA | VP_VOLOFVOL |  |  |  |  |  | .017 | .242@664006 | no | sdone | no |
| Oct 6 18:02 | VP_COSK_60 | VP_COSKEW |  |  |  |  |  | .023 | .445@642093 | no | sdone | no |
| Oct 6 18:02 | VP_COSK_RESID120 | VP_COSKEW |  |  |  |  |  | .004 | .503@579357 (irtvr .010 vs bar .198) | no | sdone | no |
| Oct 6 18:02 | VP_RESREV_VIX | VP_RESREV_VIX |  |  |  |  |  | .020 | .833@574490 (irtvr .022 vs bar .163) | no | sdone | no |
| Oct 6 18:02 | G_VWAPT_mom60b | G |  |  |  |  |  | .071 | .658@604930 (irtvr .066 vs bar .173) | no | sdone | no |
| Oct 6 18:02 | G_ACCR_mom20b | G |  |  |  |  |  | .073 | .673@673102 (irtvr .105 vs bar .409) | no | sdone | no |
| Oct 6 18:02 | G_VWAPT_mom60ind | G |  |  |  |  |  | .065 | .682@570310 (irtvr .062 vs bar .119) | no | sdone | no |
| Oct 6 18:02 | U_VWAPT_FMOM_w1 | U |  |  |  |  |  | .070 | .466@659499 | yes | submitted | YES |
| Oct 6 18:02 | X_PL_FM4_w1 | X |  |  |  |  |  | .093 | .637@604930 (irtvr .112 vs bar .173) | no | sdone | no |
| Oct 6 18:02 | X_PL_FM4_w05 | X |  |  |  |  |  | .094 | .737@604930 (irtvr .102 vs bar .173) | no | sdone | no |
| Oct 6 18:02 | X_VW_FM5_w1 | X |  |  |  |  |  | .086 | .799@695151 own (irtvr .105 vs bar .116) | no | sdone | no |
| Oct 6 18:02 | X_VW_FM5_w05 | X |  |  |  |  |  | .088 | .730@695151 own (irtvr .096 vs bar .116) | no | sdone | no |
| Oct 6 18:02 | Y_PLsz_ACC_w07 | Y |  |  |  |  |  | .109 | 1.000@698181 own (irtvr .120 vs bar .144) | no | submitted | YES |
| Oct 6 18:42 | Y_PLsz_ACC_w12 | Y |  |  |  |  |  | .116 | .979@698181 own (irtvr .138 vs bar .144) | no | sdone | no |
| Oct 6 19:12 | Y_PLewm_ACC_w1 | Y |  |  |  |  |  | .101 | .974@698181 own (irtvr .121 vs bar .144) | no | sdone | no |
| Oct 6 19:12 | Y_VW_ACC_w1 | Y |  |  |  |  |  | .091 | .854@698181 own (irtvr .100 vs bar .144) | no | sdone | no |
| Oct 6 19:12 | MM1_TOXREV | MM |  |  |  |  |  | .059 | .628@640672 (irtvr .060 vs bar .119) | no | sdone | no |
| Oct 6 19:42 | MM2_SIZEREV | MM |  |  |  |  |  | .042 | .123@657905 | no | sdone | no |
| Oct 6 19:42 | MM3_CLOSEPRESS | MM |  |  |  |  |  | .053 | .821@569727 (irtvr .051 vs bar .098) | no | sdone | no |
| Oct 6 20:12 | MO1_RESMOM | MO |  |  |  |  |  | .008 | .622@595355 (irtvr .026 vs bar .428) | no | sdone | no |
| Oct 6 20:12 | MO2_FROG2 | MO |  |  |  |  |  | .008 | .573@595355 (irtvr .023 vs bar .428) | no | sdone | no |
| Oct 6 20:12 | MO3_VOLMOM | MO |  |  |  |  |  | .007 | .553@595355 (irtvr .023 vs bar .428) | no | sdone | no |
| Oct 6 20:12 | LIQ_TURNCV | LIQ |  |  |  |  |  | .021 | .473@634793 | no | sdone | no |
| Oct 6 20:41 | LIQ_ILLIQSHOCK | LIQ |  |  |  |  |  | .003 | .500@575475 | no | sdone | no |
| Oct 6 20:41 | MOMX_STMOM_HITURN | MOMX |  |  |  |  |  | -.012 | .510@579357 (irtvr -.021 vs bar .198) | no | sdone | no |
| Oct 6 20:41 | MOMX_SEASON_1Y | MOMX |  |  |  |  |  | .026 | .392@607689 | no | sdone | no |
| Oct 6 21:12 | HR_HKS_PERIOD | HR |  |  |  |  |  | .002 | .285@570604 | no | sdone | no |
| Oct 6 21:12 | FUND_ORGCAP | FUND |  |  |  |  |  | .013 | .242@697353 | no | sdone | no |
| Oct 6 21:12 | FUND_TAXMOM | FUND |  |  |  |  |  | .025 | .405@574700 | no | sdone | no |
| Oct 6 21:12 | PV_CORD | PV |  |  |  |  |  | .035 | .392@575403 | no | sdone | no |
| Oct 6 21:42 | R_RIG_weekly2 | R |  |  |  |  |  | .075 | .584@601796 (irtvr .147 vs bar .169) | no | sdone | no |
| Oct 6 22:12 | REG_VR_FLIP | REG_VARRATIO |  |  |  |  |  | .003 | .306@642093 | no | sdone | no |
| Oct 6 22:42 | REG_VR_SMOOTH | REG_VARRATIO |  |  |  |  |  | -.004 | .221@673420 | no | sdone | no |
| Oct 6 23:18 | R_RIGwk_k15 | R_RIG |  |  |  |  |  | .068 | .633@601796 (irtvr .153 vs bar .169) | no | sdone | no |
| Oct 6 23:42 | R_RIGwk_k2 | R_RIG |  |  |  |  |  | .063 | .647@601796 (irtvr .156 vs bar .169) | no | sdone | no |
| Oct 7 0:13 | R_RIAwk | R_RIA |  |  |  |  |  | .080 | .573@601796 (irtvr .161 vs bar .169) | no | sdone | no |
| Oct 7 0:43 | R_RIAwk_w10 | R_RIA |  |  |  |  |  | .070 | .558@601796 (irtvr .150 vs bar .169) | no | sdone | no |
| Oct 7 1:13 | R_RIAwk_a15 | R_RIA |  |  |  |  |  | .085 | .540@601796 (irtvr .179 vs bar .169) | yes | submitted | YES |
| Oct 7 1:42 | R_RIAwk_r07 | R_RIA |  |  |  |  |  | .076 | .981@707365 own (irtvr .171 vs bar .215) | no | sdone | no |
| Oct 7 2:12 | R_IAwk_szvo | R_RIA |  |  |  |  |  | .079 | .915@707365 own (irtvr .156 vs bar .215) | no | sdone | no |
| Oct 7 2:43 | Y_PLsz_ACC_w16 | Y_ACC |  |  |  |  |  | .118 | .940@698181 own (irtvr .149 vs bar .144) | yes | submitted | YES |
| Oct 7 3:12 | Y_PLsz_ACC_w20 | Y_ACC |  |  |  |  |  | .118 | .993@708808 own (irtvr .158 vs bar .179) | no | sdone | no |
| Oct 7 3:42 | R_RIGwk_w10 | R_RIG |  |  |  |  |  | .063 | .811@707365 own (irtvr .134 vs bar .215) | no | sdone | no |
| Oct 7 4:12 | R_RIGwk_w10k15 | R_RIG |  |  |  |  |  | .060 | .798@707365 own (irtvr .144 vs bar .215) | no | sdone | no |
| Oct 7 4:12 | SW_L_AOCI49 | SW_DOLLAR |  |  |  |  |  | -.009 | .380@656049 | no | sdone | no |
| Oct 7 4:12 | SW_L_AOIA31 | SW_DOLLAR |  |  |  |  |  | -.018 | .236@676810 | no | sdone | no |
| Oct 7 4:12 | SW_L_CPOLTD33 | SW_DOLLAR |  |  |  |  |  | .035 | .167@655304 | no | sdone | no |
| Oct 7 4:12 | SW_L_DTALT70 | SW_DOLLAR |  |  |  |  |  | .017 | .286@700897 | no | sdone | no |
| Oct 7 4:12 | SW_L_DA60 | SW_DOLLAR |  |  |  |  |  | -.009 | .287@631112 | no | sdone | no |
| Oct 7 4:42 | SW_L_EOERCO55 | SW_DOLLAR |  |  |  |  |  | .019 | .234@578055 | no | sdone | no |
| Oct 7 4:42 | SW_L_LTD22 | SW_DOLLAR |  |  |  |  |  | -.024 | .687@578688 (irtvr -.141 vs bar .210) | no | sdone | no |
| Oct 7 4:42 | SW_L_STI78 | SW_DOLLAR |  |  |  |  |  | .013 | .439@596206 | no | sdone | no |
| Oct 7 4:42 | SW_L_TOE60 | SW_DOLLAR |  |  |  |  |  | .005 | .351@636060 | no | sdone | no |
| Oct 7 4:42 | SW_L_ANR30 | SW_DOLLAR |  |  |  |  |  | .017 | .303@656049 | no | sdone | no |
| Oct 7 4:42 | SW_L_AP44 | SW_DOLLAR |  |  |  |  |  | .012 | .342@661646 | no | sdone | no |
| Oct 7 4:42 | SW_L_AREN21 | SW_DOLLAR |  |  |  |  |  | .035 | .302@686804 | no | sdone | no |
| Oct 7 4:42 | SW_L_AD4 | SW_DOLLAR |  |  |  |  |  | .028 | .147@697346 | no | sdone | no |
| Oct 7 4:42 | SW_L_APIC78 | SW_DOLLAR |  |  |  |  |  | -.012 | .538@707365 own (irtvr -.063 vs bar .215) | no | sdone | no |
| Oct 7 4:42 | SW_L_TSA62 | SW_DOLLAR |  |  |  |  |  | .001 | .217@577441 | no | sdone | no |
| Oct 7 4:42 | SW_L_BSCNCI28 | SW_DOLLAR |  |  |  |  |  | .023 | .553@596206 (irtvr .126 vs bar .353) | no | sdone | no |
| Oct 7 4:42 | SW_L_CS49 | SW_DOLLAR |  |  |  |  |  | -.004 | .454@577441 | no | sdone | no |
| Oct 7 4:42 | SW_L_CAR57 | SW_DOLLAR |  |  |  |  |  | .033 | .599@596206 (irtvr .196 vs bar .353) | no | sdone | no |
| Oct 7 4:42 | SW_L_CL89 | SW_DOLLAR |  |  |  |  |  | .052 | .468@659377 | no | sdone | no |
| Oct 7 4:42 | SW_L_DTL94 | SW_DOLLAR |  |  |  |  |  | .011 | .332@655304 | no | sdone | no |
| Oct 7 4:42 | SW_L_G89 | SW_DOLLAR |  |  |  |  |  | -.035 | .605@687343 (irtvr -.213 vs bar .166) | no | sdone | no |
| Oct 7 4:42 | SW_L_I42 | SW_DOLLAR |  |  |  |  |  | .029 | .546@677624 (irtvr .168 vs bar .263) | no | sdone | no |
| Oct 7 5:13 | SW_L_LTB28 | SW_DOLLAR |  |  |  |  |  | -.024 | .697@578688 (irtvr -.142 vs bar .210) | no | sdone | no |
| Oct 7 5:13 | SW_L_MSAOST52 | SW_DOLLAR |  |  |  |  |  | .006 | .237@596206 | no | sdone | no |
| Oct 7 5:13 | SW_L_OCA32 | SW_DOLLAR |  |  |  |  |  | .023 | .269@654174 | no | sdone | no |
| Oct 7 5:13 | SW_L_OLTL53 | SW_DOLLAR |  |  |  |  |  | .006 | .377@707365 own | no | sdone | no |
| Oct 7 5:13 | SW_L_OSTL84 | SW_DOLLAR |  |  |  |  |  | -.009 | .410@707365 own | no | sdone | no |
| Oct 7 5:13 | SW_L_PRE5 | SW_DOLLAR |  |  |  |  |  | .004 | .549@577441 (irtvr .025 vs bar .138) | no | sdone | no |
| Oct 7 5:13 | SW_L_REAOE16 | SW_DOLLAR |  |  |  |  |  | .002 | .546@577441 (irtvr .012 vs bar .138) | no | sdone | no |
| Oct 7 5:13 | SW_L_STB59 | SW_DOLLAR |  |  |  |  |  | -.005 | .181@631112 | no | sdone | no |
| Oct 7 5:13 | SW_L_TEPC45 | SW_DOLLAR |  |  |  |  |  | -.003 | .302@581701 | no | sdone | no |
| Oct 7 5:13 | SW_L_TL60 | SW_DOLLAR |  |  |  |  |  | .004 | .412@581701 | no | sdone | no |
| Oct 7 5:13 | SW_L_TOPAE77 | SW_DOLLAR |  |  |  |  |  | .000 | .311@578688 | no | sdone | no |
| Oct 7 5:13 | SW_L_APAA29 | SW_DOLLAR |  |  |  |  |  | -.004 | .229@595355 | no | sdone | no |
| Oct 7 5:13 | SW_L_CEPA20 | SW_DOLLAR |  |  |  |  |  | -.004 | .321@655182 | no | sdone | no |
| Oct 7 5:13 | SW_L_CFFA50 | SW_DOLLAR |  |  |  |  |  | -.025 | .602@576233 (irtvr -.122 vs bar .164) | no | sdone | no |
| Oct 7 5:13 | SW_L_CFIA92 | SW_DOLLAR |  |  |  |  |  | .008 | .478@675326 | no | sdone | no |
| Oct 7 5:13 | SW_L_CII91 | SW_DOLLAR |  |  |  |  |  | .025 | .251@586157 | no | sdone | no |
| Oct 7 5:13 | SW_L_DIT73 | SW_DOLLAR |  |  |  |  |  | .024 | .459@668152 | no | sdone | no |
| Oct 7 5:13 | SW_L_DP8 | SW_DOLLAR |  |  |  |  |  | .015 | .434@576233 | no | sdone | no |
| Oct 7 5:13 | REG_PKCC_REV | REG_RANGECC |  |  |  |  |  |  |  |  | sfail | no |
| Oct 7 5:42 | REG_DNBETA_ASYM | REG_DOWNBETA |  |  |  |  |  | -.003 | .559@700992 (irtvr -.011 vs bar .104) | no | sdone | no |
| Oct 7 6:12 | REG_DNBETA_250 | REG_DOWNBETA |  |  |  |  |  | .016 | .621@628834 (irtvr .054 vs bar .192) | no | sdone | no |
| Oct 7 6:12 | ID_TSIZE_SHIFT | ID_TRADESIZE |  |  |  |  |  | .011 | .457@590728 | no | sdone | no |
| Oct 7 6:12 | ID_TSIZE_FLOW | ID_TRADESIZE |  |  |  |  |  | .015 | .344@579357 | no | sdone | no |
| Oct 7 6:12 | ANOM_MAX20 | ANOM_MAX |  |  |  |  |  | .001 | .638@655304 (irtvr .003 vs bar .144) | no | sdone | no |
| Oct 7 6:42 | ANOM_MAX_VOLADJ | ANOM_MAX |  |  |  |  |  | .010 | .741@579357 (irtvr .024 vs bar .198) | no | sdone | no |
| Oct 7 6:42 | A101_002 | A101_VOLPX | .071 | .668 | .087 | .636 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_003 | A101_VOLPX | .052 | .486 | .074 | .625 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_004 | A101_REV | .048 | .701 | .057 | .864 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_006 | A101_VOLPX | .063 | .496 | .089 | .841 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_014 | A101_VOLPX | .061 | .575 | .081 | .767 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_015 | A101_VOLPX | .073 | .670 | .089 | .546 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_018 | A101_REV | .032 | .440 | .048 | .275 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_020 | A101_GAP | .039 | 1.385 | .033 | .546 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_022 | A101_VOLPX | .055 | .831 | .061 | .406 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_026 | A101_VOLPX | .073 | .549 | .098 | .584 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_033 | A101_REV | .034 | 1.349 | .029 | .767 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_034 | A101_REV | .047 | 1.250 | .042 | .647 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_035 | A101_VOLPX | -.048 | 1.414 | -.040 | .633 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_038 | A101_REV | .052 | 1.079 | .050 | .799 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_040 | A101_VOLPX | .043 | .470 | .063 | .779 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_041 | A101_VWAP | .007 | 1.207 | .007 | .677 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_043 | A101_VOLPX | .042 | .965 | .043 | .657 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_044 | A101_VOLPX | .076 | .748 | .087 | .574 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_050 | A101_VWAP | .072 | .411 | .112 | .541 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_053 | A101_RANGE | .068 | 1.520 | .055 | .631 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_054 | A101_RANGE | .111 | 1.381 | .094 | .993 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_055 | A101_RANGE | .060 | .720 | .071 | .668 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_009b | A101_TREND | -.004 | 1.432 | -.003 | .567 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_012b | A101_VOLPX | -.001 | 1.407 | -.001 | .387 | no |  |  |  | fdone | no |
| Oct 7 6:42 | A101_030b | A101_TREND | .062 | .882 | .066 | .674 | no |  |  |  | fdone | no |
| Oct 7 8:12 | SWC_BS9 | SWC |  |  |  |  |  | .063 | .477@578688 | no | sdone | no |
| Oct 7 8:12 | SWC_BS5 | SWC |  |  |  |  |  | .055 | .392@650299 | no | sdone | no |
| Oct 7 8:42 | A101_054_S | A101 |  |  |  |  |  | .112 | .995@629528 (irtvr .095 vs bar .110) | no | sdone | no |
| Oct 7 8:42 | A101_044_S | A101 |  |  |  |  |  | .067 | .602@592314 (irtvr .075 vs bar .091) | no | sdone | no |
| Oct 7 8:42 | SWC_BS9_dl | SWC |  |  |  |  |  | .059 | .439@650299 | no | sdone | no |
| Oct 7 9:13 | A101_050_S | A101 |  |  |  |  |  | .066 | .530@574828 (irtvr .096 vs bar .205) | no | sdone | no |
| Oct 7 9:13 | A101_053_S | A101 |  |  |  |  |  | .074 | .654@631586 (irtvr .060 vs bar .142) | no | sdone | no |
| Oct 7 9:13 | A101_054_acc | A101 |  |  |  |  |  | .137 | .832@629528 (irtvr .137 vs bar .110) | yes | submitted | YES |
| Oct 7 9:13 | A101_054_s5 | A101 |  |  |  |  |  | .075 | .792@560993 (irtvr .092 vs bar .121) | no | sdone | no |
| Oct 7 9:43 | SWC_BS5_acc | SWC |  |  |  |  |  | .077 | .530@630201 (irtvr .407 vs bar .394) | yes | submitted | YES |
| Oct 7 9:43 | SWC_BS7 | SWC |  |  |  |  |  | .057 | .814@716550 own (irtvr .335 vs bar .488) | no | sdone | no |
| Oct 7 9:43 | A101_054_s5acc | A101 |  |  |  |  |  | .105 | .724@678835 (irtvr .151 vs bar .220) | no | sdone | no |
| Oct 7 10:15 | SWC_BS7_acc | SWC |  |  |  |  |  | .075 | .901@716550 own (irtvr .404 vs bar .488) | no | sdone | no |
| Oct 7 10:42 | SW_L_NCICC44 | SW_DOLLAR |  |  |  |  |  | .004 | .471@672147 | no | sdone | no |
| Oct 7 10:42 | SW_L_CFNI877 | SW_DOLLAR |  |  |  |  |  | .014 | .739@576233 (irtvr .066 vs bar .164) | no | sdone | no |
| Oct 7 10:42 | SW_L_IAOACF3 | SW_DOLLAR |  |  |  |  |  | -.036 | .461@696794 | no | sdone | no |
| Oct 7 10:42 | SW_L_ANIARD21 | SW_DOLLAR |  |  |  |  |  | -.020 | .325@695618 | no | sdone | no |
| Oct 7 10:42 | SW_L_COGSTFD21 | SW_RATIO |  |  |  |  |  | .005 | .499@656049 | no | sdone | no |
| Oct 7 10:42 | A101_050_acc | A101 |  |  |  |  |  | .102 | .644@619187 (irtvr .170 vs bar .330) | no | sdone | no |
| Oct 7 11:12 | SW_L_DED58 | SW_PERSHARE |  |  |  |  |  | .023 | .625@595932 (irtvr .097 vs bar .180) | no | sdone | no |
| Oct 7 11:12 | SW_L_DPSF20 | SW_PERSHARE |  |  |  |  |  | .014 | .402@589260 | no | sdone | no |
| Oct 7 11:12 | SW_L_BED3D | SW_PERSHARE |  |  |  |  |  | .025 | .638@595932 (irtvr .106 vs bar .180) | no | sdone | no |
| Oct 7 11:12 | SW_L_GAAEB41 | SW_DOLLAR |  |  |  |  |  | -.002 | .381@581701 | no | sdone | no |
| Oct 7 11:42 | SW_L_ITEDAF | SW_DOLLAR |  |  |  |  |  | .033 | .542@576233 (irtvr .171 vs bar .164) | no | sdone | no |
| Oct 7 11:42 | SW_L_IE6AD | SW_DOLLAR |  |  |  |  |  | -.016 | .475@581701 | no | sdone | no |
| Oct 7 11:42 | SW_L_OPDOB72 | SW_DOLLAR |  |  |  |  |  | .010 | .111@672941 | no | sdone | no |
| Oct 7 12:18 | SW_L_PE397 | SW_DOLLAR |  |  |  |  |  | .013 | .232@627389 | no | sdone | no |
| Oct 7 12:18 | SW_L_MNCIC6EE | SW_DOLLAR |  |  |  |  |  | .010 | .121@709310 | no | sdone | no |
| Oct 7 12:18 | SW_L_MNCIB9B | SW_DOLLAR |  |  |  |  |  | -.009 | .133@699632 | no | sdone | no |
| Oct 7 12:43 | SW_D_AOCI603 | SW_DOLLAR |  |  |  |  |  | -.007 | .150@688740 | no | sdone | no |
| Oct 7 12:43 | SW_D_AOIA8BA | SW_DOLLAR |  |  |  |  |  | .011 | .180@640295 | no | sdone | no |
| Oct 7 12:43 | SW_D_DTALT3BF | SW_DOLLAR |  |  |  |  |  | -.003 | .100@711661 | no | sdone | no |
| Oct 7 12:43 | SW_D_DAE29 | SW_DOLLAR |  |  |  |  |  | -.019 | .193@684336 own | no | sdone | no |
| Oct 7 12:43 | SW_D_EOERCO6B3 | SW_DOLLAR |  |  |  |  |  | .013 | .152@578055 | no | sdone | no |
| Oct 7 12:43 | SW_D_STI1A3 | SW_DOLLAR |  |  |  |  |  | -.007 | .198@579357 | no | sdone | no |
| Oct 7 12:43 | SW_D_TOE2EF | SW_DOLLAR |  |  |  |  |  | -.002 | .138@668115 | no | sdone | no |
| Oct 7 12:43 | SW_D_ANR53B | SW_DOLLAR |  |  |  |  |  | -.029 | .133@720184 | no | sdone | no |
| Oct 7 12:43 | SW_D_AP8F9 | SW_DOLLAR |  |  |  |  |  | .008 | .281@709379 | no | sdone | no |
| Oct 7 12:43 | SW_D_APICA4C | SW_DOLLAR |  |  |  |  |  | -.012 | .287@581701 | no | sdone | no |
| Oct 7 12:43 | SW_D_TSA107 | SW_DOLLAR |  |  |  |  |  | .007 | .209@601796 | no | sdone | no |
| Oct 7 12:43 | SW_L_NIBMIAB2 | SW_DOLLAR |  |  |  |  |  | .005 | .679@576233 (irtvr .027 vs bar .164) | no | sdone | no |
| Oct 7 13:12 | SW_D_BSCNCIBA8 | SW_DOLLAR |  |  |  |  |  | .049 | .558@679993 (irtvr .203 vs bar .280) | no | sdone | no |
| Oct 7 13:12 | N_GLDHEDGE | MACRO |  |  |  |  |  | .005 | .265@618945 | no | sdone | no |
| Oct 7 13:12 | N_OILRESP | MACRO |  |  |  |  |  |  |  |  | sfail | no |
| Oct 7 13:12 | N_GDPBETA | MACRO |  |  |  |  |  |  |  |  | sfail | no |
