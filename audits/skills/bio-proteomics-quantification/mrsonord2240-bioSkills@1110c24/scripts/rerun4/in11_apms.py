"""Input 7 regression + NEW Input 11: does the pass-4 AP-MS scorer separate real
interactors from bead background, and how does it behave at its edges?

score_vs_control_ips is extracted VERBATIM from the fork's SKILL.md.
"""
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4")
from extract import blocks  # noqa: E402

QK = r"F:\OpenScience\external\mrsonord2240__bioSkills\proteomics\quantification\SKILL.md"
DATA = r"F:\OpenScience\audits\bio-proteomics-quantification\data"
SRC = [b for h, l, b in blocks(QK, "python") if h.startswith("AP-MS / Affinity")][0]
NS = {}
exec(compile(SRC, "<SKILL.md: AP-MS / Affinity-Enrichment Scoring>", "exec"), NS)
score = NS["score_vs_control_ips"]

ip = pd.read_csv(f"{DATA}/apms_lfq.csv", index_col=0)
print("columns:", list(ip.columns))
# Ground truth is POSITIONAL in this synthetic fixture (see the first audit's
# runs/in7_apms.py, which generated it): row 0 is the bait, rows 1-15 are the
# 15 true interactors, rows 16-75 are the 60 sticky bead/antibody binders, the
# rest is background.
cls = pd.Series("background", index=ip.index)
cls.iloc[0] = "bait"
cls.iloc[1:16] = "interactor"
cls.iloc[16:76] = "sticky"
print("truth classes:", cls.value_counts().to_dict())
num = ip
bait = [c for c in num.columns if c.lower().startswith("bait")]
ctrl = [c for c in num.columns if c.lower().startswith(("ctrl", "control", "gfp"))]
inp = [c for c in num.columns if c.lower().startswith(("input", "lysate"))]
print("bait:", bait, "| control:", ctrl, "| input:", inp)

print("\n=== Input 7 regression: the Skill's route ===")
out = score(num, bait, ctrl)
called = out[out["interactor"]]
print(f"called {len(called)} | classes {dict(cls[called.index].value_counts()) if cls is not None else 'n/a'}")
if cls is not None:
    true_int = set(cls[cls == "interactor"].index)
    sticky = set(cls[cls == "sticky"].index)
    print(f"true interactors recovered: {len(true_int & set(called.index))}/{len(true_int)}"
          f" | sticky binders called: {len(sticky & set(called.index))}/{len(sticky)}")
    print("median log2 enrichment by class:",
          {k: round(v, 2) for k, v in out["log2_enrichment"].groupby(cls).median().items()})
print("Inf cells in log2_enrichment:", int(np.isinf(out["log2_enrichment"]).sum()),
      "| NaN:", int(out["log2_enrichment"].isna().sum()),
      "| all NaN rows have n_bait == 0:",
      bool((out.loc[out["log2_enrichment"].isna(), "n_bait"] == 0).all()))

print("\n=== the route the Skill warns against: median-normalize, rank vs input ===")
if inp:
    L = np.log2(num.replace(0, np.nan))
    L = L - L.median(axis=0)
    naive = (L[bait].mean(axis=1) - L[inp].mean(axis=1)).sort_values(ascending=False)
    top50 = naive.head(50)
    print("top 50 by bait-vs-input:",
          dict(cls[top50.index].value_counts()) if cls is not None else "n/a")

print("\n=== NEW Input 11: edges of the scorer ===")
print("(a) a true interactor missing in ONE bait replicate, default min_bait_reps")
probe = num.copy()
if cls is not None and len(true_int) > 0:
    victim = sorted(true_int)[0]
    probe.loc[victim, bait[0]] = 0
    o = score(probe, bait, ctrl)
    print(f"    {victim}: n_bait {o.loc[victim, 'n_bait']} "
          f"enrich {o.loc[victim, 'log2_enrichment']:.2f} called {o.loc[victim, 'interactor']}"
          "   <- dropped by the strict default")
    o2 = score(probe, bait, ctrl, min_bait_reps=2)
    print(f"    same prey with min_bait_reps=2: called {o2.loc[victim, 'interactor']}"
          "   <- the escape hatch works")

print("(b) prey seen ONLY in the bait (no control signal at all)")
probe2 = num.copy()
probe2.loc[:, ctrl] = probe2.loc[:, ctrl].astype(float)
newrow = pd.Series(0.0, index=probe2.columns)
for c in bait:
    newrow[c] = 5e6
probe2.loc["BAIT_ONLY_PREY"] = newrow
o = score(probe2, bait, ctrl)
r = o.loc["BAIT_ONLY_PREY"]
print(f"    n_bait {r['n_bait']} n_ctrl {r['n_ctrl']} enrich {r['log2_enrichment']:.2f} "
      f"finite {np.isfinite(r['log2_enrichment'])} called {r['interactor']}")

print("(c) prey seen ONLY in the controls")
probe3 = num.copy()
newrow = pd.Series(0.0, index=probe3.columns)
for c in ctrl:
    newrow[c] = 5e6
probe3.loc["CTRL_ONLY_PREY"] = newrow
o = score(probe3, bait, ctrl)
r = o.loc["CTRL_ONLY_PREY"]
print(f"    n_bait {r['n_bait']} n_ctrl {r['n_ctrl']} enrich {r['log2_enrichment']} "
      f"called {r['interactor']}")

print("(d) an ENTIRELY EMPTY control run (a failed control IP)")
probe4 = num.copy()
probe4.loc[:, ctrl[0]] = 0.0
o = score(probe4, bait, ctrl)
n_called = int(o["interactor"].sum())
print(f"    called {n_called} (baseline {int(out['interactor'].sum())}) | "
      f"NaN enrichment {int(o['log2_enrichment'].isna().sum())} | "
      f"Inf {int(np.isinf(o['log2_enrichment']).sum())}")
if cls is not None:
    cc = cls[o[o['interactor']].index].value_counts().to_dict()
    print(f"    classes called: {cc}")

print("(e) ONE control replicate only (the minimum a lab might run)")
o = score(num, bait, ctrl[:1])
if cls is not None:
    print(f"    called {int(o['interactor'].sum())} classes "
          f"{dict(cls[o[o['interactor']].index].value_counts())}")

print("(f) spectral COUNTS instead of intensities (the Skill says either is fine)")
counts = (num[bait + ctrl] / num[bait + ctrl].replace(0, np.nan).min().min()).round()
o = score(counts, bait, ctrl)
if cls is not None:
    print(f"    called {int(o['interactor'].sum())} classes "
          f"{dict(cls[o[o['interactor']].index].value_counts())}")
