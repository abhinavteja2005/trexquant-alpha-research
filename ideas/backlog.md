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

## Oct 5 late: price/intraday-only batch (queued at the front, tag prefix P_)
Insider-trading data does not exist on Trexsim; the closest public proxies are issuance (shsout) and stock-based pay, already used as companions.
- P_CI_s3, P_CI_volcond, P_CI_lowvol: INTRA composite smoothed / volume-conditioned / calm stocks only (Bogousslavsky & Muravyev 2023; Nagel 2012)
- P_VWAPV_s3, P_VWAPV_sub, P_VWAPV_illiq, P_VWAPT: VWAP-gap reversal variants (Campbell-Grossman-Wang 1993; Amihud 2002)
- P_RETL_small: last-hour reversal in small-trade (retail-like) stocks (Barber, Odean & Zhu 2009)
- P_RANGE_volcond: last-hour range position on heavy volume
- P_A101: Alpha #101 (Kakushadze 2016, https://arxiv.org/abs/1601.00991)
- P_FIRST_LAST: long first-hour, short last-hour return (Gao, Han, Li & Zhou 2018)
Plan: anything with Fast IR >= .078 and corr <= .55 auto-promotes to Slow (no ts_fill, so short lookback and quick Slow runs).

## Oct 5 22:05: volatility batch (tag prefix V_, queued after P_)
No single-stock implied vol on Trexsim; VIX (close_vix, ret1_vix) and realized-vol inputs exist.
- V_RSJ: signed jump variation, short good-vol (Bollerslev, Li & Zhao, JFQA 2020)
- V_RSKEW: intraday realized skewness (Amaya, Christoffersen, Jacobs & Vasquez, JFE 2015)
- V_VIXBETA: aggregate-volatility (VIX) beta (Ang, Hodrick, Xing & Zhang, JF 2006)
- V_VOLSHOCK: 5d/60d realized variance spike
- V_LATEVOL_REV: last-hour reversal where the close is more volatile than the open
Slow-ish signals (VIXBETA, RSKEW, RSJ) are candidate blend partners for the reversal base if their PnL is uncorrelated.

## Cycle 1 (local master): vol-premium and regime proxies
Format: name | thesis | source URL | variables | horizon | sign | why uncrowded. Drafts in `alphas/drafts/c1.json` (base C1). Not duplicating V_RSJ/V_RSKEW/V_VIXBETA/V_VOLSHOCK/V_LATEVOL_REV.
- VP_VOLOFVOL | uncertainty about risk (vol of rolling vol) is priced: high vol-of-vol underperforms (~8%/yr) | https://ideas.repec.org/a/cup/jfinqa/v53y2018i04p1615-1651_00.html | ret1; std_dev_return_first/last_hour | weeks-months | short high vov | second moment of vol, not a return signal; intraday variant uses untested hour-std data
- VP_COSKEW | stocks that rise when the market makes big moves (long-gamma-like, positive coskewness) are overpriced; skew premium ~3.6%/yr | https://people.duke.edu/~charvey/Research/Published_Papers/P56_Conditional_skewness_in.pdf | ret1, ret1_spx | months | long negative coskew | ts_corr_binary(ret1, ret1_spx^2) is a slow risk tilt with no reversal content
- VP_RESREV_VIX | reversal = liquidity provision, whose return rises with VIX (Nagel 2012); apply to beta-residual returns and tilt toward high idio-vol names only in high-VIX regimes | https://econpapers.repec.org/RePEc:oup:rfinst:v:25:y:2012:i:7:p:2005-2039 | ret1, ret1_spx, close_vix | 3 days | fade residual | VIX changes the cross-sectional weights (not the book scale); residual 3d is less crowded than raw 1-5d. Critic: highest risk of pool corr in this batch
- REG_VARRATIO | Lo-MacKinlay variance ratio (var(ret5)/5var(ret1)) labels each stock trending vs mean-reverting: momentum in high-VR, reversal in low-VR, NaN in between | https://www.nber.org/papers/w2168 | ret1, ret5, ret10 | 5-10 days | sign flips by regime | sign-flipping by regime decorrelates from plain reversal (half the book is momentum)
- REG_RANGECC | Parkinson range variance (log(high/low)^2/4ln2) above close-to-close variance means intraday noise that reverts; reverse only those names | https://www.nber.org/papers/w2168 | high, low, ret1, ret5 | 5 days | fade, gated | gate keeps ~half the universe; range/close-vol ratio not used elsewhere
- REG_DOWNBETA | downside beta (comovement on market down days) earns ~6%/yr; asymmetry (down minus up corr) or excess downside beta | https://www.nber.org/papers/w11824 | ret1, ret1_spx | months | long downside beta | slow risk premium, candidate blend companion, unrelated to reversal
- ID_TRADESIZE | small-trade (retail) favored stocks underperform for months; proxy with falling average trade size and small-trade-weighted first-hour returns | https://econpapers.repec.org/article/ouprfinst/v_3a21_3ay_3a2008_3ai_3a3_3ap_3a1123-1151.htm | volume_first/last_hour, number_of_trades_first/last_hour, return_first_hour | weeks | short retail-favored | trade-count data barely used by the pool
- ANOM_MAX | lottery demand: max daily return over the past month predicts low returns (>1%/month spread); vol-adjusted variant separates spikes from plain vol | https://pages.stern.nyu.edu/~rwhitela/papers/max%20jfe11.pdf | ret1 | month | short high MAX | sourced anomaly, not in backlog; 52-week-high card skipped (source page not openable)

