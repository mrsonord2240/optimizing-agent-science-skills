"""Input 5 regression (IRS bridging) + the median-centering block + the shipped
example, all from the fork's current text."""
import subprocess
import sys

import numpy as np
import pandas as pd

QD = r"F:\OpenScience\audits\bio-proteomics-quantification\data"
QW = r"F:\OpenScience\audits\bio-proteomics-quantification\rerun4"
QK = r"F:\OpenScience\external\mrsonord2240__bioSkills\proteomics\quantification"

ns = {}
exec(compile(open(rf"{QW}\blocks\irs.py", encoding="utf-8").read(),
             "<SKILL.md: Bridge multiple TMT plexes with IRS>", "exec"), ns)

A = pd.read_csv(f"{QD}/tmt_plexA.csv", index_col=0)
B = pd.read_csv(f"{QD}/tmt_plexB.csv", index_col=0)
print("plex A", A.shape, "| plex B", B.shape, "| columns", list(A.columns))
refA, refB = A.columns[-1], B.columns[-1]
print("reference channel (last column):", refA, refB)

# reproduce the prior audit's perturbation: 3 zero + 3 NaN plex-B references
rng = np.random.default_rng(7)
victims = list(rng.choice(B.index, 6, replace=False))
B = B.copy()
B.loc[victims[:3], refB] = 0.0
B.loc[victims[3:], refB] = np.nan


def plex_offset(a, b):
    nonref_a = a.drop(columns=[refA])
    nonref_b = b.drop(columns=[refB])
    return float(np.nanmedian(np.log2(nonref_b.replace(0, np.nan)).median(axis=1)
                              - np.log2(nonref_a.replace(0, np.nan)).median(axis=1)))


print(f"raw       non-ref plex offset B-A {plex_offset(A, B):+.3f}")
sA, sB = ns["sample_loading_normalize"](A), ns["sample_loading_normalize"](B)
print(f"SL only   non-ref plex offset B-A {plex_offset(sA, sB):+.3f}")
bA, bB = ns["irs_scale"]([sA, sB], [refA, refB])
print(f"SL + IRS  non-ref plex offset B-A {plex_offset(bA, bB):+.3f}")
print(f"bridged plex B: +inf cells {int(np.isinf(bB.to_numpy()).sum())} | "
      f"all-NaN rows {int(bB.isna().all(axis=1).sum())}")

print("\n=== median-centering block, verbatim ===")
lfq = pd.read_csv(f"{QD}/proteinGroups.txt", sep="\t", low_memory=False)
icols = [c for c in lfq.columns if c.startswith("LFQ intensity")] or \
        [c for c in lfq.columns if c.startswith("Intensity ") and c != "Intensity"]
print("intensity columns:", len(icols))
ns2 = {"intensities": lfq[icols]}
import warnings  # noqa: E402
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    exec(compile(open(rf"{QW}\blocks\median_center.py", encoding="utf-8").read(),
                 "<SKILL.md: Median-center label-free intensities>", "exec"), ns2)
    print("warnings raised:", [str(x.message)[:60] for x in w])
norm = ns2["normalized"]
print("post-centering per-column medians:",
      [round(float(x), 3) for x in norm.median(axis=0)])
print("-inf cells:", int(np.isneginf(norm.to_numpy()).sum()))

print("\n=== shipped examples/lfq_normalization.py ===")
r = subprocess.run([sys.executable, "-B", rf"{QK}\examples\lfq_normalization.py"],
                   capture_output=True, text=True)
print((r.stdout or r.stderr)[:1200])
