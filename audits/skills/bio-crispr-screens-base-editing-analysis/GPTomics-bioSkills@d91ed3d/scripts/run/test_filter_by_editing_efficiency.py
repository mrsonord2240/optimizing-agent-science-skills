"""
Run the Skill's filter_by_editing_efficiency() function verbatim (copied from
SKILL.md) against REAL CRISPResso2 output from the synthetic CBE FASTQ (ground
truth: 50% target editing at the target C, 30% at the bystander C).

Input 2 (Variant A): "Run CRISPResso2 on my pilot timepoint samples. Compute
target editing % per sgRNA. Keep sgRNAs >30% target editing for the primary
screen." -- this is exactly the code path exercised here.
"""
import pandas as pd
from pathlib import Path

# ---- verbatim from SKILL.md ----
def filter_by_editing_efficiency(crispresso_outputs_dir, target_pos, target_base, efficiency_threshold=0.5):
    '''Drop sgRNAs that edit <efficiency_threshold of reads at target position.
    crispresso_outputs_dir: directory containing CRISPResso per-sample outputs.'''
    results = []
    for sample_dir in Path(crispresso_outputs_dir).glob('CRISPResso_on_*'):
        sgrna_id = sample_dir.name.replace('CRISPResso_on_', '')
        quant_file = sample_dir / 'Quantification_window_nucleotide_percentage_table.txt'
        if not quant_file.exists():
            continue
        df = pd.read_csv(quant_file, sep='\t')
        # Find target position in the quantification window
        target_row = df[df['Position'] == target_pos]
        if target_row.empty:
            continue
        # Editing = sum of non-original bases at target position
        original_pct = target_row[target_base].values[0]
        editing_pct = (100 - original_pct) / 100
        results.append({'sgrna_id': sgrna_id, 'editing_pct': editing_pct,
                         'pass_filter': editing_pct >= efficiency_threshold})
    return pd.DataFrame(results)
# ---- end verbatim ----

CRISPRESSO_DIR = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\base-editing-synthetic\results"

print("=== Real file structure (what the function actually receives) ===")
quant_file = Path(CRISPRESSO_DIR) / "CRISPResso_on_synth_cbe" / "Quantification_window_nucleotide_percentage_table.txt"
df_real = pd.read_csv(quant_file, sep='\t')
print("Columns:", list(df_real.columns))
print("Index / first column values (row labels):")
print(pd.read_csv(quant_file, sep='\t', index_col=0).index.tolist())
print()

print("=== Running the Skill's filter_by_editing_efficiency() verbatim ===")
try:
    result = filter_by_editing_efficiency(CRISPRESSO_DIR, target_pos=5, target_base='C',
                                           efficiency_threshold=0.3)
    print("Result:")
    print(result)
except Exception as e:
    print(f"CRASHED: {type(e).__name__}: {e}")