## Oct 5 23:55: Slow-only round 2 (queued, lb 300)
- S_COMP5_slow: rnd+sbc+iss+fcf+gpa composite alone (low TVR; tests IR/sqrtTVR route)
- S_CI_sbc_iss_fcf_w2: INTRA composite base + sbc/iss/fcf at 2x (10 vars)
- S_BL1_subind: best blend (IR .090, corr .72) made sub-industry relative
- S_VWAPT_vol_iss: VWAPT + RSJ + VIX beta + issuance at 1.5x (non-fundamental partners)
- S_LATEVOL_sbc_iss_fcf_w2: volatile-close reversal base + sbc/iss/fcf at 2x

## Oct 6 00:55: night batch Q_ (Slow, new families; drafts in alphas/drafts/oct6-night.json)
52-week high (George & Hwang 2004), frog-in-the-pan momentum (Da, Gurun & Warachka 2014), overnight-vs-intraday tug of war (Lou, Polk & Skouras 2019), high-volume return premium (Gervais, Kaniel & Mingelgrin 2001), value x quality interaction (Piotroski 2000; Asness, Frazzini & Pedersen 2019), accruals + asset growth (Sloan 1996; Cooper, Gulen & Schill 2008), betting against beta (Frazzini & Pedersen 2014), MAX gated by retail trade size (Bali, Cakici & Whitelaw 2011; Kumar 2009), sub-industry lead-lag for small caps (Hou 2007), EPS-change drift (Bernard & Thomas 1989).

## Cycle 2 (scrape, Oct 6 evening)
Scout: 12 cards. Aim: low-turnover or anti-reversal PARTNERS on uncrowded inputs. All sketches are dtype-safe (flags cast with float32 ones, no bool - bool), dimensionless, windows/lags from the allowed sets. lb = suggested Slow lookback (max 300). "(search)" = source seen only in search results (arxiv/ssrn/quantpedia/alphaarchitect/nber/cepr PDFs blocked here). Families: LIQ 2, MOMX 4, HR 2, FUND 3, PV 1.

