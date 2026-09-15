"""Input 2 (Variant A): DIA-NN 1.9 report.parquet QC -- per-run IDs at 1% global FDR, raw per-run signal before
normalisation, then matrix QC on PG.MaxLFQ. Mode A (SKILL.md gives no DIA code; Decision Tree row 7 + Thresholds
table row 'DIA precursor + protein q both <= 0.01, GLOBAL q'). Data: SYNTHETIC report.parquet. Audit 2026-09-11."""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from skill_funcs import *

D = os.path.join(os.path.dirname(__file__), '..', 'data')
rep = pd.read_parquet(os.path.join(D, 'report.parquet'))
print('rows', len(rep), 'runs', rep['Run'].nunique(), 'protein groups', rep['Protein.Group'].nunique())
rep['sample'] = rep['Run'].str.replace('_DIA', '', regex=False)
info = pd.read_csv(os.path.join(D, 'sample_annotation.csv')).set_index('sample')

# --- 1. Run-level-only filter vs the SKILL's global filter
run_only = rep[(rep['Q.Value'] <= 0.01) & (rep['PG.Q.Value'] <= 0.01)]
glob = rep[(rep['Q.Value'] <= 0.01) & (rep['Global.Q.Value'] <= 0.01) & (rep['PG.Q.Value'] <= 0.01) & (rep['Global.PG.Q.Value'] <= 0.01)]
print(f'\nProtein groups, run-level q only : {run_only["Protein.Group"].nunique()}  (LOWCONF: {run_only["Protein.Group"].str.startswith("LOWCONF").sum() and run_only.loc[run_only["Protein.Group"].str.startswith("LOWCONF"), "Protein.Group"].nunique()})')
print(f'Protein groups, + global q <= 0.01: {glob["Protein.Group"].nunique()}  (LOWCONF: {glob["Protein.Group"].str.startswith("LOWCONF").sum()})')

# --- 2. Per-run QC BEFORE normalisation: IDs + raw summed Precursor.Quantity (not Precursor.Normalised / PG.MaxLFQ)
per_run = glob.groupby('sample').agg(precursors=('Precursor.Id', 'nunique'), protein_groups=('Protein.Group', 'nunique'),
                                    raw_precursor_signal=('Precursor.Quantity', 'sum'), norm_precursor_signal=('Precursor.Normalised', 'sum'))
per_run['raw_fold_vs_median'] = per_run['raw_precursor_signal'] / per_run['raw_precursor_signal'].median()
per_run['pg_fold_vs_median'] = per_run['protein_groups'] / per_run['protein_groups'].median()
print('\nPer-run QC (global 1% FDR):\n', per_run.round(3).to_string())

# --- 3. Protein matrix from PG.MaxLFQ (one value per run x group), then SKILL.md matrix QC functions
mat = glob.drop_duplicates(['sample', 'Protein.Group']).pivot(index='Protein.Group', columns='sample', values='PG.MaxLFQ')
mat = mat[info.index]
n_zero = int((mat == 0).sum().sum())
print(f'\nPG.MaxLFQ matrix {mat.shape}; exact zeros: {n_zero}; NaN: {int(mat.isna().sum().sum())}')
grp = info['condition']
print('\n[as written] replicate_correlation(np.log2(mat)) with the zeros still in:')
rc_raw = replicate_correlation(np.log2(mat), grp)
print(rc_raw.round(3).to_string())
print('[as written] median_cv_linear(mat) with zeros still in:')
print(median_cv_linear(mat, grp).round(2).to_string())
matn = mat.replace(0, np.nan)
log2 = np.log2(matn)
print('\n[adapted: 0 -> NaN] replicate_correlation:')
print(replicate_correlation(log2, grp).round(3).to_string())
print('[adapted] median_cv_linear:\n', median_cv_linear(matn, grp).round(2).to_string())
filt = completeness_filter(log2, grp, 0.7)
print(f'completeness_filter(0.7): {len(log2)} -> {len(filt)}')
coords, evr = pca_batch_check(filt, info)
print('explained variance', np.round(evr, 3))
print(coords[['PC1', 'PC2', 'condition', 'batch']].round(2).to_string())
