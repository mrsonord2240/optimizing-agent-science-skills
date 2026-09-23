"""
Input 7 (Adversarial) -- POST-FIX regression test, bio-crispr-screens-batch-correction.

Real request simulated: "My replicate correlations are already 0.97+ within
and across batches, but let's run ComBat anyway just to be safe."

Regression target: pre-fix P1 #3 -- forcing ComBat on a batch-free design used
to silently return a 100%-NaN matrix with exit code 0. The current
combat_correct() (VERBATIM below) now checks `corrected.isna().any().any()`
and raises ValueError instead. This input verifies that actually happens.
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

# NO planted batch shift -- both "batches" are independent Poisson resamples
# of the SAME real distributions (T0 for day0, T18A for endpt).
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

# === current (post-fix) combat_correct(), VERBATIM from SKILL.md ===
def combat_correct(counts_df, batch_vector, condition_vector=None, verbose=True):
    data = pd.DataFrame(np.log2(counts_df.values + 1),
                        index=counts_df.index, columns=counts_df.columns)
    batch = pd.Series(list(batch_vector), index=counts_df.columns)
    usable = pd.Series(True, index=data.index)
    for b in batch.unique():
        usable &= data.loc[:, batch.index[batch == b]].std(axis=1) > 0
    if verbose and (~usable).any():
        print(f'ComBat: {(~usable).sum()} features are constant within a batch; '
              f'left uncorrected to keep them from NaN-ing the whole matrix')
    if condition_vector is not None:
        corrected = pycombat(data[usable], list(batch_vector), mod=list(condition_vector))
    else:
        corrected = pycombat(data[usable], list(batch_vector))
    if corrected.isna().any().any():
        raise ValueError('ComBat returned NaN values: pooled variance is near zero. Check that a '
                         'batch effect is actually present before correcting.')
    out = pd.DataFrame(np.power(2, corrected.values) - 1,
                       index=corrected.index, columns=corrected.columns).clip(lower=0)
    return out.reindex(counts_df.index).fillna(counts_df)

print("\n=== Forcing ComBat anyway (user override), via the CURRENT (post-fix) combat_correct() ===")
raised = False
try:
    corrected = combat_correct(counts_df, batch_vector, condition_vector)
    print("UNEXPECTED: combat_correct() returned a result without raising.")
    print(f"NaN count in result: {corrected.isna().sum().sum()}")
except ValueError as e:
    raised = True
    print(f"CONFIRMED FIX: combat_correct() raised ValueError instead of returning a silent all-NaN matrix:")
    print(f"  {e}")

# Also directly confirm the UNDERLYING pycombat behavior is still the same landmine
# (i.e. the fix is in the wrapper, not upstream) -- run pycombat raw, bypassing the wrapper.
print("\n=== Confirming the raw pycombat() call underneath still returns all-NaN silently (exit 0) ===")
data = pd.DataFrame(np.log2(counts_df.values + 1), index=counts_df.index, columns=counts_df.columns)
raw_corrected = pycombat(data, batch_vector, mod=list(condition_vector))
n_total = raw_corrected.size
n_nan = raw_corrected.isna().sum().sum()
print(f"Raw pycombat() output: {n_nan}/{n_total} NaN ({100*n_nan/n_total:.1f}%), no exception raised, exit code 0")

assert raised, "combat_correct() must raise ValueError on this batch-free input"
assert n_nan == n_total, "Sanity check: underlying pycombat should still be all-NaN without the wrapper's guard"
print("\nBoth assertions passed: wrapper now catches exactly the landmine that used to reach the user.")