### LIQ_TURNCV Variability of trading activity
- Thesis: stocks whose trading volume is erratic (high coefficient of variation) earn LOWER returns, after controlling for the volume level (Chordia et al. expected the opposite and found a strong negative effect). Steady-volume names are cheaper.
- Source: Chordia, Subrahmanyam & Anshuman, "Trading activity and expected stock returns", JFE 2001, https://repository.iimb.ac.in/handle/2074/11853 (search); qlib Alpha158 VSTD/WVMA features (Std(volume)/volume; Std(|ret|*volume)/Mean(|ret|*volume)), https://github.com/microsoft/qlib/blob/main/qlib/contrib/data/loader.py (opened)
- Variables (2): volume, shsout
- Horizon/windows: months; 60, 20. lb 100
- Sign: negative (short high CV)
- Why uncrowded / partner role: a second moment of liquidity, not a return signal, so ~0 overlap with reversal. Very low TVR, so it passes the IR/sqrt(TVR) test easily. A slow partner. Variant: WVMA (CV of |ret1|*volume, +ret1).
- Sketch:
```
cv = ts_std(volume, 60)/ts_mean(volume, 60)  # coefficient of variation of daily volume (dimensionless)
lvl = ts_mean(volume/shsout, 60)  # turnover level: the control CSA use
alpha = cs_factorneut(-cs_zscore(ts_mean(cv, 20)), [cs_zscore(lvl)])  # short erratic-trading names beyond their turnover level
```

### LIQ_ILLIQSHOCK Liquidity-shock underreaction
- Thesis: the market underreacts to stock-level liquidity shocks. A drop in Amihud illiquidity versus the stock's own norm predicts return CONTINUATION for up to 6 months (0.70-1.20%/month long-short), driven by inattention.
- Source: Bali, Peng, Shen & Tang, "Liquidity Shocks and Stock Market Reactions", RFS 2014, https://ideas.repec.org/a/oup/rfinst/v27y2014i5p1434-1485..html (search)
- Variables (3): ret1, volume, close
- Horizon/windows: 1-6 months; 20 vs 250. lb 270
- Sign: negative on the illiquidity ratio (long names whose liquidity improved)
- Why uncrowded / partner role: price-impact dynamics rather than a return level. Shocks coincide with positive same-month returns and then continue, so the signal should load AGAINST 20-day reversal: an anti-reversal partner. Distinct from the dead high-volume premium, because it is impact per dollar traded, not raw volume.
- Sketch:
```
il = abs(ret1)/(volume*close + 1)  # Amihud price impact per dollar traded today
shock = ts_mean(il, 20)/ts_mean(il, 250)  # this month's illiquidity vs own 1-year norm (ratio: dimensionless, split-safe)
alpha = -cs_rank(shock)  # long improving liquidity, short drying-up liquidity
```

### MOMX_STMOM_HITURN Short-term momentum in high-turnover stocks
- Thesis: sorted on last month's return and turnover, low-turnover stocks reverse but HIGH-turnover stocks show short-term MOMENTUM. That momentum is as profitable and persistent as 12-1 momentum and strongest in the largest, most liquid names (our TOP1000). Traders underweight the information in prices.
- Source: Medhat & Schmeling, "Short-term Momentum", RFS 2022, https://repec.cepr.org/repec/cpr/ceprdp/DP15857.pdf (search)
- Variables (4): close, ret20, volume, shsout
- Horizon/windows: 1 month; 20. lb 40
- Sign: positive on ret20 within the top-turnover bucket
- Why uncrowded / partner role: by construction a continuation bet that is negatively correlated with the crowded 1-5 day reversal pool. The best direct partner for U_PRICE2_szvo / VWAPT-type bases. Variant B is the full double sort, `cs_zscore(ret20)*(cs_rank(turn) - 1.5)`; its low-turnover reversal half may be crowded.
- Sketch:
```
f = close/close  # float32 ones for the flag cast
turn = ts_mean(volume/shsout, 20)  # last month's share turnover (dimensionless)
hi = f*(cs_rank(turn) > 1.8)  # top-20% turnover flag
alpha = at_zero2nan(cs_zscore(ret20)*hi)  # follow last month's return in the most-traded names only
```

