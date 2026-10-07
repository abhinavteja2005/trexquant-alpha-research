"""Pre-screen blends in the browser before simulating them (cheap proxy, successive-halving rung 0).

A draft may carry "parts": [[tag, weight], ...] naming finished Slow alphas whose PnL it combines.
  python tools/prescreen.py request   -> adds PX.blend(...) calls for un-screened drafts to alphas/queue/ops.json "px"
  python tools/prescreen.py apply     -> reads the newest alphas/snapshots/*-px.txt, records predictions in
                                         alphas/prescreen.json, and moves drafts predicted IR < .055 or own-corr > .7 to
                                         the ops.json skip list (others go to the front).
PX.blend (runner/px.js) scales each part to equal volatility, so it approximates the real blend; it reads ~.04-.08
high on correlation and is a pre-screen, not a verdict.
"""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "alphas" / "prescreen.json"
OPS = ROOT / "alphas" / "queue" / "ops.json"


def drafts():
    out = {}
    for f in (ROOT / "alphas" / "drafts").glob("*.json"):
        for it in json.loads(f.read_text(encoding="utf-8")):
            if it.get("parts"):
                out[it["tag"]] = it
    return out


def call(it):
    return f"'{it['tag']}=>'+JSON.stringify(PX.blend({json.dumps(it['parts'])}))"


def main(mode):
    store = json.loads(STORE.read_text()) if STORE.exists() else {}
    ops = json.loads(OPS.read_text())
    d = drafts()
    if mode == "request":
        todo = [t for t in d if t not in store]
        ops["px"] = list(dict.fromkeys(ops.get("px", []) + [call(d[t]) for t in todo]))
        OPS.write_text(json.dumps(ops, indent=1), encoding="utf-8")
        print(f"{len(todo)} PX.blend requests added to ops.json")
        return
    files = sorted(glob.glob(str(ROOT / "alphas" / "snapshots" / "*-px.txt")))
    text = open(files[-1], encoding="utf-8").read() if files else ""
    for t in d:
        m = re.search(re.escape(t) + r"=>(\{.*?\})(?:\"|\s|$)", text)
        if not m:
            continue
        try:
            res = json.loads(m.group(1))
        except ValueError:
            continue
        own = max(res.get("ownCorr", {}).values() or [0])
        ok = res.get("ir", 0) >= .055  # own-corr only orders (similar alphas may be submitted); PX under-predicts it (.52 vs .84)
        store[t] = {"ir": res.get("ir"), "ownMax": own, "pass": ok}
        if ok and own <= .45:
            ops["front"] = [t] + [x for x in ops.get("front", []) if x != t]
        elif ok:
            ops["front"] = [x for x in ops.get("front", []) if x != t] + [t]
        else:
            ops["skip"] = sorted(set(ops.get("skip", [])) | {t})
        print(f"{t}: predicted IR {res.get('ir')} own-max {own} -> {'front' if ok else 'skip'}")
    ops["px"] = [p for p in ops.get("px", []) if not any(p.startswith(f"'{t}=>") for t in store)]
    STORE.write_text(json.dumps(store, indent=1), encoding="utf-8")
    OPS.write_text(json.dumps(ops, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "request")
