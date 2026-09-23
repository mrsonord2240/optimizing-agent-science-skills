"""
Input 5 (Stress, regression): "Apply MAGeCK MLE to the BE screen counts. Aggregate
per-sgRNA LFC to per-variant fitness scores."

Regression test for the P0 fix to aggregate_variant_scores() (KeyError 'sgRNA' ->
real MAGeCK sgrna_summary.txt column is lowercase 'sgrna'). Reuses the real MAGeCK
0.5.9.5 output from the sibling bio-crispr-screens-mageck-analysis audit's own
verified real-data run (input1_canonical.sgrna_summary.txt, real HAP1 TKOv3 data).
"""
import sys
sys.path.insert(0, ".")
from skill_functions import aggregate_variant_scores
import pandas as pd

mageck_path = r"F:\OpenScience\audits\bio-crispr-screens-mageck-analysis\run\input1_canonical.sgrna_summary.txt"
mageck = pd.read_csv(mageck_path, sep='\t')
print("Real MAGeCK sgrna_summary.txt columns:", list(mageck.columns))
print(f"Rows: {len(mageck)}")
print(mageck.head(3).to_string())

# Build a synthetic variant-annotation table keyed on the first 6 real sgRNAs,
# assigning half to a "clean" (0 bystanders) variant and half to a
# bystander-confounded variant, exactly the shape the function expects.
sample_sgrnas = mageck['sgrna'].head(6).tolist()
variant_annotation_df = pd.DataFrame({
    'sgrna': sample_sgrnas,
    'target_variant': ['V1', 'V1', 'V1', 'V2', 'V2', 'V2'],
    'n_bystanders': [0, 0, 0, 1, 1, 2],
})
print("\nSynthetic variant_annotation_df:")
print(variant_annotation_df.to_string())

target_only_scores, mixed = aggregate_variant_scores(mageck, variant_annotation_df)
print("\ntarget_only_scores (per-variant mean/std/count of LFC, n_bystanders==0 only):")
print(target_only_scores.to_string())
print(f"\nmixed (n_bystanders>0) shape: {mixed.shape}")
print(mixed[['sgrna', 'target_variant', 'n_bystanders', 'LFC']].to_string())

# Independent hand check: V1's 3 sgRNAs all have n_bystanders=0, so
# target_only_scores.loc['V1','count'] must be 3, and its mean must equal the
# real MAGeCK LFC values for those 3 sgRNAs averaged by hand.
real_lfcs_v1 = mageck[mageck['sgrna'].isin(sample_sgrnas[:3])]['LFC'].astype(float).tolist()
hand_mean_v1 = sum(real_lfcs_v1) / len(real_lfcs_v1)
print(f"\nReal LFC values for V1's 3 sgRNAs: {real_lfcs_v1}")
print(f"Hand-computed mean: {hand_mean_v1}")
print(f"Function's reported mean for V1: {target_only_scores.loc['V1', 'mean']}")
assert target_only_scores.loc['V1', 'count'] == 3
assert abs(target_only_scores.loc['V1', 'mean'] - hand_mean_v1) < 1e-9
print("\nPASS: aggregate_variant_scores() merges cleanly on real MAGeCK output "
      "(lowercase 'sgrna') and its per-variant aggregation matches a by-hand mean.")
