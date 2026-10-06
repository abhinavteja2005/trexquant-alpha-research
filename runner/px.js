// PX: in-page daily-PnL helpers for the Trexsim tab (read-only; never starts simulations, never touches R.cfg).
// Paste once into the runner tab, then call e.g. PX.own('TAG'), PX.blend([['A',1],['B',2]]), PX.pair('A','B').
// Uses each job's Slow result id (j.sid). Correlation = Pearson on daily PnL over the last 500 common days,
// the same window the portal uses. Caches PnL in memory (PX.cache); fetch at most ~6 new ids per call.
(function () {
  const PX = (window.PX = window.PX || {});
  PX.cache = PX.cache || {};
  const job = (tag) => window.R.jobs.find((j) => j.tag === tag);
  PX.pnl = function (id) {
    if (PX.cache[id]) return PX.cache[id];
    const x = new XMLHttpRequest();
    x.open('GET', '/trexsim/pysim/alpha/' + id + '/?format=json', false);
    x.send();
    if (x.status !== 200) return null;
    const s = JSON.parse(JSON.parse(x.responseText).simresdata);
    const m = {};
    s[0].data.forEach((r) => (m[r.timestamps] = r.dailypnl));
    return (PX.cache[id] = m);
  };
  const series = (tag) => { const j = job(tag); return j && j.sid ? PX.pnl(j.sid) : null; };
  const mean = (x) => x.reduce((a, b) => a + b, 0) / x.length;
  const sd = (x) => { const m = mean(x); return Math.sqrt(mean(x.map((y) => (y - m) * (y - m)))); };
  const cor = (x, y) => { const mx = mean(x), my = mean(y); let s = 0; for (let i = 0; i < x.length; i++) s += (x[i] - mx) * (y[i] - my); return s / x.length / sd(x) / sd(y); };
  const common = (maps) => Object.keys(maps[0]).filter((t) => maps.every((m) => t in m)).map(Number).sort((a, b) => a - b);
  const vals = (m, ts) => ts.map((t) => (isFinite(m[t]) ? m[t] : 0));
  PX.submitted = () => window.R.jobs.filter((j) => j.state === 'submitted' && j.sid).map((j) => j.tag);
  // Correlation of two finished jobs (last 500 days) and each one's full-period daily IR.
  PX.pair = function (a, b) {
    const A = series(a), B = series(b); if (!A || !B) return 'missing PnL';
    const ts = common([A, B]), t5 = ts.slice(-500), x = vals(A, ts), y = vals(B, ts);
    return { corr500: +cor(vals(A, t5), vals(B, t5)).toFixed(3), irA: +(mean(x) / sd(x)).toFixed(3), irB: +(mean(y) / sd(y)).toFixed(3) };
  };
  // Correlation of a finished job with each of OUR submitted alphas (self-correlation check).
  PX.own = function (tag) {
    const out = {}; PX.submitted().forEach((s) => { if (s !== tag) out[s] = PX.pair(tag, s).corr500; }); return out;
  };
  // Predict a blend from finished parts: parts = [[tag, weight], ...]. Each part's PnL is scaled to equal
  // volatility, then weighted and summed. This only approximates the real blend (the portal re-scales
  // positions daily), so treat it as a pre-screen and confirm with a Slow run.
  PX.blend = function (parts) {
    const maps = parts.map(([t]) => series(t)); if (maps.some((m) => !m)) return 'missing PnL';
    const ts = common(maps), t5 = ts.slice(-500);
    const mk = (T) => { const cols = maps.map((m) => vals(m, T)); const sds = cols.map(sd);
      return T.map((_, i) => cols.reduce((acc, c, k) => acc + parts[k][1] * c[i] / sds[k], 0)); };
    const full = mk(ts), last = mk(t5), own = {};
    PX.submitted().forEach((s) => { const S = series(s); const tt = t5.filter((t) => t in S);
      const idx = new Map(t5.map((t, i) => [t, i])); own[s] = +cor(tt.map((t) => last[idx.get(t)]), vals(S, tt)).toFixed(3); });
    return { ir: +(mean(full) / sd(full)).toFixed(3), ownCorr: own };
  };
  // Triage: every finished, unsubmitted Slow job with IR >= minIR, with what blocks it and what a repair must achieve.
  // bar = 1.2 x the blocking pool alpha's IR/sqrt(TVR); needTVR = turnover at which today's IR would clear the bar.
  PX.triage = function (minIR) {
    minIR = minIR || 0.065;
    return window.R.jobs.filter((j) => j.s && j.state !== 'submitted' && j.s.ir >= minIR).map((j) => {
      const s = j.s, bar = s.corrIrTvr ? +(1.2 * s.corrIrTvr).toFixed(3) : null;
      const needTVR = bar ? +Math.pow(s.ir / bar, 2).toFixed(3) : null;
      let fix = s.ir < 0.072 ? 'RAISE IR to .072+' : (s.corr > 0.5 ? (needTVR && needTVR >= 0.05 ? 'CUT TVR ' + s.tvr + '->' + needTVR + ' or CORR ' + s.corr + '->.5' : 'CORR ' + s.corr + '->.5 (TVR route hopeless)') : 'check rw/best');
      if (s.st && s.st.rw != null && s.st.rw < 0.04) fix += ' | rw ' + s.st.rw + ' < .04';
      if (s.st && s.st.best != null && s.st.best > 0.5) fix += ' | best-year ' + s.st.best + ' > .5';
      return [j.tag, 'ir' + s.ir, 'tvr' + s.tvr, 'irtvr' + s.irtvr, 'corr' + s.corr + '@' + s.corrId, 'bar' + bar, fix].join(' ');
    });
  };
})();
'PX ready';
