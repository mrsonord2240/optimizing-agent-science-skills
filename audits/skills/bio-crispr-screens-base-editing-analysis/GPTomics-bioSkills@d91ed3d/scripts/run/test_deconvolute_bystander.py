"""
Run the Skill's deconvolute_bystander() function verbatim (copied from SKILL.md)
against the REAL Alleles_frequency_table.zip from the synthetic CBE CRISPResso2
run. Ground truth partition (planted): 40% unmodified, 30% target-only,
20% target+bystander, 10% bystander-only.

Input 4 (Variant B): "From CRISPResso2 allele tables, separate reads by edit
pattern: target only, target+bystander_1, target+bystander_2. Compute per-pattern
fitness contribution."
"""
import pandas as pd

# ---- verbatim from SKILL.md ----
def deconvolute_bystander(allele_table_path, target_pos, bystander_pos_list):
    '''From CRISPResso2 allele table, partition reads by edit pattern at target + bystanders.
    Returns: per-pattern frequency for each combination of target/bystander edits.'''
    alleles = pd.read_csv(allele_table_path, sep='\t', compression='zip')
    alleles['target_edited'] = alleles['Aligned_Sequence'].str[target_pos-1] != alleles['Reference_Sequence'].str[target_pos-1]
    for bp in bystander_pos_list:
        alleles[f'bystander_{bp}_edited'] = alleles['Aligned_Sequence'].str[bp-1] != alleles['Reference_Sequence'].str[bp-1]
    return alleles.groupby(['target_edited'] + [f'bystander_{bp}_edited' for bp in bystander_pos_list])['Reference_pct'].sum().reset_index()
# ---- end verbatim ----

ALLELE_TABLE = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\base-editing-synthetic\results\CRISPResso_on_synth_cbe\Alleles_frequency_table.zip"

print("=== Real file columns ===")
df_real = pd.read_csv(ALLELE_TABLE, sep='\t', compression='zip')
print(list(df_real.columns))
print()

# 1-indexed amplicon positions matching this audit's ground truth (0-indexed 66 -> 1-indexed 67)
TARGET_POS_1INDEXED = 67
BYSTANDER_POS_1INDEXED = 69

print("=== Running the Skill's deconvolute_bystander() verbatim ===")
try:
    result = deconvolute_bystander(ALLELE_TABLE, target_pos=TARGET_POS_1INDEXED,
                                    bystander_pos_list=[BYSTANDER_POS_1INDEXED])
    print(result)
except Exception as e:
    print(f"CRASHED: {type(e).__name__}: {e}")

print()
print("=== Ground truth (from make_synthetic_be_fastq.py) ===")
print("unmodified=80 (40%), target_only=60 (30%), target_and_bystander=40 (20%), bystander_only=20 (10%)")
