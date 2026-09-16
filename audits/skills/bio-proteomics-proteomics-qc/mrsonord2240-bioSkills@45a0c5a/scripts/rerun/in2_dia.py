# Re-audit 2026-09-15, Input 2 (Variant A, regression). DIA-NN report.parquet: global-q filtering (decision tree),
# per-run raw signal on Precursor.Quantity (now named by the Skill), PG.MaxLFQ zeros as missing, matrix QC.
import numpy as np, pandas as pd
from skill import S
D = '../data/'
rep = pd.read_parquet(D + 'report.parquet')
rep['sample'] = rep['Run'].str.replace('_DIA', '', regex=False)
info = pd.read_csv(D + 'sample_annotation.csv').set_index('sample'); grp = info['condition']
run_only = rep[(rep['Q.Value'] <= 0.01) & (rep['PG.Q.Value'] <= 0.01)]
glob = rep[(rep['Q.Value'] <= 0.01) & (rep['PG.Q.Value'] <= 0.01) & (rep['Global.Q.Value'] <= 0.01) & (rep['Global.PG.Q.Value'] <= 0.01)]
lc = lambda d: d.loc[d['Protein.Group'].str.startswith('LOWCONF'), 'Protein.Group'].nunique()
print(f'protein groups run-level q only: {run_only["Protein.Group"].nunique()} (LOWCONF {lc(run_only)}) | + global q: {glob["Protein.Group"].nunique()} (LOWCONF {lc(glob)})')

# raw per-run signal: precursor x run matrix of Precursor.Quantity -> raw_sample_qc
pq = glob.pivot_table(index='Precursor.Id', columns='sample', values='Precursor.Quantity', aggfunc='first')[info.index]
print('\nraw_sample_qc on Precursor.Quantity:')
print(S['raw_sample_qc'](pq, grp).round(3).to_string())

mat = glob.drop_duplicates(['sample', 'Protein.Group']).pivot(index='Protein.Group', columns='sample', values='PG.MaxLFQ')[info.index]
print('\nPG.MaxLFQ exact zeros:', int((mat == 0).sum().sum()))
matn = mat.replace(0, np.nan)
print('median_cv_linear (zeros as NaN):', S['median_cv_linear'](matn, grp).round(2).to_dict('records'))
print('median_cv_linear (zeros left in):', S['median_cv_linear'](mat, grp).round(2).to_dict('records'))
log2 = np.log2(matn)
rc = S['replicate_correlation'](log2, grp); print('replicate r range', round(rc.r.min(), 3), round(rc.r.max(), 3))
filt = S['completeness_filter'](log2, grp, 0.7)
coords, evr = S['pca_batch_check'](filt, info)
print('explained', np.round(evr, 3))
