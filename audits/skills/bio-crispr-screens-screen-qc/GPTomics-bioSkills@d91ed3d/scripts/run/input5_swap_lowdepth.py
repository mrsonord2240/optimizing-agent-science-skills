"""Input 5 (Stress / multi-part). Prompt:
"Run the full composite QC gate across all four samples -- library
representation, Gini, replicate concordance, depth, and PCA clustering by
stage -- and tell me which endpoint replicates are safe to carry into hit
calling."
Data: hap1_tkov3_swap_lowdepth_fault.txt -- real HAP1 TKOv3 data where
HAP1_T18B has been replaced with a jittered copy of the plasmid-stage
(HAP1_T0) sample mislabeled as an endpoint replicate (a realistic sample-sheet
mixup), and HAP1_T18C has been down-sampled 50x (a low-depth sequencing
lane). Both faults must be caught before hit calling.
"""
import sys
sys.path.insert(0, r"F:\OpenScience\audits\bio-crispr-screens-screen-qc\run")
import pandas as pd
import numpy as np
from qc_functions import (library_representation, stage_specific_thresholds, gini,
                           replicate_concordance, depth_audit, screen_pca)

DATA = r"F:\OpenScience\audits\bio-crispr-screens-screen-qc\data\hap1_tkov3_swap_lowdepth_fault.txt"
df = pd.read_csv(DATA, sep="\t")
counts = df[["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]]

print("=== Gini per sample ===")
thr = stage_specific_thresholds()
ginis = {}
for col in counts.columns:
    g = gini(counts[col].to_numpy())
    ginis[col] = g
    stage = "plasmid" if col == "HAP1_T0" else "endpoint"
    print(f"{col} (stage={stage}): Gini={g:.4f}")
print("-> HAP1_T18B Gini looks plasmid-like even though labeled endpoint:",
      abs(ginis["HAP1_T18B"] - ginis["HAP1_T0"]) < 0.02)

print("\n=== Replicate concordance (endpoint T18 A/B/C) ===")
cond_map = {"T18_endpoint": ["HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]}
rc = replicate_concordance(counts, cond_map)
print(rc.round(4))

print("\n=== Depth ===")
depth = depth_audit(counts)
print(depth.round(2))

print("\n=== PCA (samples labeled by intended stage) ===")
metadata = pd.DataFrame({
    "stage": ["plasmid", "endpoint", "endpoint", "endpoint"],
}, index=["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"])
pcs, evr = screen_pca(counts, metadata, condition_col="stage")
print(pcs.round(3))
print("explained_variance_ratio:", evr.round(3))

# Diagnostic: does HAP1_T18B (mislabeled plasmid) sit near HAP1_T0 in PC space,
# and correlate with T0 far more than with the true endpoint replicates?
log_counts = np.log10(counts + 1)
r_T18B_vs_T0 = log_counts[["HAP1_T18B", "HAP1_T0"]].corr().iloc[0, 1]
r_T18B_vs_T18A = log_counts[["HAP1_T18B", "HAP1_T18A"]].corr().iloc[0, 1]
print(f"\nHAP1_T18B vs HAP1_T0 (plasmid) pearson_log = {r_T18B_vs_T0:.4f}")
print(f"HAP1_T18B vs HAP1_T18A (true endpoint rep) pearson_log = {r_T18B_vs_T18A:.4f}")
swap_caught = r_T18B_vs_T0 > r_T18B_vs_T18A and (r_T18B_vs_T0 - r_T18B_vs_T18A) > 0.05
print(f"Swapped-plasmid-as-endpoint fault in HAP1_T18B caught (correlates more with plasmid than with true replicate): {swap_caught}")

low_depth_caught = depth.loc["HAP1_T18C", "depth_grade"] in ("FAIL", "CAUTION")
print(f"Low-depth fault in HAP1_T18C caught by depth_audit: {low_depth_caught} (grade={depth.loc['HAP1_T18C', 'depth_grade']})")
