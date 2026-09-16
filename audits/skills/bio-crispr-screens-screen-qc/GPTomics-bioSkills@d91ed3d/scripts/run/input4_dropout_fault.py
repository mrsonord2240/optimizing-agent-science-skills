"""Input 4 (Edge / planted fault). Prompt:
"We just got the endpoint sequencing back for replicate B. Run library
representation and Gini QC on all four samples before we move to hit calling."
Data: hap1_tkov3_dropout_fault.txt -- real HAP1 TKOv3 data with HAP1_T18B
artificially degraded (8% of guides zeroed + remaining counts crushed to ~5%
of original, simulating a failed library prep / heavy PCR dropout). The QC
must catch this planted fault.
"""
import sys
sys.path.insert(0, r"F:\OpenScience\audits\bio-crispr-screens-screen-qc\run")
import pandas as pd
from qc_functions import library_representation, stage_specific_thresholds, gini, depth_audit

DATA = r"F:\OpenScience\audits\bio-crispr-screens-screen-qc\data\hap1_tkov3_dropout_fault.txt"
df = pd.read_csv(DATA, sep="\t")
counts = df[["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]]

print("=== Library representation ===")
lib = library_representation(counts)
print(lib.round(3))

print("\n=== Gini per sample ===")
thr = stage_specific_thresholds()
for col in counts.columns:
    g = gini(counts[col].to_numpy())
    stage = "plasmid" if col == "HAP1_T0" else "endpoint"
    verdict = "PASS" if g < thr[stage]["gini_max"] else "FAIL"
    print(f"{col} (stage={stage}): Gini={g:.4f} threshold<{thr[stage]['gini_max']} -> {verdict}")

print("\n=== Depth ===")
print(depth_audit(counts).round(2))

caught = lib.loc["HAP1_T18B", "pct_zero"] > 5.0 or gini(counts["HAP1_T18B"].to_numpy()) > thr["endpoint"]["gini_max"]
print(f"\nPlanted dropout fault in HAP1_T18B caught by QC thresholds: {caught}")
