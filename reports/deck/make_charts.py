# Redraws the Trexsim PnL curves (digitized from the portal screenshots, calibrated with
# the portal's own Ret and period: final cum PnL = Ret x years, start = 0) in one consistent style.
import json, datetime as dt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as mdates

D = json.load(open("digitized.json"))
INK, MUTED, GRID = "#1F2937", "#6B7280", "#E5E7EB"
FAM = {"A": "#d9480f", "B": "#2a78d6", "C": "#1baf7a", "D": "#eda100"}
GREYS = ["#9CA3AF", "#B8BEC7", "#CBD0D7"]
IR = {"673000": .083, "705948": .080, "707365": .085, "708808": .118, "715966": .137, "724045": .129,
      "684336": .073, "685104": .092, "679831": .067, "685741": .083, "716550": .077, "678911": .075}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID,
                     "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})

def series(i, risk=False):
    t = [dt.date.fromisoformat(x) for x in D[i]["t"]]
    v = D[i]["v"]
    if risk:  # equal-volatility scaling: final value = daily IR x trading days (cum PnL in units of daily sigma)
        n = (t[-1] - t[0]).days / 365.25 * 252
        k = IR[i] * n / v[-1]; v = [x * k for x in v]
    return t, v

def style(ax):
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.xaxis.set_major_locator(mdates.YearLocator(2)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_ylabel("Cumulative PnL ($M)")
    ax.set_xlim(dt.date(2006, 6, 1), dt.date(2023, 9, 1))

def label_end(ax, t, v, text, color, ypos=None):
    ax.plot([t[-1]], [v[-1]], "o", ms=4, color=color, mec="white", mew=1.2, zorder=5)
    ax.annotate(text, (t[-1], v[-1] if ypos is None else ypos), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=8, color=INK, annotation_clip=False)

def spread(vals, gap):  # push end labels apart so they never collide
    order = sorted(range(len(vals)), key=lambda k: vals[k]); out = list(vals)
    for a, b in zip(order, order[1:]):
        if out[b] - out[a] < gap: out[b] = out[a] + gap
    return out

def family(name, others, best, fname, dys=None):
    fig, ax = plt.subplots(figsize=(10.5, 2.75), dpi=200)
    ids = others + [best]; S = {i: series(i, risk=True) for i in ids}
    top = max(max(S[i][1]) for i in ids)
    ys = spread([S[i][1][-1] for i in ids], top * 0.075)
    for k, i in enumerate(others):
        t, v = S[i]
        ax.plot(t, v, color=GREYS[k], lw=1.2, label=f"#{i} (IR {IR[i]:.3f})")
        label_end(ax, t, v, f"#{i}", GREYS[k], ys[k])
    t, v = S[best]
    ax.plot(t, v, color=FAM[name], lw=2.0, label=f"#{best} best in family (IR {IR[best]:.3f})", zorder=4)
    label_end(ax, t, v, f"#{best}  BEST", FAM[name], ys[-1])
    ax.axvspan(dt.date(2017, 1, 1), dt.date(2021, 12, 30), color="#F3F4F6", zorder=0, lw=0)
    ax.text(dt.date(2019, 7, 1), 0.02, "recent 5y (2017-21)", transform=ax.get_xaxis_transform(),
            ha="center", va="bottom", fontsize=7, color=MUTED)
    style(ax); ax.set_ylabel("Cum. PnL, equal-risk scale\n(units of daily $\\sigma$)")
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(f"charts/{fname}.png"); plt.close(fig)

family("A", ["673000", "705948", "707365"], "708808", "famA")
family("B", ["715966"], "724045", "famB")
family("C", ["684336"], "685104", "famC")
family("D", ["679831", "685741"], "716550", "famD")

fig, ax = plt.subplots(figsize=(6.6, 4.2), dpi=200)
finals = [("A", "708808"), ("B", "724045"), ("C", "685104"), ("D", "716550")]
ends = spread([series(i)[1][-1] for _, i in finals], 0.07)
for (f, i), y in zip(finals, ends):
    t, v = series(i)
    ax.plot(t, v, color=FAM[f], lw=1.8, label=f"{f}  #{i}")
    label_end(ax, t, v, f"{f}", FAM[f], y)
style(ax); ax.xaxis.set_major_locator(mdates.YearLocator(3)); ax.set_xlim(dt.date(2006, 6, 1), dt.date(2023, 3, 1))
ax.legend(loc="upper left", frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig("charts/finals.png"); plt.close(fig)
print("ok")
