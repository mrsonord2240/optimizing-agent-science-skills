"""
Input 3 (Edge, regression): "Run CRISPResso2 on my pilot timepoint samples. Compute
target editing % per sgRNA. Keep sgRNAs >30% target editing for the primary screen."

Regression test for the P0 fix to filter_by_editing_efficiency() (KeyError 'Position').
Reuses the real CRISPResso2 2.3.4 output from this candidate's own tooling/fix pass
(F:\\OpenScience\\audit-envs\\crispr-screen-analyst\\tools\\dl\\base-editing-synthetic\\results\\),
a synthetic-CBE amplicon run with planted ground truth: target C editing = 50.00%,
bystander C editing = 30.00% (see data/ground_truth.txt in this audit folder, and the
source CRISPResso2_info.json / ground_truth.txt next to the real output).

target_position_0indexed = 66, bystander_position_0indexed = 68 in the amplicon
(from ground_truth.txt). The quantification window was run with
--quantification_window_size 10 --quantification_window_center -10, i.e. a
10nt window; need the 1-indexed position WITHIN that window, not the amplicon.
"""
import sys
sys.path.insert(0, ".")
from skill_functions import filter_by_editing_efficiency
import pandas as pd

RESULTS_DIR = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\base-editing-synthetic\results"
quant_file = RESULTS_DIR + r"\CRISPResso_on_synth_cbe\Quantification_window_nucleotide_percentage_table.txt"

raw = pd.read_csv(quant_file, sep='\t', index_col=0)
print("Raw table shape:", raw.shape)
print("Row index (nucleotide identities):", list(raw.index))
print("Number of window-position columns:", raw.shape[1])
print(raw.to_string())

# A researcher identifies target_pos from the amplicon/guide design, not by
# scanning -- but as an independent sanity check, the only window positions
# whose REFERENCE base is 'C' are the columns literally header-labeled 'C'
# (first occurrence) and 'C.1' (pandas' dedup suffix for the second occurrence
# of a repeated 'C' header); every other column's row-'C' value is structurally
# uninformative (reference isn't C there, so no C->T editing is possible).
c_ref_columns_1idx = [i + 1 for i, col in enumerate(raw.columns) if col in ('C', 'C.1')]
print("\nWindow positions (1-indexed) whose reference base is C:", c_ref_columns_1idx)
print("(By the synthetic design: spacer position 5 = target C, spacer position 7 = bystander C.)")

print("\n=== Running filter_by_editing_efficiency() at each real reference-C position ===")
results = {}
for pos in c_ref_columns_1idx:
    df = filter_by_editing_efficiency(RESULTS_DIR, target_pos=pos, target_base='C', efficiency_threshold=0.3)
    rec = df.to_dict('records')[0]
    results[pos] = rec
    print(f"target_pos={pos}: {rec}")

print("\nPlanted ground truth (data/ground_truth.txt / this audit's own real CRISPResso2 run):")
print("  window position 5 (target C)    -> 50.00% editing")
print("  window position 7 (bystander C) -> 30.00% editing")
assert abs(results[5]['editing_pct'] * 100 - 50.0) < 1e-6, "target position editing_pct mismatch"
assert abs(results[7]['editing_pct'] * 100 - 30.0) < 1e-6, "bystander position editing_pct mismatch"
print("\nPASS: filter_by_editing_efficiency() reproduces planted ground truth exactly "
      "at both the target (50%) and bystander (30%) positions on real CRISPResso2 2.3.4 output.")
