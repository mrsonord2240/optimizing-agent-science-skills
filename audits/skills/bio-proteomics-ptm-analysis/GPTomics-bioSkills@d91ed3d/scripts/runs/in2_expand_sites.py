"""Input 2 (Variant A): multiplicity expansion of a MaxQuant 'Phospho (STY)Sites.txt' (SYNTHETIC data).

Block 1 = SKILL.md lines 108-131 VERBATIM (only the working directory is set).
Block 2 = the site x run matrix + residue distribution the user asked for (agent code following the Skill).
Block 3 = SKILL.md motif block (lines 181-195) run next, in SKILL.md order.
"""
import os
import traceback
os.chdir('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho')

# ------------------------------------------------------------------ Block 1: SKILL.md verbatim
import pandas as pd
import numpy as np

# Filename has a SPACE in the modification name; accept either form.
phospho = pd.read_csv('Phospho (STY)Sites.txt', sep='\t', low_memory=False)

# Newer MaxQuant uses 'Potential contaminant'; older uses 'Contaminant'.
contaminant_col = 'Potential contaminant' if 'Potential contaminant' in phospho.columns else 'Contaminant'
phospho = phospho[(phospho['Reverse'] != '+') & (phospho[contaminant_col] != '+')]

CLASS_I_PROB = 0.75  # Olsen 2006 class-I convention; comparability standard, not a calibrated FLR
phospho = phospho[phospho['Localization prob'] >= CLASS_I_PROB].copy()

gene = phospho['Gene names'].where(phospho['Gene names'].notna(), phospho['Protein'])
phospho['site_id'] = gene.str.split(';').str[0] + '_' + phospho['Amino acid'] + phospho['Position'].astype(int).astype(str)

# Multiplicity columns carry THREE underscores: collapsing them mixes phospho-states.
mult_cols = [c for c in phospho.columns if '___' in c and c.split('___')[-1] in {'1', '2', '3'} and c.startswith('Intensity')]
long = phospho.melt(id_vars=['site_id', 'Amino acid', 'Position', 'Localization prob'], value_vars=mult_cols, var_name='run_multiplicity', value_name='intensity')
long['multiplicity'] = long['run_multiplicity'].str.split('___').str[-1]
long['run'] = long['run_multiplicity'].str.replace(r'___[123]$', '', regex=True).str.replace('Intensity ', '', regex=False)
long = long[long['intensity'] > 0]
long['log2_intensity'] = np.log2(long['intensity'])

# ------------------------------------------------------------------ checks on Block 1 output
raw = pd.read_csv('Phospho (STY)Sites.txt', sep='\t', low_memory=False)
print('rows in table:', len(raw), '| after REV/CON filter + class I:', len(phospho))
print('mult_cols picked up (%d):' % len(mult_cols), mult_cols[:5], '...')
print('distinct run labels after expansion:', sorted(long['run'].unique()))
bogus = long[long['run'] == 'Intensity']
print('rows carrying the bogus run "Intensity":', len(bogus), 'of', len(long))
s0 = bogus.iloc[0]
per_run = long[(long['site_id'] == s0['site_id']) & (long['multiplicity'] == s0['multiplicity']) & (long['run'] != 'Intensity')]
print(f"example {s0['site_id']} ___{s0['multiplicity']}: 'Intensity' run log2 = {s0['log2_intensity']:.2f}; "
      f"real runs log2 range = {per_run['log2_intensity'].min():.2f}-{per_run['log2_intensity'].max():.2f}; "
      f"sum of real runs = {np.log2(per_run['intensity'].sum()):.2f}")
blank_gene = phospho[phospho['Gene names'].isna()]
print('site_id for the row with blank Gene names:', blank_gene['site_id'].tolist())
print('duplicated site_id x multiplicity x run rows:', long.duplicated(['site_id', 'multiplicity', 'run']).sum())

# ------------------------------------------------------------------ Block 2: matrix the user asked for
mat = long.pivot_table(index=['site_id', 'multiplicity'], columns='run', values='log2_intensity')
print('\nsite x run matrix shape (Skill output as-is):', mat.shape, '| columns:', list(mat.columns))
med = mat.median()
print('column medians (log2):', med.round(2).to_dict())
# what a naive median-centring would do with the bogus column in place
print('bogus column median minus mean of real-run medians: %.2f log2' % (med['Intensity'] - med.drop('Intensity').mean()))
# corrected expansion: only per-experiment columns
mult_ok = [c for c in phospho.columns if c.startswith('Intensity ') and '___' in c and c.split('___')[-1] in {'1', '2', '3'}]
print('corrected: per-experiment multiplicity columns =', len(mult_ok))
print('\nresidue distribution, class I (Skill filter):')
print(phospho['Amino acid'].value_counts().to_string())
print('localization classes before filtering:')
cls = pd.cut(raw.loc[(raw['Reverse'] != '+') & (raw['Potential contaminant'] != '+'), 'Localization prob'],
             bins=[0, 0.25, 0.5, 0.75, 1.0001], labels=['IV', 'III', 'II', 'I'], include_lowest=True, right=False)
print(cls.value_counts().sort_index().to_string())

# multiplicity switch: collapsed vs expanded log2FC (T - C) for the 4 multiplicity-switch sites
truth = pd.read_csv('truth_sites.csv')
sw = truth.loc[truth['multiplicity_switch'], 'protein'].tolist()
print('\nmultiplicity-switch sites: collapsed "Intensity <run>" log2FC vs expanded ___1 / ___2 log2FC (T - C):')
for acc in sw:
    r = raw[raw['Protein'] == acc].iloc[0]
    def fc(suffix):
        c = np.log2([r[f'Intensity {s}{suffix}'] for s in ['C1', 'C2', 'C3', 'C4']])
        t = np.log2([r[f'Intensity {s}{suffix}'] for s in ['T1', 'T2', 'T3', 'T4']])
        return np.nanmean(t[np.isfinite(t)]) - np.nanmean(c[np.isfinite(c)])
    print(f"  {acc}_{r['Amino acid']}{r['Position']}: collapsed {fc(''):+.2f} | ___1 {fc('___1'):+.2f} | ___2 {fc('___2'):+.2f}")

# ------------------------------------------------------------------ Block 3: SKILL.md motif block, next in order
print('\n--- SKILL.md motif block (lines 181-195), run after Block 1 ---')
try:
    from collections import Counter

    # 'Sequence window' is a 31-mer (+/-15) centered on the modified residue.
    WINDOW_HALF = 7  # +/-7 flanking is the standard kinase-motif window
    foreground = [w[15 - WINDOW_HALF: 16 + WINDOW_HALF] for w in confident['Sequence window'].dropna() if len(w) >= 31]
except Exception:
    traceback.print_exc(limit=1)
long.to_csv('F:/OpenScience/audits/bio-proteomics-ptm-analysis/runs/in2_long_skill_output.csv', index=False)
