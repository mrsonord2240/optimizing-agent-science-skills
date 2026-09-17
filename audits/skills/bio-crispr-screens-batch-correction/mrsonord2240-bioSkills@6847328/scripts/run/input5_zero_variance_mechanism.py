"""
Input 5 (Stress) -- NEW input, not part of the pre-fix audit's 7 inputs.

Directly tests the fix log's headline, previously-unaudited claim: "features
that are constant within a single batch turn the entire ComBat output into
NaN -- measured as 6 zero-variance guides out of 2,000 producing an all-NaN
matrix." This script builds a controlled 2,000-guide dataset with EXACTLY 6
guides set to identical (zero-variance) counts within one batch, at the same
order of magnitude the fix log cites, and checks three things independently:

  1. Mechanism: does the OLD (pre-fix) combat_correct() -- no filter, no NaN
     check -- actually go all-NaN on this data, confirming the claimed cause?
  2. Fix: does the CURRENT (post-fix) combat_correct() drop exactly those 6
     guides, print the count, and return a fully non-NaN, non-corrupted matrix?
  3. No silent data loss: are the 6 dropped guides still present in the output
     (not silently discarded), with their exact raw counts, and are the OTHER
     1,994 guides still meaningfully batch-corrected (not just passed through)?
"""
import numpy as np
import pandas as pd
from pathlib import Path
from combat.pycombat import pycombat

rng = np.random.default_rng(2026)
OUT = Path(r"F:\OpenScience\audits\bio-crispr-screens-batch-correction\run\out_input5")
OUT.mkdir(exist_ok=True)

n_genes = 500
guides_per_gene = 4
n_guides = n_genes * guides_per_gene  # 2000, matching the fix log's own scale
n_per_batch = 4  # 4 samples per batch, >=3 per SKILL.md's own ComBat sample-size threshold

gene_names = [f"Gene_{i:03d}" for i in range(n_genes)]
genes = np.repeat(gene_names, guides_per_gene)
guide_ids = [f"{g}_g{i+1}" for g in gene_names for i in range(guides_per_gene)]

essential_genes = set(gene_names[:50])  # planted essential set with real dropout signal

batch1_base = 700.0
batch2_base = 700.0  # NOTE: made deliberately equal for PART 1's clean mechanism reproduction --
# an earlier version of this script used unequal (800 vs 650) baselines and found the SAME
# "dangerous" (deterministic, zero-residual-in-both-batches) construction did NOT reliably
# reproduce whole-matrix NaN (var_pooled came out as a tiny non-zero float, ~1e-30, from FP
# round-off in the linear-algebra solve, rather than an exact 0.0) -- it instead silently
# produced a degenerate-but-finite constant value for just the planted genes, without
# corrupting the rest. That is reported below as a second, independent finding (see the
# "numerically fragile" note near Part 1). This block isolates the clean, literature-matching
# reproduction; the batch-shifted variant is re-tested separately further down.
samples = [f"B1_ctrl_{i+1}" for i in range(n_per_batch)] + \
          [f"B1_treat_{i+1}" for i in range(n_per_batch)] + \
          [f"B2_ctrl_{i+1}" for i in range(n_per_batch)] + \
          [f"B2_treat_{i+1}" for i in range(n_per_batch)]
batch_vector = (["batch1"] * (2 * n_per_batch)) + (["batch2"] * (2 * n_per_batch))
condition_vector = (["ctrl"] * n_per_batch + ["treat"] * n_per_batch) * 2

counts = np.zeros((n_guides, len(samples)))
for j, s in enumerate(samples):
    base = batch1_base if "B1" in s else batch2_base
    lam = np.full(n_guides, base)
    is_ess = np.isin(genes, list(essential_genes))
    if "treat" in s:
        lam[is_ess] *= 0.25  # essential dropout under treatment
    counts[:, j] = rng.poisson(lam)