### MOMX_HIVOL_MOM6 Momentum where volatility is high
- Thesis: momentum and reversal coexist among large stocks. High-volatility large caps show momentum and low-volatility large caps show reversal. Trade 6-month momentum (skip the last week) only in the high-vol group.
- Source: Wei, "Do momentum and reversals coexist?", via the awesome-systematic-trading implementation https://github.com/paperswithbacktest/awesome-systematic-trading/blob/main/static/strategies/momentum-and-reversal-combined-with-volatility-effect-in-stocks.py (opened); https://quantpedia.com/strategies/momentum-and-reversal-combined-with-volatility-effect-in-stocks (search)
- Variables (1): ret1
- Horizon/windows: 6 months, skipping 1 week; 120, lag 5. lb 140
- Sign: positive on momentum in high-vol names
- Why uncrowded / partner role: a low-TVR continuation bet, so an anti-reversal partner. It differs from MO1 (residual 12-1) and MO3 (volume-confirmed 12-1) in horizon and in the volatility conditioning. Risk: the 2009 momentum crash hits high-vol momentum hardest; check the best-year share.
- Sketch:
```
f = ret1*0 + 1  # float32 ones
mom = ts_delay(ts_sum(ret1, 120), 5)  # 6-month return skipping the last week (sum of daily returns, split-safe)
hv = f*(cs_rank(ts_std(ret1, 120)) > 1.6)  # top-40% 6-month volatility flag
alpha = at_zero2nan(cs_zscore(mom)*hv)  # momentum only where it lives (high vol); low-vol names would reverse
```

### MOMX_SEASON_1Y Same-window-last-year seasonality
- Thesis: stocks tend to earn relatively high (or low) returns in the same calendar month every year, at annual lags up to 20 years. This sits on top of momentum and reversal and holds across industries and sizes, independent of earnings announcements. With lb <= 300 only the 1-year lag fits.
- Source: Heston & Sadka, "Seasonality in the cross-section of stock returns", JFE 2008, https://rhsmith.umd.edu/news/seasonality-stock-market-returns (search); implementation https://github.com/paperswithbacktest/awesome-systematic-trading/blob/main/static/strategies/12-month-cycle-in-cross-section-of-stocks-returns.py (opened)
- Variables (1): ret20
- Horizon/windows: 1 month; ret20 at lag 240 (120+120). lb 280
- Sign: positive
- Why uncrowded / partner role: its information is a year old, so it is orthogonal to all reversal/VWAP families and to fundamentals. Expect a weak IR alone (~.02-.03): a pure diversifier in blends. Variant: lag 230 (nested 120+60+40+10) targets the COMING 20 days of last year.
- Sketch:
```
s = ts_delay(ts_delay(ret20, 120), 120)  # 20-day return ending 240 days ago: window centred on this date one year ago
alpha = cs_rank(s)  # long names that did well in this calendar window last year
```

### MOMX_VALMOM_AMP Value plus momentum, 50/50
- Thesis: value and momentum premia exist everywhere and are NEGATIVELY correlated with each other, so an equal-risk combination has a much higher Sharpe than either. Use EBIT/EV as the value leg (more robust than B/M in 2008-2021). The portal's industry neutralisation makes it within-industry value.
- Source: Asness, Moskowitz & Pedersen, "Value and Momentum Everywhere", JF 2013, https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf (search)
- Variables (2): ebit_yield, ret1
- Horizon/windows: 6-1 months (AMP use 12-1, but 250 + ts_fill trips the 300 cap: checker estimated ~340); 120, 20. lb 210
- Sign: positive on both legs
- Why uncrowded / partner role: additive, not the dead value x quality interaction. Both legs are slow (TVR ~.05). The momentum leg is anti-reversal. Risk: value was weak in 2008-2021, so run it once and keep it only if IR > .03 or it is negatively correlated with U_PRICE2_szvo.
- Sketch:
```
mom = ts_sum(ret1, 120) - ts_sum(ret1, 20)  # 6-1 month momentum, split-safe
val = ts_fill(ebit_yield)  # EBIT / EV value measure
alpha = cs_zscore(cs_rank(val)) + cs_zscore(cs_rank(mom))  # equal-weight value + momentum
```

