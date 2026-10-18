# Portal stats collected for the deck (Slow OS, from Abhinav's screenshots, Oct 18)

| ID | Tag | Family | Period | IR | TVR | DD | Ret | IR/sqrt(TVR) | NumStks | Lookback |
|---|---|---|---|---|---|---|---|---|---|---|
| 673000 | P_VWAPT | A start | 2008-02-01..2021-12-30 | .083 | 1.047 | 12.5 | .082 | .081 | 539 | 55 |
| 705948 | R_RIAwk | A weekly | 2007-03-15..2021-12-30 | .080 | .248 | 11.7 | .059 | .161 | 747 | 300 |
| 708808 | Y_PLsz_ACC_w16 | A final (submitted) | 2006-07-25..2021-12-30 | .118 | .624 | 6.2 | .074 | .149 | 708 | 140 |
| 678911 | S_LATEVOL_sbc_iss_fcf_w2 | C start | 2006-07-25..2021-12-30 | .075 | .540 | 17.7 | .068 | .102 | 639 | 140 |
| 684336 | T_LATE_w3 | C first submission | 2006-07-25..2021-12-30 | .073 | .486 | 17.7 | .067 | .105 | 639 | 140 |

P_VWAPT code (from the portal screenshot; not in the repo before):
```
g = ts_mean((close - vwap_last_hour)/vwap_last_hour, 5)   # 5-day avg close-vs-VWAP gap
busy = cs_rank(number_of_trades_last_hour/ts_mean(number_of_trades_last_hour, 20)) > 1.3   # unusually many last-hour trades
alpha = at_zero2nan(-cs_rank(g) * busy)   # fade the gap only on busy closes
```

Observations from the PnL curves:
- A: P_VWAPT rises steadily after a 2008 dip. R_RIAwk is flat 2008-10, then trends, with a 2020 drawdown and a sharp 2021 recovery. The final (#708808) has the smoothest curve: drawdown 6.2 versus 12.5 for the start, and no flat stretch longer than about a year.
- C: S_LATEVOL and T_LATE_w3 have almost the same curve. Most of their PnL came in 2008-09 and 2011, they are roughly flat from mid-2014 to 2020, and they have deep 2019-20 drawdowns (DD 17.7). The thesis worked mainly in high-volatility regimes, so present C as a crisis-alpha family, or replace it.
