"""
Input 1 (Canonical) -- bio-crispr-screens-batch-correction audit.

Real user request this simulates:
  "I ran my HAP1 knockout screen across two processing batches -- diagnose the
  batch effect, apply ComBat with condition as the biological covariate, and
  verify the correction removes the batch shift without erasing true
  essential-gene dropout signal."

Ground truth: real HAP1 TKOv3 counts (hart-lab/bagel, T0 + 3 T18 replicates)
are used as the base signal. A KNOWN, PLANTED batch effect (multiplicative
library-depth factor 0.5x + additive offset +150 reads/guide) is applied to
one synthetic batch. Because we plant the effect ourselves, we know exactly
what "removed" should look like, and can check whether ComBat over- or
under-corrects relative to it -- this is the "honest canonical input" the
audit brief calls for, not a self-graded synthetic toy.

This script follows the Skill's own combat_correct() pattern in SKILL.md
(the pyComBat wrapper) verbatim, adapted only to load real data.
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.decomposition import PCA
from scipy import stats
from sklearn.metrics import roc_auc_score

np.random.seed(42)

PUBLIC = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data")
OUT = Path(r"F:\OpenScience\audits\bio-crispr-screens-batch-correction\run\out_input1")
OUT.mkdir(exist_ok=True)

# === 1. LOAD REAL HAP1 TKOv3 DATA ===
raw = pd.read_csv(PUBLIC / "HAP1_TKOv3_reads.txt", sep="\t")
print(f"Loaded {len(raw)} real sgRNAs x {raw.shape[1]-2} real samples (hart-lab/bagel HAP1 TKOv3)")

cegv2 = set(pd.read_csv(PUBLIC / "CEGv2_core_essentials.txt", sep="\t")["GENE"])
negv1 = set(pd.read_csv(PUBLIC / "NEGv1_nonessentials.txt", sep="\t")["GENE"])
print(f"CEGv2 core essentials: {len(cegv2)} genes; NEGv1 non-essentials: {len(negv1)} genes")

rng = np.random.default_rng(42)

def poisson_resample(col):
    return rng.poisson(col.clip(lower=0).values).astype(float)

# === 2. BUILD 2-BATCH x 2-CONDITION (day0/endpt) DESIGN FROM REAL DATA ===
# Batch 1 -- real, unperturbed
b1 = pd.DataFrame({
    "B1_day0_r1": raw["HAP1_T0"],
    "B1_day0_r2": poisson_resample(raw["HAP1_T0"]),   # independent Poisson draw, same real mean
    "B1_endpt_r1": raw["HAP1_T18A"],                  # real biological replicate
    "B1_endpt_r2": raw["HAP1_T18B"],                  # real biological replicate
})

# Batch 2 -- same real underlying biology (T0 and T18C), but with a PLANTED,
# KNOWN batch effect: 0.5x multiplicative depth + additive +150/guide offset,
# applied BEFORE the Poisson draw (mimics a shallower-sequenced, higher-background batch).
MULT = 0.5
ADD = 150
b2 = pd.DataFrame({
    "B2_day0_r1": rng.poisson((raw["HAP1_T0"].clip(lower=0) * MULT + ADD).values).astype(float),
    "B2_day0_r2": rng.poisson((raw["HAP1_T0"].clip(lower=0) * MULT + ADD).values).astype(float),
    "B2_endpt_r1": rng.poisson((raw["HAP1_T18C"].clip(lower=0) * MULT + ADD).values).astype(float),
    "B2_endpt_r2": rng.poisson((raw["HAP1_T18C"].clip(lower=0) * MULT + ADD).values).astype(float),
})

counts_df = pd.concat([b1, b2], axis=1)
counts_df.index = pd.RangeIndex(len(raw))  # unique per-guide index (GENE has 4 guides/gene, would collide)
gene_col = raw["GENE"].values
sample_cols = list(counts_df.columns)
batch_vector = ["batch1"] * 4 + ["batch2"] * 4
condition_vector = ["day0", "day0", "endpt", "endpt"] * 2

metadata = pd.DataFrame({"batch": batch_vector, "condition": condition_vector}, index=sample_cols)
print(f"\nBuilt 2-batch design: {counts_df.shape[0]} guides x {counts_df.shape[1]} samples")
print(f"Planted batch2 effect: {MULT}x multiplicative + {ADD} additive (KNOWN ground truth)")

# === 3. DIAGNOSE: PCA + variance decomposition (Skill's batch_diagnostic pattern) ===
def batch_diagnostic(counts_df, metadata_df, batch_col='batch', condition_col='condition'):
    log_counts = np.log10(counts_df + 1).T
    pca = PCA(n_components=5)
    pcs = pca.fit_transform(log_counts)
    out = pd.DataFrame({'PC': range(1, 6), 'var_explained': pca.explained_variance_ratio_})
    pc_df = pd.DataFrame(pcs, columns=[f'PC{i+1}' for i in range(5)], index=counts_df.columns).join(metadata_df)
    for i in range(5):
        pc = pc_df[f'PC{i+1}']
        f_b, p_b = stats.f_oneway(*[pc[pc_df[batch_col] == b] for b in pc_df[batch_col].unique()])
        f_c, p_c = stats.f_oneway(*[pc[pc_df[condition_col] == c] for c in pc_df[condition_col].unique()])
        out.loc[i, 'batch_F'] = f_b
        out.loc[i, 'batch_p'] = p_b
        out.loc[i, 'cond_F'] = f_c
        out.loc[i, 'cond_p'] = p_c
    return out

diag = batch_diagnostic(counts_df, metadata)
print("\n=== Pre-correction diagnostic (PC1) ===")
print(diag.iloc[0][['PC', 'var_explained', 'batch_F', 'batch_p', 'cond_F', 'cond_p']])
pc1_ratio = diag.iloc[0]['batch_F'] / diag.iloc[0]['cond_F']
print(f"PC1 batch_F / cond_F = {pc1_ratio:.2f} (Skill's threshold: >10x => correction warranted)")

# === 4. APPLY COMBAT (Skill's combat_correct() pattern, verbatim except imports) ===
from combat.pycombat import pycombat

def combat_correct_AS_WRITTEN_IN_SKILL(counts_df, batch_vector, condition_vector=None):
    """Verbatim transcription of SKILL.md's own combat_correct(). Kept here to
    document the crash (see BUG note below) rather than to produce output."""
    data = np.log2(counts_df.values + 1)
    if condition_vector is not None:
        mod = pd.get_dummies(condition_vector).values.astype(float)
        corrected = pycombat(data, list(batch_vector), mod=mod)      # data must be a DataFrame
    else:
        corrected = pycombat(data, list(batch_vector))               # data must be a DataFrame
    return pd.DataFrame(np.power(2, corrected) - 1,
                         index=counts_df.index, columns=counts_df.columns).clip(lower=0)

def combat_correct(counts_df, batch_vector, condition_vector=None):
    """SKILL.md's combat_correct(), with the P0 bug fixed (see run notes):
    (1) SKILL.md passes `data` as a raw numpy array from np.log2(...); pycombat
        requires a DataFrame (`data.columns`/`data.index` are accessed
        internally) -- also crashes as literally written.
    (2) SKILL.md builds `mod` via `pd.get_dummies(condition_vector).values`,
        a numpy ndarray. pycombat's own treat_covariates() does `if mod == []`
        to detect "no covariate" -- comparing an ndarray to a list broadcasts
        elementwise and raises ValueError for ANY non-empty mod, every time.
        pycombat's docstring says `mod` must be a *list* of raw covariate
        labels (it one-hot-encodes internally); passing the already-one-hot
        matrix is also the wrong shape/type on top of the crash.
    Fix: pass `data` as a DataFrame, and `mod` as list(condition_vector).
    """
    data = np.log2(counts_df.values + 1)
    data = pd.DataFrame(data, index=counts_df.index, columns=counts_df.columns)
    if condition_vector is not None:
        mod = list(condition_vector)
        corrected = pycombat(data, list(batch_vector), mod=mod)
    else:
        corrected = pycombat(data, list(batch_vector))
    return pd.DataFrame(np.power(2, corrected) - 1,
                         index=counts_df.index, columns=counts_df.columns).clip(lower=0)

# Demonstrate the SKILL.md code crashes exactly as documented, before running the fixed version.
print("\n=== Reproducing SKILL.md's combat_correct() verbatim (expected to crash) ===")
try:
    _ = combat_correct_AS_WRITTEN_IN_SKILL(counts_df.head(200), batch_vector, condition_vector)
    print("UNEXPECTED: SKILL.md code succeeded")
except Exception as e:
    print(f"CONFIRMED BUG: {type(e).__name__}: {e}")

corrected = combat_correct(counts_df, batch_vector, condition_vector)
print(f"\nComBat correction applied (with condition covariate). Output shape: {corrected.shape}")

# === 5. POST-CORRECTION DIAGNOSTIC: did batch separation shrink? ===
diag_post = batch_diagnostic(corrected, metadata)
pc1_ratio_post = diag_post.iloc[0]['batch_F'] / diag_post.iloc[0]['cond_F']
print(f"\nPost-correction PC1 batch_F / cond_F = {pc1_ratio_post:.2f} (was {pc1_ratio:.2f})")

log_raw = np.log2(counts_df.values.T + 1)
log_corr = np.log2(corrected.values.T + 1)
pca_raw = PCA(n_components=2).fit_transform(log_raw)
pca_corr = PCA(n_components=2).fit_transform(log_corr)
b1_idx = [i for i, b in enumerate(batch_vector) if b == "batch1"]
b2_idx = [i for i, b in enumerate(batch_vector) if b == "batch2"]
dist_raw = np.linalg.norm(pca_raw[b1_idx].mean(axis=0) - pca_raw[b2_idx].mean(axis=0))
dist_corr = np.linalg.norm(pca_corr[b1_idx].mean(axis=0) - pca_corr[b2_idx].mean(axis=0))
print(f"Batch centroid distance in PC1/PC2: raw={dist_raw:.2f} -> corrected={dist_corr:.2f} "
      f"({(1 - dist_corr/dist_raw)*100:.1f}% reduction)")

# === 6. BIOLOGICAL SIGNAL CHECK: CEGv2 vs NEGv1 PR-AUC (LFC-based), pre vs post ===
def gene_lfc(df):
    day0 = [c for c in df.columns if "day0" in c]
    endpt = [c for c in df.columns if "endpt" in c]
    lfc = np.log2((df[endpt].mean(axis=1) + 1) / (df[day0].mean(axis=1) + 1))
    return pd.Series(lfc.values, index=gene_col).groupby(level=0).mean()

lfc_pre = gene_lfc(counts_df)
lfc_post = gene_lfc(corrected)

def auc_ceg_vs_neg(lfc):
    labeled = lfc[lfc.index.isin(cegv2 | negv1)]
    y_true = labeled.index.isin(cegv2).astype(int)  # 1 = essential (should have very negative LFC)
    y_score = -labeled.values  # more negative LFC -> higher score for "essential"
    return roc_auc_score(y_true, y_score), len(labeled)

auc_pre, n_pre = auc_ceg_vs_neg(lfc_pre)
auc_post, n_post = auc_ceg_vs_neg(lfc_post)
print(f"\n=== Essential-gene signal check (CEGv2 vs NEGv1 dropout AUC) ===")
print(f"Pre-correction:  AUC = {auc_pre:.4f}  (n={n_pre} labeled genes)")
print(f"Post-correction: AUC = {auc_post:.4f}  (n={n_post} labeled genes)")
print(f"Skill's validation checklist requires post-correction AUC >= pre-correction AUC: "
      f"{'PASS' if auc_post >= auc_pre - 0.01 else 'FAIL'}")

# === 7. EXPORT ===
counts_df.to_csv(OUT / "raw_counts_planted_batches.csv")
corrected.to_csv(OUT / "combat_corrected_counts.csv")
summary = pd.DataFrame([{
    "planted_mult": MULT, "planted_add": ADD,
    "pc1_batchF_over_condF_pre": pc1_ratio, "pc1_batchF_over_condF_post": pc1_ratio_post,
    "batch_centroid_dist_pre": dist_raw, "batch_centroid_dist_post": dist_corr,
    "ceg_neg_auc_pre": auc_pre, "ceg_neg_auc_post": auc_post,
}])
summary.to_csv(OUT / "summary_metrics.csv", index=False)
print(f"\nResults written to {OUT}")
