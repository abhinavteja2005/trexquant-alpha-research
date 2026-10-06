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
