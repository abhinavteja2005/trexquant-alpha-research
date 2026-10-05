# Idea backlog (attach a real, opened source URL when an idea is queued)

Status: idea | queued | tested-pass | tested-fail | dropped

## Reversal bases
- INTRA: last-hour composite (return, range position, VWAP gap). Taken alone (corr .649). queued in blends
- VWAPV: VWAP gap where volume is elevated. Best Fast blend (corr .476), but failed in Slow
- RETL (last-hour return): queued. OVN, D3, RANGE: tested-fail (Fast IR .060-.067)

## Slow companions
- rnd (R&D/mktcap), sbc (stock-based pay/mktcap), fcf (FCF yield), gpa (gross profitability), iss (net issuance). Reliability in Slow is unknown; diagnose first.
- earn: dropped (possible look-ahead)

## To research
- 101 Formulaic Alphas (https://arxiv.org/pdf/1601.00991): translate the OHLCV/vwap ones (vwap -> vwap_last_hour)
- Overnight vs intraday tug of war (Lou, Polk & Skouras 2019): queued as TUGOFWAR
- Sub-industry lead-lag momentum: queued as SUBIND_MOM
- Intraday volatility, skew, trade-size and information-ratio variables: mostly untested
- Volume-spike conditioned drift (a post-earnings-drift proxy without the earnings-date variable)
- Value composites from the ratio group (earnings_yield, ev_to_t12m_ebit, price_to_book_ratio)
