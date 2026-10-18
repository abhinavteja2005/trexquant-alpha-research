// Read-only export of Trexsim alpha results for the deck (Oct 18).
// Paste into the DevTools console of a logged-in Trexsim tab (www.trexsim.com/trexsim/pysim).
// It only GETs each alpha's result page, never starts or changes anything,
// then downloads trexsim_export.json (daily PnL + every other field the portal returns).
(async () => {
  const ids = [673000, 705948, 708808, 678911, 684336, 685104, 679831, 685741, 716550, 724045, 715966, 707365];
  const out = {};
  for (const id of ids) {
    try {
      const r = await fetch('/trexsim/pysim/alpha/' + id + '/?format=json', { credentials: 'include' });
      if (!r.ok) { out[id] = { error: r.status }; console.log(id, 'HTTP', r.status); continue; }
      const j = await r.json();
      if (typeof j.simresdata === 'string') j.simresdata = JSON.parse(j.simresdata);
      out[id] = j;
      console.log(id, 'ok');
    } catch (e) { out[id] = { error: String(e) }; console.log(id, 'failed', e); }
  }
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out)], { type: 'application/json' }));
  a.download = 'trexsim_export.json';
  a.click();
  console.log('done:', Object.keys(out).length, 'alphas');
})();