### HR_HKS_PERIOD Intraday periodicity (same-hour continuation)
- Thesis: returns in a given intraday interval CONTINUE at lags that are exact multiples of a trading day, for at least 40 days. The cause is institutional flows that trade at the same time each day; volume, order imbalance and spreads do not explain it. Tomorrow's first and last hours sit inside our close-to-close hold, so past first-hour and last-hour returns (skipping the reversal week) predict them.
- Source: Heston, Korajczyk & Sadka, "Intraday Patterns in the Cross-section of Stock Returns", JF 2010, https://ideas.repec.org/a/bla/jfinan/v65y2010i4p1369-1407.html (search)
- Variables (2): return_first_hour, return_last_hour
- Horizon/windows: days 5-44; 40, lag 5. lb 60
- Sign: positive
- Why uncrowded / partner role: uses hour-bar returns with a continuation sign over a 40-day memory. The pool's last-hour signals are 1-5 day reversals, and skipping lag 0-4 avoids them. An anti-reversal partner with modest TVR.
- Sketch:
```
a = ts_delay(ts_mean(return_first_hour, 40), 5)  # avg first-hour return over days t-44..t-5
b = ts_delay(ts_mean(return_last_hour, 40), 5)  # same for the last hour
alpha = cs_zscore(a) + cs_zscore(b)  # tomorrow's first/last hour repeat these same-hour patterns
```

### HR_IR_PERSIST Smooth-drift persistence (split institutional orders)
- Thesis: institutions execute large orders as multi-day packages whose price impact keeps building. Those algorithms leave a smooth, one-directional intra-hour price path, which shows up as a high signed information ratio. A persistent signed hour-IR, beyond what the 10-day return already shows, marks an unfinished package that will keep pushing the price.
- Source: Chan & Lakonishok, "The Behavior of Stock Prices around Institutional Trades", JF 1995, https://ideas.repec.org/a/bla/jfinan/v50y1995i4p1147-74.html (search); mechanism also in Heston-Korajczyk-Sadka 2010 (above)
- Variables (3): information_ratio_first_hour, information_ratio_last_hour, ret10
- Horizon/windows: 1-2 weeks; 10. lb 30
- Sign: positive
- Why uncrowded / partner role: the information-ratio variables are barely used (only as |IR| in MM1), and this uses the signed value. Orthogonalising to ret10 removes the reversal exposure by construction. A fast partner that should be negatively correlated with VWAP-gap reversal.
- Sketch:
```
irp = ts_mean(information_ratio_first_hour + information_ratio_last_hour, 10)  # 2-week avg signed intra-hour drift quality
alpha = cs_factorneut(cs_zscore(irp), [cs_zscore(ret10)])  # smooth one-way drift beyond the 10-day return itself
```

### FUND_OPLEV Operating leverage
- Thesis: firms with high operating costs relative to assets (COGS + SG&A over total assets) have more operating leverage, so riskier cash flows and higher expected returns. Within industries this explains much of the value premium.
- Source: Novy-Marx, "Operating Leverage", Review of Finance 2011, https://ideas.repec.org/a/oup/revfin/v15y2011i1p103-134.html (search)
- Variables (4): net_sales, operating_income, total_assets, gross_profit
- Horizon/windows: quarters; ts_fill only. lb 260
- Sign: positive
- Why uncrowded / partner role: a cost-structure LEVEL that none of our companions use (rnd, sbc, fcf, gpa, iss, accruals, fundamental changes). It is neutralised to gross profitability to keep it off the saturated GP family. Near-zero TVR makes it a slow partner.
- Sketch:
```
ta = ts_fill(total_assets)  # latest total assets
oc = (ts_fill(net_sales) - ts_fill(operating_income))/ta  # operating costs (COGS + SG&A) per dollar of assets
alpha = cs_factorneut(cs_zscore(oc), [cs_zscore(ts_fill(gross_profit)/ta)])  # operating leverage beyond gross profitability
```

