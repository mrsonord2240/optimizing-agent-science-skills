"""
Input 5b -- companion to input5_zero_variance_mechanism.py.

A minimal, clean reproduction of the fix log's claimed mechanism ("6 zero-within-batch
guides out of 2,000 produced an all-NaN matrix"), used to isolate exactly which condition
triggers pycombat's whole-matrix NaN corruption. TEST B is the condition that reliably
reproduces it: a gene must be deterministically constant (zero residual, no Poisson noise)
in EVERY batch separately, not merely constant within one noisy-elsewhere batch (TEST C).
See input5_zero_variance_mechanism.py Part 5 for why the SAME "constant in both batches"
construction does not always reproduce the NaN outcome in a differently-shaped dataset
(floating-point fragility in the underlying linear-algebra solve).
"""
import numpy as np, pandas as pd
from combat.pycombat import pycombat

def old_pattern(counts_df, batch_vector, condition_vector):
    data = pd.DataFrame(np.log2(counts_df.values + 1), index=counts_df.index, columns=counts_df.columns)
    corrected = pycombat(data, list(batch_vector), mod=list(condition_vector))
    return corrected

rng = np.random.default_rng(1)
n_genes = 500
total_guides = 2000
gene_names = [f"G{i}" for i in range(n_genes)]
genes = np.repeat(gene_names, 4)
guide_ids = [f"{g}_g{i}" for g in gene_names for i in range(4)]
n_per_batch = 4
samples = [f"B1_{i}" for i in range(n_per_batch)] + [f"B2_{i}" for i in range(n_per_batch)]
batch_vector = ["batch1"]*n_per_batch + ["batch2"]*n_per_batch
condition_vector = (["ctrl","treat"]*n_per_batch)[:n_per_batch]*2
counts = rng.poisson(700, size=(total_guides, len(samples))).astype(float)
counts_df = pd.DataFrame(counts, index=guide_ids, columns=samples)
b1cols = [i for i,b in enumerate(batch_vector) if b=="batch1"]
b2cols = [i for i,b in enumerate(batch_vector) if b=="batch2"]

# Test A: constant-in-batch1-only (0), batch2 noisy (previous probe, already known NaN=0%)
# Test B: constant in BOTH batches, deterministically, no noise at all (perfectly design-explained)
zidx = rng.choice(total_guides, size=6, replace=False)
counts_df2 = counts_df.copy()
for gi in zidx:
    counts_df2.iloc[gi, b1cols] = 0.0     # exact constant in batch1
    counts_df2.iloc[gi, b2cols] = 500.0   # exact constant in batch2 too (different level, no noise)
corrected = old_pattern(counts_df2, batch_vector, condition_vector)
nan_frac = corrected.isna().sum().sum() / corrected.size
print(f"TEST B (constant in BOTH batches, no noise): NaN fraction = {nan_frac:.4f}  ({corrected.isna().sum().sum()}/{corrected.size})")
# which rows are NaN?
nan_rows = corrected.index[corrected.isna().any(axis=1)]
print(f"  NaN rows: {len(nan_rows)} -- matches planted guides? {set(nan_rows) == set(counts_df2.index[zidx])}")

# Test C: constant in batch1 only (0), batch2 ALSO has near-zero variance but not exactly (tiny jitter)
counts_df3 = counts_df.copy()
for gi in zidx:
    counts_df3.iloc[gi, b1cols] = 0.0
    counts_df3.iloc[gi, b2cols] = 500.0 + rng.integers(-1,2,size=len(b2cols))  # tiny noise
corrected3 = old_pattern(counts_df3, batch_vector, condition_vector)
nan_frac3 = corrected3.isna().sum().sum() / corrected3.size
print(f"TEST C (batch1 constant 0, batch2 tiny jitter): NaN fraction = {nan_frac3:.4f}")