# === Plant two groups, to distinguish the actual NaN-triggering condition from a
# merely suspicious-looking one (found by probing pycombat's source: var_pooled is
# a PER-GENE variance pooled across ALL batches combined after regressing out the
# design matrix -- so a gene only drives the SHARED hyper-prior to NaN if it has
# ZERO residual in EVERY batch, i.e. it is perfectly, deterministically constant in
# BOTH batches, not merely constant in one noisy-elsewhere batch):
#
#   DANGEROUS (6 guides, matches the fix log's 6/2000 claim): deterministic,
#     noise-free constant value in EACH batch separately (0 in batch1, 500 in
#     batch2) -> zero pooled residual variance -> should corrupt the WHOLE matrix
#     via compute_prior()'s np.mean/np.var over ALL genes' gamma_hat/delta_hat.
#   SAFE-LOOKING (6 more guides): zero counts in batch1 only, ordinary Poisson
#     noise in batch2 -> nonzero pooled variance -> should NOT corrupt anything,
#     even though SKILL.md's own filter (std>0 per batch, independently) flags
#     and drops these too.
zero_var_target = 6
non_ess_idx = np.where(~np.isin(genes, list(essential_genes)))[0]
picked = rng.choice(non_ess_idx, size=2 * zero_var_target, replace=False)
planted_zero_idx = picked[:zero_var_target]          # DANGEROUS group
planted_safe_idx = picked[zero_var_target:]          # SAFE-LOOKING group
b1_cols = [i for i, b in enumerate(batch_vector) if b == "batch1"]
b2_cols = [i for i, b in enumerate(batch_vector) if b == "batch2"]
for gi in planted_zero_idx:
    counts[gi, b1_cols] = 0.0     # deterministic constant in batch1
    counts[gi, b2_cols] = 500.0   # ALSO deterministic constant in batch2 -- no noise anywhere
for gi in planted_safe_idx:
    counts[gi, b1_cols] = 0.0     # deterministic constant in batch1 only

counts_df = pd.DataFrame(counts, index=guide_ids, columns=samples)
print(f"Built {n_guides} guides x {len(samples)} samples, real batch shift "
      f"({batch1_base} vs {batch2_base} baseline), {len(essential_genes)} planted essential genes")
print(f"Planted {zero_var_target} DANGEROUS guides (deterministic constant in BOTH batches, "
      f"zero pooled residual variance) matching the fix log's claimed scale (6/2000)")
print(f"Planted {zero_var_target} more SAFE-LOOKING guides (constant in batch1 only, ordinary "
      f"Poisson noise in batch2) to test whether the fix's filter over-excludes safe features")

# === PART 1: does the OLD (pre-fix) combat_correct() -- verbatim, no filter/guard -- go all-NaN? ===
def combat_correct_OLD_PREFIX(counts_df, batch_vector, condition_vector=None):
    """Pre-fix SKILL.md pattern: log-transform, call pycombat directly, no
    within-batch-constant filter, no NaN check on the result."""
    data = pd.DataFrame(np.log2(counts_df.values + 1), index=counts_df.index, columns=counts_df.columns)
    if condition_vector is not None:
        corrected = pycombat(data, list(batch_vector), mod=list(condition_vector))
    else:
        corrected = pycombat(data, list(batch_vector))
    return pd.DataFrame(np.power(2, corrected.values) - 1,
                         index=corrected.index, columns=corrected.columns).clip(lower=0)

print("\n=== PART 1: reproducing the fix log's claimed mechanism with the OLD (unfiltered) pattern ===")
print("(isolated: DANGEROUS group only, i.e. deterministic zero-residual in BOTH batches -- see")
print(" comment above; this is the precise condition, found by reading pycombat's own source,")
print(" that zeroes var_pooled for a gene and corrupts the SHARED hyper-prior used by every gene)")
dangerous_only_idx = list(range(n_guides))
guides_to_drop_for_isolation = [i for i in range(n_guides) if i in set(planted_safe_idx)]
counts_dangerous_only = np.delete(counts, guides_to_drop_for_isolation, axis=0)
ids_dangerous_only = [g for i, g in enumerate(guide_ids) if i not in set(planted_safe_idx)]
counts_df_dangerous_only = pd.DataFrame(counts_dangerous_only, index=ids_dangerous_only, columns=samples)