### FUND_ORGCAP Organization capital (SG&A intensity)
- Thesis: SG&A-built organization capital (key talent with firm-specific efficiency) is risky for shareholders. Firms with more of it than industry peers outperform by about 4.7%/yr, not explained by CAPM, FF3 or Carhart.
- Source: Eisfeldt & Papanikolaou, "Organization Capital and the Cross-Section of Expected Returns", JF 2013, https://www.tse-fr.eu/sites/default/files/medias/stories/SEMIN_09_10/FINANCE/eisfeldt.pdf (search)
- Variables (2): sell_and_admin_exp_to_net_sales_ratio, sales_to_total_assets_ratio
- Horizon/windows: quarters; 120 (smoothed flow as a stock proxy). lb 260
- Sign: positive (relative to industry; the portal neutralises)
- Why uncrowded / partner role: SG&A is unused (R&D/mktcap is the saturated one, and this is scaled by assets, not price). It is neutralised to asset turnover so it is not a sales-scale bet. Correlation with FUND_OPLEV is expected to be moderate; if both pass, blend rather than submit twice.
- Sketch:
```
at = ts_fill(sales_to_total_assets_ratio)  # asset turnover
sga = ts_fill(sell_and_admin_exp_to_net_sales_ratio)*at  # SG&A / assets: flow proxy for organization capital
alpha = cs_factorneut(cs_zscore(ts_mean(sga, 120)), [cs_zscore(at)])  # SG&A intensity beyond plain asset turnover
```

### FUND_TAXMOM Tax-expense momentum
- Thesis: the seasonally differenced (year-over-year) change in tax expense carries information about core profitability beyond reported earnings. Prices absorb it with a delay, so it predicts returns positively over the next two quarters, separately from size, B/M, accruals and momentum.
- Source: Thomas & Zhang, "Tax Expense Momentum", Journal of Accounting Research 2011, https://ideas.repec.org/a/bla/joares/v49y2011i3p791-821.html (search)
- Variables (2): income_tax_expense_year_growth_pct, pretax_income_year_growth_pct
- Horizon/windows: 1-2 quarters; ts_fill only. lb 260
- Sign: positive
- Why uncrowded / partner role: tax data is unused. Neutralising to pre-tax income growth keeps only the taxable-vs-book-income news, so it is not the dead EPS drift and not in FMOM5 (dROA, dCFO, leverage, turnover, margin). A slow partner; check own-correlation with #695151 before blending.
- Sketch:
```
g = cs_rank(ts_fill(income_tax_expense_year_growth_pct))  # YoY tax-expense growth, ranked to tame small bases
p = cs_rank(ts_fill(pretax_income_year_growth_pct))  # YoY pre-tax book-income growth
alpha = cs_factorneut(cs_zscore(g), [cs_zscore(p)])  # tax news beyond book-income news
```

### PV_CORD Return / volume-change correlation (qlib CORD)
- Thesis: when rallies come with volume surges and declines with volume drops (high corr(return, d log volume)), buying is attention- or hedging-driven, and such price moves get unwound. Llorente et al.: returns from risk-sharing trades reverse while speculative ones continue. CORD is one of the strongest Alpha158 features.
- Source: qlib Alpha158 CORD = Corr($close/Ref($close,1), Log($volume/Ref($volume,1)+1), d), https://github.com/microsoft/qlib/blob/main/qlib/contrib/data/loader.py (opened); Llorente, Michaely, Saar & Wang, "Dynamic Volume-Return Relation of Individual Stocks", RFS 2002, https://www.johnhcochrane.com/s/llorente_michaely_saar_wang_volume_rfs.pdf (search)
- Variables (2): ret1, volume
- Horizon/windows: weeks; 60 (variant 20). lb 80
- Sign: negative (as in qlib's evidence; screen both signs in Fast, since the US sign is unverified)
- Why uncrowded / partner role: a co-movement statistic, not a return level, so its overlap with the reversal pool should be low. Moderate TVR (60-day correlation). `at_signlog` is exactly qlib's Log(x+1).
- Sketch:
```
dv = at_signlog(volume/ts_delay(volume, 1))  # log(1 + volume ratio), as in qlib
cord = ts_corr_binary(ret1, dv, 60)  # 3-month correlation of daily return with volume change
alpha = -cs_rank(cord)  # short names whose rallies come with volume surges
```
