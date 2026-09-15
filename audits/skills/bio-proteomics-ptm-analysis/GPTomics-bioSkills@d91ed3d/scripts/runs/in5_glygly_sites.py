"""Input 5 (Stress), part 1: diGly (K-GG) site table - SYNTHETIC data.
Skill expansion block (SKILL.md 108-131) with the filename changed to the GlyGly table (the Skill hard-codes
'Phospho (STY)Sites.txt'), then the checks the Skill's ubiquitin guidance implies, plus what an FLR can and
cannot be from MaxQuant tables alone.
"""
import os
import pandas as pd
import numpy as np
os.chdir('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/glygly')

# ---- SKILL.md block, filename swapped
phospho = pd.read_csv('GlyGly (K)Sites.txt', sep='\t', low_memory=False)
contaminant_col = 'Potential contaminant' if 'Potential contaminant' in phospho.columns else 'Contaminant'
phospho = phospho[(phospho['Reverse'] != '+') & (phospho[contaminant_col] != '+')]
CLASS_I_PROB = 0.75
phospho = phospho[phospho['Localization prob'] >= CLASS_I_PROB].copy()
gene = phospho['Gene names'].where(phospho['Gene names'].notna(), phospho['Protein'])
phospho['site_id'] = gene.str.split(';').str[0] + '_' + phospho['Amino acid'] + phospho['Position'].astype(int).astype(str)
mult_cols = [c for c in phospho.columns if '___' in c and c.split('___')[-1] in {'1', '2', '3'} and c.startswith('Intensity')]
long = phospho.melt(id_vars=['site_id', 'Amino acid', 'Position', 'Localization prob'], value_vars=mult_cols, var_name='run_multiplicity', value_name='intensity')
long['multiplicity'] = long['run_multiplicity'].str.split('___').str[-1]
long['run'] = long['run_multiplicity'].str.replace(r'___[123]$', '', regex=True).str.replace('Intensity ', '', regex=False)
long = long[long['intensity'] > 0]
long['log2_intensity'] = np.log2(long['intensity'])
print('class-I K-GG sites:', len(phospho), '| run labels:', sorted(long['run'].unique()))

# ---- localization / FLR: what the tables allow
lp = phospho['Localization prob']
print('Localization prob summary: min %.3f, median %.3f; sites with p < 1: %d' % (lp.min(), lp.median(), (lp < 1).sum()))
print('model-based expected FLR among accepted sites = mean(1 - p) = %.4f  (NOT an empirical FLR; '
      'LuciPHOr2/DeepFLR need the spectra, which a MaxQuant txt/ folder does not contain)' % (1 - lp).mean())

# ---- K-GG QC the Skill does not prompt: GG on the peptide C-terminal K (trypsin does not cleave after K-GG)
ev = pd.read_csv('evidence_glygly.txt', sep='\t', low_memory=False)
gg = ev[ev['Modifications'].str.contains('GlyGly', na=False)].copy()
gg['cterm_GG'] = gg['Modified sequence'].str.contains(r'K\(GlyGly \(K\)\)_$', regex=True)
bad = gg.loc[gg['cterm_GG'], 'Modified sequence'].unique()
print('K-GG peptides with GG on the C-terminal K:', len(bad), '->', list(bad)[:4])
truth = pd.read_csv('truth_sites.csv')
print('truth rows planted as C-terminal K-GG artifacts:', (truth['class'] == 'artifact_cterm_K').sum())
print('those artifact sites survive the Skill filters (REV/CON + class I):',
      int(truth.loc[truth['class'] == 'artifact_cterm_K', 'protein'].isin(phospho['Protein']).sum()))