old_corrected = combat_correct_OLD_PREFIX(counts_df_dangerous_only, batch_vector, condition_vector)
old_nan_count = old_corrected.isna().sum().sum()
old_total = old_corrected.size
print(f"OLD pattern ({len(ids_dangerous_only)} guides, {zero_var_target} of them DANGEROUS): "
      f"{old_nan_count}/{old_total} values NaN ({100*old_nan_count/old_total:.1f}%), "
      f"exit code 0, no exception raised")
mechanism_confirmed = (old_nan_count == old_total)
print(f"Mechanism confirmed ({zero_var_target} zero-pooled-variance guides corrupted the ENTIRE "
      f"matrix, not just their own rows): {mechanism_confirmed}")

# Contrast: the SAFE-LOOKING-only subset (constant in batch1, noisy in batch2) should NOT corrupt
# anything under the OLD unfiltered pattern -- confirming "constant within one batch" alone, the
# condition the fix's docstring cites, is not actually sufficient; zero POOLED variance is.
guides_to_drop_for_isolation2 = [i for i in range(n_guides) if i in set(planted_zero_idx)]
counts_safe_only = np.delete(counts, guides_to_drop_for_isolation2, axis=0)
ids_safe_only = [g for i, g in enumerate(guide_ids) if i not in set(planted_zero_idx)]
counts_df_safe_only = pd.DataFrame(counts_safe_only, index=ids_safe_only, columns=samples)
old_corrected_safe = combat_correct_OLD_PREFIX(counts_df_safe_only, batch_vector, condition_vector)
old_nan_safe = old_corrected_safe.isna().sum().sum()
print(f"\nContrast -- OLD pattern on the SAFE-LOOKING-only subset ({len(ids_safe_only)} guides, "
      f"{zero_var_target} constant-in-batch1-only but noisy-in-batch2): "
      f"{old_nan_safe}/{old_corrected_safe.size} NaN "
      f"({'as expected, NOT corrupted' if old_nan_safe == 0 else 'UNEXPECTEDLY corrupted'})")

# === PART 2: does the CURRENT (post-fix) combat_correct() fix it? ===
def combat_correct(counts_df, batch_vector, condition_vector=None, verbose=True):
    '''Verbatim from current SKILL.md.'''
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

print("\n=== PART 2: the CURRENT (post-fix) combat_correct() on the SAME data ===")
new_corrected = combat_correct(counts_df, batch_vector, condition_vector)
new_nan_count = new_corrected.isna().sum().sum()
print(f"NEW pattern: {new_nan_count}/{new_corrected.size} values NaN (must be 0)")
assert new_nan_count == 0, "post-fix combat_correct() must return zero NaNs here"
assert new_corrected.shape == counts_df.shape, "output must retain all 2000 guides (no rows dropped from the DataFrame)"

# === PART 3: no silent data loss -- both planted groups (12 total) are present with RAW counts ===
planted_ids = [guide_ids[i] for i in planted_zero_idx] + [guide_ids[i] for i in planted_safe_idx]
raw_vals = counts_df.loc[planted_ids]
out_vals = new_corrected.loc[planted_ids]
max_diff = (raw_vals - out_vals).abs().values.max()
print(f"\n=== PART 3: are the {len(planted_ids)} dropped guides silently discarded, or preserved as raw? ===")
print(f"Max abs diff between output and RAW counts for all planted guides (should be 0.0): {max_diff}")
assert max_diff == 0.0, "dropped guides must retain their exact raw counts, not be discarded or zeroed"

