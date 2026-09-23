"""Fresh Phase-2 executions for Inputs 3, 5, 7, 10-13.

All imported functions are copied byte-for-byte from fb1efc10's Skill package.
The script asserts output properties; no source files are modified.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RUN = Path(r"F:\OpenScience\audits\bio-proteomics-quantification\run\phase2_20260923")
DATA = Path(r"F:\OpenScience\audits\bio-proteomics-quantification\data")
sys.path.insert(0, str(RUN / "skill_copy" / "scripts"))
from silac_checks import arg_to_pro_shift, silac_labeling_efficiency
from apms_score import score_vs_control_ips


def median_center(log_int: pd.DataFrame) -> pd.DataFrame:
    med = log_int.median(axis=0)
    return log_int - med + med.median()


def sample_loading_normalize(plex: pd.DataFrame) -> pd.DataFrame:
    target = plex.sum(axis=0).mean()
    return plex * (target / plex.sum(axis=0))


def irs_scale(plexes: list[pd.DataFrame], refs: list[str]) -> list[pd.DataFrame]:
    ref = pd.concat([p[c] for p, c in zip(plexes, refs)], axis=1).where(lambda x: x > 0)
    geo = np.exp(np.log(ref).mean(axis=1, skipna=False))
    return [p.mul(geo / ref.iloc[:, i], axis=0) for i, p in enumerate(plexes)]


def plex_offset(a: pd.DataFrame, b: pd.DataFrame, ra: str, rb: str) -> float:
    return float(np.nanmedian(np.log2(b.drop(columns=rb).replace(0, np.nan)).median(axis=1) - np.log2(a.drop(columns=ra).replace(0, np.nan)).median(axis=1)))


print("INPUT 3: SILAC ratios retain on/off proteins")
sp = pd.read_csv(DATA / "silac_proteins.csv")
h = sp[[c for c in sp if c.startswith("Intensity H")][0]].to_numpy(float)
l = sp[[c for c in sp if c.startswith("Intensity L")][0]].to_numpy(float)
both = (h > 0) & (l > 0)
ratio = np.where(both, np.log2(h / l), np.nan)
presence = np.select([both, h > 0, l > 0], ["both", "H-only", "L-only"], default="none")
counts = pd.Series(presence).value_counts().to_dict()
assert not np.isinf(ratio).any() and counts.get("H-only", 0) > 0 and counts.get("L-only", 0) > 0
print(json.dumps({"presence": counts, "infinite_ratios": int(np.isinf(ratio).sum())}, sort_keys=True))

print("INPUT 5: sample loading then IRS bridge")
a, b = (pd.read_csv(DATA / n, index_col=0) for n in ("tmt_plexA.csv", "tmt_plexB.csv"))
ra, rb = a.columns[-1], b.columns[-1]
b = b.copy(); victims = list(b.index[:6]); b.loc[victims[:3], rb] = 0; b.loc[victims[3:], rb] = np.nan
sa, sb = sample_loading_normalize(a), sample_loading_normalize(b)
ba, bb = irs_scale([sa, sb], [ra, rb])
sl, irs = plex_offset(sa, sb, ra, rb), plex_offset(ba, bb, ra, rb)
assert abs(irs) < 0.05 and not np.isinf(bb.to_numpy()).any() and int(bb.isna().all(axis=1).sum()) == 6
print(json.dumps({"sl_offset": round(sl, 4), "irs_offset": round(irs, 4), "unbridged": 6}))

print("INPUT 7: AP-MS reject bait-vs-input normalization and score controls")
ip = pd.read_csv(DATA / "apms_lfq.csv", index_col=0)
bait = [c for c in ip if c.lower().startswith("bait")]
ctrl = [c for c in ip if c.lower().startswith(("ctrl", "control", "gfp"))]
inp = [c for c in ip if c.lower().startswith(("input", "lysate"))]
classes = pd.Series("background", index=ip.index); classes.iloc[0] = "bait"; classes.iloc[1:16] = "interactor"; classes.iloc[16:76] = "sticky"
scored = score_vs_control_ips(ip, bait, ctrl)
called = scored.index[scored.interactor]
naive = np.log2(ip.replace(0, np.nan)); naive = naive - naive.median(axis=0)
top50 = (naive[bait].mean(axis=1) - naive[inp].mean(axis=1)).sort_values(ascending=False).head(50)
assert int((classes[called] == "interactor").sum()) == 15 and int((classes[called] == "sticky").sum()) == 0
assert int((classes[top50.index] == "sticky").sum()) >= 40
print(json.dumps({"called": int(scored.interactor.sum()), "true_interactors": int((classes[called] == "interactor").sum()), "sticky_called": int((classes[called] == "sticky").sum()), "naive_top50_sticky": int((classes[top50.index] == "sticky").sum())}))

print("INPUT 10: SILAC estimator range and formula")
rng = np.random.default_rng(20260923)
rows = []
for truth in (0.98, 0.93, 0.88):
    n = 1800
    sequence = ["APEPK" if i % 3 else "AAAK" for i in range(n)]
    total = 10 ** rng.uniform(4, 7, n)
    # Pro-containing peptides deliberately lose 10% heavy signal: correct estimator must exclude them.
    heavy = total * truth * np.where(np.array(["P" in x for x in sequence]), 0.9, 1.0)
    light = total - total * truth
    got = silac_labeling_efficiency(pd.DataFrame({"Sequence": sequence, "Intensity H": heavy, "Intensity L": light}))
    assert abs(got["incorporation"] - truth) < 0.0002 and got["pro_containing_excluded"] == 1200
    rows.append({"truth": truth, "estimate": got["incorporation"], "excluded": got["pro_containing_excluded"]})
seq = ["AAAK", "AAPK", "AAPPAK", "AAPPPK"] * 200
conv = 0.08
ratios = 2 ** (np.array([s.count("P") for s in seq]) * np.log2(1 - conv))
shift = arg_to_pro_shift(pd.DataFrame({"Sequence": seq, "Ratio H/L": ratios}))
assert abs(shift["conversion_per_proline"] - conv) < 0.001
print(json.dumps({"efficiency_sweep": rows, "conversion": shift["conversion_per_proline"]}))

print("INPUT 11: AP-MS failed controls and edge behaviour")
one_dead = ip.copy(); one_dead.loc[:, ctrl[0]] = 0
edge = score_vs_control_ips(one_dead, bait, ctrl)
assert int(edge.n_ctrl_runs_used.iloc[0]) == len(ctrl) - 1 and int(edge.interactor.sum()) == int(scored.interactor.sum())
all_dead = ip.copy(); all_dead.loc[:, ctrl] = 0
try:
    score_vs_control_ips(all_dead, bait, ctrl)
except ValueError as e:
    assert "every control IP is empty" in str(e)
else:
    raise AssertionError("all-empty controls did not fail")
print(json.dumps({"one_dead_controls_used": int(edge.n_ctrl_runs_used.iloc[0]), "all_dead": "ValueError"}))

print("INPUT 12 (fresh): sequence-free SILAC fallback and all-Pro guard")
fallback = silac_labeling_efficiency(pd.DataFrame({"Intensity H": [93., 93.], "Intensity L": [7., 7.]}))
assert fallback["sequence_column_used"] is False and fallback["incorporation"] == 0.93
try:
    silac_labeling_efficiency(pd.DataFrame({"Sequence": ["PPP"], "Intensity H": [93.], "Intensity L": [7.]}))
except ValueError as e:
    assert "no Pro-free peptide" in str(e)
else:
    raise AssertionError("all-Pro guard did not fail")
print(json.dumps({"fallback": fallback["incorporation"], "all_pro": "ValueError"}))

print("INPUT 13 (fresh): shipped example copy")
example = subprocess.run([sys.executable, "-B", str(RUN / "skill_copy" / "examples" / "lfq_normalization.py")], capture_output=True, text=True)
print(example.stdout.strip())
assert example.returncode == 0 and "SILAC pilot:" in example.stdout and "AP-MS: called" in example.stdout
print(json.dumps({"example_exit": example.returncode, "assertions": "pass"}))
