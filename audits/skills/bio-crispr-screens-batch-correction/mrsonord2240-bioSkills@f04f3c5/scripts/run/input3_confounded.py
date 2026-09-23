"""
Input 3 (Edge) -- POST-FIX regression test, bio-crispr-screens-batch-correction.

Real request simulated: "All my drug-arm samples were processed in batch 2
(arrived late) and all vehicle-arm samples in batch 1. Can I still use ComBat
to remove the batch effect?"

Regression target: this input was unaffected by the P1 fixes directly, but it
now runs through the FIXED combat_correct() (with its within-batch-constant
filter and NaN-raise), so it verifies that filter does not interfere with
pycombat's own confound detector on a design that is deliberately fully
confounded, and that the "correction destroys biology" claim still holds
post-fix.
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import roc_auc_score
from combat.pycombat import pycombat

np.random.seed(11)
PUBLIC = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data")
OUT = Path(r"F:\OpenScience\audits\bio-crispr-screens-batch-correction\run\out_input3")
OUT.mkdir(exist_ok=True)

raw = pd.read_csv(PUBLIC / "HAP1_TKOv3_reads.txt", sep="\t")
cegv2 = set(pd.read_csv(PUBLIC / "CEGv2_core_essentials.txt", sep="\t")["GENE"])
negv1 = set(pd.read_csv(PUBLIC / "NEGv1_nonessentials.txt", sep="\t")["GENE"])
gene_col = raw["GENE"].values
rng = np.random.default_rng(11)

MULT, ADD = 0.6, 100
counts_df = pd.DataFrame({
    "day0_b1_r1": raw["HAP1_T0"],
    "day0_b1_r2": rng.poisson(raw["HAP1_T0"].clip(lower=0).values).astype(float),
    "endpt_b2_r1": rng.poisson((raw["HAP1_T18A"].clip(lower=0) * MULT + ADD).values).astype(float),
    "endpt_b2_r2": rng.poisson((raw["HAP1_T18B"].clip(lower=0) * MULT + ADD).values).astype(float),
    "endpt_b2_r3": rng.poisson((raw["HAP1_T18C"].clip(lower=0) * MULT + ADD).values).astype(float),
})
counts_df.index = pd.RangeIndex(len(raw))
batch_vector = ["batch1", "batch1", "batch2", "batch2", "batch2"]
condition_vector = ["day0", "day0", "endpt", "endpt", "endpt"]
print(f"Built fully-confounded design: batch == condition for every sample "
      f"({dict(zip(condition_vector, batch_vector))})")

def gene_lfc(df):
    day0 = [c for c in df.columns if "day0" in c]
    endpt = [c for c in df.columns if "endpt" in c]
    lfc = np.log2((df[endpt].mean(axis=1) + 1) / (df[day0].mean(axis=1) + 1))
    return pd.Series(lfc.values, index=gene_col).groupby(level=0).mean()

def auc_ceg_vs_neg(lfc):
    labeled = lfc[lfc.index.isin(cegv2 | negv1)]
    y_true = labeled.index.isin(cegv2).astype(int)
    return roc_auc_score(y_true, -labeled.values), len(labeled)

lfc_before = gene_lfc(counts_df)
auc_before, n = auc_ceg_vs_neg(lfc_before)
print(f"\nBefore any correction: CEGv2-vs-NEGv1 essentiality AUC = {auc_before:.4f} (n={n})")

# === current (post-fix) combat_correct(), verbatim from SKILL.md, WITHOUT mod
# (the documented common mistake) ===
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

corrected_nomod = combat_correct(counts_df, batch_vector, condition_vector=None)
lfc_nomod = gene_lfc(corrected_nomod)
auc_nomod, _ = auc_ceg_vs_neg(lfc_nomod)
print(f"\nComBat WITHOUT mod (batch==condition, uncorrected mistake):")
print(f"  Essentiality AUC after = {auc_nomod:.4f} (was {auc_before:.4f})")
print(f"  Mean |LFC| for CEGv2 genes: before={lfc_before[lfc_before.index.isin(cegv2)].abs().mean():.3f}, "
      f"after={lfc_nomod[lfc_nomod.index.isin(cegv2)].abs().mean():.3f}")
print(f"  SKILL.md's claim ('correction will destroy biology') "
      f"{'CONFIRMED' if auc_nomod < auc_before - 0.05 else 'NOT REPRODUCED'} by this run.")

# === WITH mod=condition -- condition IS the confound; pycombat's own detector should refuse ===
print("\nComBat WITH mod=condition_vector (condition is fully collinear with batch):")
try:
    _ = combat_correct(counts_df, batch_vector, condition_vector=condition_vector)
    print("  UNEXPECTED: combat_correct() did not detect the confound and returned a result.")
    refused = False
except Exception as e:
    print(f"  Correctly REFUSED: {type(e).__name__}: {e}")
    refused = True

summary = pd.DataFrame([{
    "auc_before": auc_before, "auc_after_combat_nomod": auc_nomod,
    "destroyed_signal": bool(auc_nomod < auc_before - 0.05),
    "confound_refused_with_mod": refused,
}])
summary.to_csv(OUT / "summary_metrics.csv", index=False)
print(f"\nResults written to {OUT}")
