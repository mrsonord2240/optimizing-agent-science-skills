"""
Input 4 (Variant B, regression): "From CRISPResso2 allele tables, separate reads by
edit pattern: target only, target+bystander_1. Compute per-pattern fitness contribution."

Regression test for the P0 fix to deconvolute_bystander() (KeyError 'Reference_pct'
-> real column is '%Reads'). Reuses the same real CRISPResso2 2.3.4 allele table as
Input 3, with the same planted ground truth: 40% unmodified / 30% target-only /
20% target+bystander / 10% bystander-only (data/ground_truth.txt).
"""
import sys
sys.path.insert(0, ".")
from skill_functions import deconvolute_bystander
import pandas as pd

RESULTS_DIR = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\base-editing-synthetic\results"
allele_zip = RESULTS_DIR + r"\CRISPResso_on_synth_cbe\Alleles_frequency_table.zip"

raw = pd.read_csv(allele_zip, sep='\t', compression='zip')
print("Real Alleles_frequency_table.zip columns:", list(raw.columns))
print(f"Rows: {len(raw)}")

# target C at amplicon 0-indexed 66 -> 1-indexed position 67; bystander at 0-indexed
# 68 -> 1-indexed position 69 (from ground_truth.txt in this audit's data/).
target_pos = 67
bystander_pos = 69

result = deconvolute_bystander(allele_zip, target_pos=target_pos, bystander_pos_list=[bystander_pos])
print("\ndeconvolute_bystander() output:")
print(result.to_string())

total = result['%Reads'].sum()
print(f"\nSum of %Reads across all partitions: {total}")

def get_pct(target_edited, bystander_edited):
    row = result[(result['target_edited'] == target_edited) &
                  (result[f'bystander_{bystander_pos}_edited'] == bystander_edited)]
    return float(row['%Reads'].iloc[0]) if len(row) else 0.0

unmodified = get_pct(False, False)
target_only = get_pct(True, False)
target_and_bystander = get_pct(True, True)
bystander_only = get_pct(False, True)

print(f"\nunmodified={unmodified}  target_only={target_only}  "
      f"target+bystander={target_and_bystander}  bystander_only={bystander_only}")
print("Planted ground truth: unmodified=40.0  target_only=30.0  target+bystander=20.0  bystander_only=10.0")

assert abs(unmodified - 40.0) < 1e-6
assert abs(target_only - 30.0) < 1e-6
assert abs(target_and_bystander - 20.0) < 1e-6
assert abs(bystander_only - 10.0) < 1e-6
print("\nPASS: deconvolute_bystander() reproduces the planted ground truth exactly "
      "(40/30/20/10) on real CRISPResso2 2.3.4 output.")
