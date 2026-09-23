"""
Input 1 (Canonical) -- POST-FIX regression test, bio-crispr-screens-batch-correction.
Source: mrsonord2240/bioSkills@684732876d2781df75d90ba35c3e9949ff4f28b2:crispr-screens/batch-correction

Real user request this simulates:
  "I ran my HAP1 knockout screen across two processing batches -- diagnose the
  batch effect, apply ComBat with condition as the biological covariate, and
  verify the correction removes the batch shift without erasing true
  essential-gene dropout signal."

Regression target: pre-fix P1 #1 -- combat_correct() crashed because `data`
was passed as a raw ndarray and `mod` as a one-hot ndarray. The fixed version
in SKILL.md now passes a DataFrame and mod=list(condition_vector), adds a
within-batch-constant-feature filter, and raises ValueError if the result is
still all-NaN.

combat_correct() below is a VERBATIM transcription of the current SKILL.md
"ComBat Empirical-Bayes Correction" code block (copied from
run/skill-copy/SKILL.md, not hand-fixed by the auditor).
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.decomposition import PCA
from scipy import stats
from sklearn.metrics import roc_auc_score
from combat.pycombat import pycombat

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
b1 = pd.DataFrame({
    "B1_day0_r1": raw["HAP1_T0"],
    "B1_day0_r2": poisson_resample(raw["HAP1_T0"]),
    "B1_endpt_r1": raw["HAP1_T18A"],
    "B1_endpt_r2": raw["HAP1_T18B"],
})

MULT = 0.5
ADD = 150
b2 = pd.DataFrame({
    "B2_day0_r1": rng.poisson((raw["HAP1_T0"].clip(lower=0) * MULT + ADD).values).astype(float),
    "B2_day0_r2": rng.poisson((raw["HAP1_T0"].clip(lower=0) * MULT + ADD).values).astype(float),
    "B2_endpt_r1": rng.poisson((raw["HAP1_T18C"].clip(lower=0) * MULT + ADD).values).astype(float),
    "B2_endpt_r2": rng.poisson((raw["HAP1_T18C"].clip(lower=0) * MULT + ADD).values).astype(float),
})

counts_df = pd.concat([b1, b2], axis=1)
counts_df.index = pd.RangeIndex(len(raw))
gene_col = raw["GENE"].values
sample_cols = list(counts_df.columns)
batch_vector = ["batch1"] * 4 + ["batch2"] * 4
condition_vector = ["day0", "day0", "endpt", "endpt"] * 2

metadata = pd.DataFrame({"batch": batch_vector, "condition": condition_vector}, index=sample_cols)
print(f"\nBuilt 2-batch design: {counts_df.shape[0]} guides x {counts_df.shape[1]} samples")
print(f"Planted batch2 effect: {MULT}x multiplicative + {ADD} additive (KNOWN ground truth)")

# Report how many REAL guides are naturally constant within one batch here (not planted --
# this is what actually happens on real screen data at this scale).
log_check = pd.DataFrame(np.log2(counts_df.values + 1), index=counts_df.index, columns=counts_df.columns)
batch_s = pd.Series(batch_vector, index=sample_cols)
natural_constant = pd.Series(True, index=log_check.index)
for b in batch_s.unique():
    natural_constant &= log_check.loc[:, batch_s.index[batch_s == b]].std(axis=1) == 0
print(f"Naturally-occurring within-batch-constant guides in this real design: {natural_constant.sum()} / {len(counts_df)}")

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

# === 4. combat_correct() -- VERBATIM from current SKILL.md ===
def combat_correct(counts_df, batch_vector, condition_vector=None, verbose=True):
    '''ComBat on log-counts with optional biological covariate (condition).
    Preserves condition signal while removing batch shifts.

    pycombat takes the matrix as a DataFrame (rows = features, columns = samples) and both
    `batch` and `mod` as plain lists of labels -- it one-hot-encodes `mod` itself, so passing a
    pre-encoded array fails inside pycombat.

    Features that are constant within any one batch (e.g. a guide with zero counts across that
    batch) make ComBat's standardization divide by zero, and the NaNs propagate to EVERY value
    it returns -- with no exception and exit code 0. Measured on real TKOv3 counts: 6 such
    guides out of 2,000 produced an all-NaN matrix. They are dropped from the fit here and
    returned uncorrected.
    '''
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
    return out.reindex(counts_df.index).fillna(counts_df)   # dropped features keep raw counts

print("\n=== Running current (post-fix) SKILL.md combat_correct() verbatim ===")
corrected = combat_correct(counts_df, batch_vector, condition_vector)
print(f"ComBat correction applied (with condition covariate). Output shape: {corrected.shape}")
assert corrected.shape == counts_df.shape, "Output shape must match input shape (no rows lost)"
n_nan = corrected.isna().sum().sum()
print(f"NaN count in final output: {n_nan}")
assert n_nan == 0, "Final output must contain zero NaNs"

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
    y_true = labeled.index.isin(cegv2).astype(int)
    y_score = -labeled.values
    return roc_auc_score(y_true, y_score), len(labeled)

auc_pre, n_pre = auc_ceg_vs_neg(lfc_pre)
auc_post, n_post = auc_ceg_vs_neg(lfc_post)
print(f"\n=== Essential-gene signal check (CEGv2 vs NEGv1 dropout AUC) ===")
print(f"Pre-correction:  AUC = {auc_pre:.4f}  (n={n_pre} labeled genes)")
print(f"Post-correction: AUC = {auc_post:.4f}  (n={n_post} labeled genes)")
print(f"Skill's validation checklist requires post-correction AUC >= pre-correction AUC: "
      f"{'PASS' if auc_post >= auc_pre - 0.01 else 'FAIL'}")

# === 7. EXPORT ===
corrected.to_csv(OUT / "combat_corrected_counts.csv")
summary = pd.DataFrame([{
    "planted_mult": MULT, "planted_add": ADD,
    "natural_constant_guides": int(natural_constant.sum()),
    "final_nan_count": int(n_nan),
    "pc1_batchF_over_condF_pre": pc1_ratio, "pc1_batchF_over_condF_post": pc1_ratio_post,
    "batch_centroid_dist_pre": dist_raw, "batch_centroid_dist_post": dist_corr,
    "ceg_neg_auc_pre": auc_pre, "ceg_neg_auc_post": auc_post,
}])
summary.to_csv(OUT / "summary_metrics.csv", index=False)
print(f"\nResults written to {OUT}")
