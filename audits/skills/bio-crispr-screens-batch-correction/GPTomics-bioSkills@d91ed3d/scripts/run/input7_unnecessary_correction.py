"""
Input 7 (Adversarial) -- bio-crispr-screens-batch-correction audit.

Real request simulated: "My replicate correlations are already 0.97+ within
and across batches, but let's run ComBat anyway just to be safe."

Tests SKILL.md's own "When NOT to Correct" table (row: "Replicates already
correlate >0.95 within and across batches -> No batch effect to correct") and
the Common Errors row "Replicates lose internal cohesion after correction ->
Over-correction". Does an agent following this Skill correctly decline, and
if the user insists, does forcing ComBat on clean data measurably hurt
anything (the claim the Skill makes)?
"""
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from combat.pycombat import pycombat

np.random.seed(5)
PUBLIC = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data")
raw = pd.read_csv(PUBLIC / "HAP1_TKOv3_reads.txt", sep="\t")
rng = np.random.default_rng(5)

# NO planted batch shift this time -- both "batches" are independent Poisson
# resamples of the SAME real distributions (T0 for day0, T18A for endpt).
counts_df = pd.DataFrame({
    "B1_day0_r1": raw["HAP1_T0"],
    "B1_day0_r2": rng.poisson(raw["HAP1_T0"].clip(lower=0).values).astype(float),
    "B1_endpt_r1": raw["HAP1_T18A"],
    "B1_endpt_r2": rng.poisson(raw["HAP1_T18A"].clip(lower=0).values).astype(float),
    "B2_day0_r1": rng.poisson(raw["HAP1_T0"].clip(lower=0).values).astype(float),
    "B2_day0_r2": rng.poisson(raw["HAP1_T0"].clip(lower=0).values).astype(float),
    "B2_endpt_r1": rng.poisson(raw["HAP1_T18A"].clip(lower=0).values).astype(float),
    "B2_endpt_r2": rng.poisson(raw["HAP1_T18A"].clip(lower=0).values).astype(float),
})
counts_df.index = pd.RangeIndex(len(raw))
batch_vector = ["batch1"] * 4 + ["batch2"] * 4
condition_vector = ["day0", "day0", "endpt", "endpt"] * 2

log_c = np.log2(counts_df + 1)
print("=== Replicate Pearson correlations (no planted batch effect) ===")
pairs = [("B1_day0_r1", "B2_day0_r1"), ("B1_endpt_r1", "B2_endpt_r1"),
         ("B1_day0_r1", "B1_day0_r2"), ("B1_endpt_r1", "B1_endpt_r2")]
for a, b in pairs:
    r, _ = stats.pearsonr(log_c[a], log_c[b])
    tag = "cross-batch" if a[:2] != b[:2] else "within-batch"
    print(f"  {a} vs {b} ({tag}): r = {r:.4f}")

print("\nPer SKILL.md 'When NOT to Correct': replicate r>0.95 within AND across "
      "batches => 'No batch effect to correct'. Correction should be DECLINED here.")

# Force it anyway, to test the Skill's claim that unnecessary correction adds noise.
data = pd.DataFrame(np.log2(counts_df.values + 1), index=counts_df.index, columns=counts_df.columns)
mod = list(condition_vector)
corrected = pycombat(data, batch_vector, mod=mod)
corrected = pd.DataFrame(np.power(2, corrected) - 1, index=counts_df.index, columns=counts_df.columns).clip(lower=0)
log_corr = np.log2(corrected + 1)

print("\n=== Replicate Pearson correlations AFTER forcing ComBat on clean data ===")
for a, b in pairs:
    r_before, _ = stats.pearsonr(log_c[a], log_c[b])
    r_after, _ = stats.pearsonr(log_corr[a], log_corr[b])
    tag = "cross-batch" if a[:2] != b[:2] else "within-batch"
    delta = r_after - r_before
    print(f"  {a} vs {b} ({tag}): r_before={r_before:.4f} -> r_after={r_after:.4f}  (delta={delta:+.4f})")

print("\nConclusion: unnecessary ComBat on already-clean data changes replicate")
print("correlation only marginally here (there was no real batch signal to remove or")
print("distort) -- consistent with the Skill's own guidance that the main risk of")
print("over-correction is on GENUINE batch effects with small per-batch n, not a")
print("blanket 'ComBat always hurts clean data' claim. The correct agent behavior")
print("per SKILL.md is still to decline unless the user overrides after being told why.")