# And: are the OTHER (non-planted) guides actually corrected (not just passed through)?
other_ids = [g for g in guide_ids if g not in planted_ids]
same_as_raw = (new_corrected.loc[other_ids].round(6) == counts_df.loc[other_ids].round(6)).all(axis=1).sum()
print(f"Of the other {len(other_ids)} guides, {same_as_raw} are identical to raw (should be 0 -- "
      f"confirms they were genuinely ComBat-corrected, not accidentally also passed through raw)")
assert same_as_raw == 0

# === PART 4: over-exclusion check -- did the fix's per-batch filter drop the SAFE-LOOKING group
# even though Part 1's contrast run showed they never actually threaten pycombat with NaN? ===
print(f"\n=== PART 4: does the fix's filter drop MORE than the 6 guides that are actually dangerous? ===")
data_full = pd.DataFrame(np.log2(counts_df.values + 1), index=counts_df.index, columns=counts_df.columns)
batch_s_full = pd.Series(batch_vector, index=counts_df.columns)
usable_full = pd.Series(True, index=data_full.index)
for b in batch_s_full.unique():
    usable_full &= data_full.loc[:, batch_s_full.index[batch_s_full == b]].std(axis=1) > 0
dropped_by_filter = set(data_full.index[~usable_full])
dangerous_ids = set(guide_ids[i] for i in planted_zero_idx)
safe_ids = set(guide_ids[i] for i in planted_safe_idx)
print(f"Filter dropped {len(dropped_by_filter)} guides total: "
      f"{len(dropped_by_filter & dangerous_ids)}/{zero_var_target} DANGEROUS (correctly dropped, needed) + "
      f"{len(dropped_by_filter & safe_ids)}/{zero_var_target} SAFE-LOOKING (unnecessarily dropped, per Part 1's contrast run)")
over_excluded = len(dropped_by_filter & safe_ids)
if over_excluded > 0:
    print(f"FINDING: the fix's per-batch std>0 filter is broader than the actual NaN-triggering "
          f"condition (zero POOLED variance across all batches). It leaves {over_excluded} safe, "
          f"correctable guides permanently batch-confounded in the output (raw counts, un-corrected) "
          f"even though they never threatened the NaN corruption it exists to prevent. This matches "
          f"the 294-guide over-exclusion measured on real data in Input 1 (run/input1_canonical.py).")

# === Bonus: essential-gene dropout signal (on the un-planted guides) preserved post-correction ===
def gene_lfc(df):
    ctrl = [c for c in df.columns if "ctrl" in c]
    treat = [c for c in df.columns if "treat" in c]
    lfc = np.log2((df[treat].mean(axis=1) + 1) / (df[ctrl].mean(axis=1) + 1))
    gene_of = dict(zip(guide_ids, genes))
    return pd.Series(lfc.values, index=[gene_of[g] for g in df.index]).groupby(level=0).mean()

lfc_pre = gene_lfc(counts_df)
lfc_post = gene_lfc(new_corrected)
ess_lfc_pre = lfc_pre[lfc_pre.index.isin(essential_genes)].mean()
ess_lfc_post = lfc_post[lfc_post.index.isin(essential_genes)].mean()
noness_lfc_post = lfc_post[~lfc_post.index.isin(essential_genes)].mean()
print(f"\nEssential-gene mean LFC: pre-correction={ess_lfc_pre:.3f}, post-correction={ess_lfc_post:.3f} "
      f"(non-essential post-correction={noness_lfc_post:.3f}, should be near 0)")

summary = pd.DataFrame([{
    "n_guides": n_guides, "n_planted_zero_variance": zero_var_target,
    "old_pattern_nan_fraction": old_nan_count / old_total,
    "mechanism_confirmed": mechanism_confirmed,
    "new_pattern_nan_count": int(new_nan_count),
    "dropped_guides_max_diff_from_raw": float(max_diff),
    "essential_lfc_post": float(ess_lfc_post), "nonessential_lfc_post": float(noness_lfc_post),
}])
summary.to_csv(OUT / "summary_metrics.csv", index=False)

# === PART 5: is the "all-NaN" manifestation numerically reliable, or fragile? ===
# Re-run the SAME dangerous-guide construction, but with a realistic per-batch baseline
# shift among the surrounding genes (800 vs 650, as in a real screen with an actual batch
# effect) instead of Part 1-4's uniform 700/700. This changes the floating-point path
# through np.linalg.solve enough that var_pooled for the planted genes comes out as a tiny
# NONZERO float (~1e-30) rather than exact 0.0 -- division doesn't hit inf/nan, so the
# whole-matrix corruption this section otherwise reproduces (Part 1) does NOT occur here.
print("\n=== PART 5: is the all-NaN manifestation numerically reliable across data shapes? ===")
rng2 = np.random.default_rng(2026)
counts_shifted = np.zeros((n_guides, len(samples)))
b1b, b2b = 800.0, 650.0
for j, s in enumerate(samples):
    base = b1b if "B1" in s else b2b
    lam = np.full(n_guides, base)
    is_ess = np.isin(genes, list(essential_genes))
    if "treat" in s:
        lam[is_ess] *= 0.25
    counts_shifted[:, j] = rng2.poisson(lam)
picked2 = rng2.choice(non_ess_idx, size=zero_var_target, replace=False)
for gi in picked2:
    counts_shifted[gi, b1_cols] = 0.0
    counts_shifted[gi, b2_cols] = 500.0
counts_df_shifted = pd.DataFrame(counts_shifted, index=guide_ids, columns=samples)
old_shifted = combat_correct_OLD_PREFIX(counts_df_shifted, batch_vector, condition_vector)
nan_frac_shifted = old_shifted.isna().sum().sum() / old_shifted.size
dangerous_ids2 = [guide_ids[i] for i in picked2]
degenerate_vals = old_shifted.loc[dangerous_ids2].round(3).apply(lambda r: r.nunique(), axis=1)
other_ids2 = [g for g in guide_ids if g not in set(dangerous_ids2)]
other_unaffected = np.allclose(old_shifted.loc[other_ids2].values,
                                combat_correct_OLD_PREFIX(counts_df_shifted.loc[other_ids2],
                                                           batch_vector, condition_vector).values,
                                atol=1e-6)
print(f"With a real per-batch baseline shift (800 vs 650) among the surrounding genes:")
print(f"  Whole-matrix NaN fraction: {nan_frac_shifted:.4f} (Part 1's clean case: {old_nan_count/old_total:.4f})")
print(f"  The {zero_var_target} planted genes instead collapse to a single degenerate finite value "
      f"per gene (distinct values per row: {degenerate_vals.tolist()}, should be 1 each if degenerate)")
print(f"  Other (non-planted) genes numerically unaffected either way: {other_unaffected}")
if nan_frac_shifted == 0 and (degenerate_vals == 1).all():
    print("FINDING: the all-NaN failure this fix targets is real but numerically FRAGILE -- it depends "
          "on whether the linear-algebra solve's residual for a zero-residual gene rounds to exact 0.0 "
          "or a tiny nonzero float. In this realistic variant it manifests instead as a silently WRONG "
          "constant value for just the affected genes, not a matrix-wide NaN. Critically, that milder "
          "manifestation would NOT be caught by combat_correct()'s own `corrected.isna().any().any()` "
          "guard -- only the per-batch std>0 PRE-filter (which runs before pycombat is ever called) "
          "catches both manifestations. The NaN check alone, without the pre-filter, would be "
          "insufficient; the shipped fix's actual design (filter-then-check) is more robust than a "
          "reader would infer from the fix log's NaN-only framing.")

summary5 = pd.DataFrame([{
    "variant": "batch-shifted (800/650) bulk baseline",
    "nan_fraction": nan_frac_shifted,
    "degenerate_not_nan": bool(nan_frac_shifted == 0 and (degenerate_vals == 1).all()),
    "other_genes_unaffected": bool(other_unaffected),
}])
summary5.to_csv(OUT / "part5_fragility_check.csv", index=False)

print(f"\nAll assertions passed. Results written to {OUT}")
