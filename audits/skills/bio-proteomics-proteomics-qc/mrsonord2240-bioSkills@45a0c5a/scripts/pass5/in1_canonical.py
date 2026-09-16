# Re-audit 2026-09-15, Input 1 (Canonical, regression). MaxQuant LFQ QC before limma, SKILL.md functions verbatim.
import numpy as np, pandas as pd
from skill import S
D = '../data/'
pg = pd.read_csv(D + 'proteinGroups.txt', sep='\t', low_memory=False)
info = pd.read_csv(D + 'sample_annotation.csv')          # as a user loads it (RangeIndex)
samples = info['sample'].tolist()
grp = info.set_index('sample')['condition']
int_cols = [f'Intensity {s}' for s in samples]

print('contaminant % of raw Intensity (contaminant_fraction):')
print(S['contaminant_fraction'](pg, int_cols).round(2).to_string())
clean = S['strip_contaminant_rows'](pg)
print('strip_contaminant_rows:', len(pg), '->', len(clean))

raw = clean[int_cols].copy(); raw.columns = samples
print('\nraw_sample_qc(raw Intensity, groups):')
print(S['raw_sample_qc'](raw, grp).round(3).to_string())

lfq = clean[[f'LFQ intensity {s}' for s in samples]].replace(0, np.nan); lfq.columns = samples
log2 = np.log2(lfq)
rc = S['replicate_correlation'](log2, grp)
print('\nreplicate r (log2 LFQ): min', round(rc.r.min(), 3), 'max', round(rc.r.max(), 3))
print('median_cv_linear:', S['median_cv_linear'](lfq, grp).round(2).to_dict('records'))
g = S['geometric_cv_from_log'](log2[grp[grp == 'Control'].index]).median()
base_log = (100 * log2[grp[grp == 'Control'].index].std(axis=1) / log2[grp[grp == 'Control'].index].mean(axis=1)).median()
print(f'Control geometric CV {g:.2f}% | base formula on log2 {base_log:.2f}% | mean log2 {log2.stack().mean():.1f} | ln2*mean {np.log(2)*log2.stack().mean():.1f}')
print('missingness_profile (present fraction by abundance decile):', S['missingness_profile'](log2).round(2).tolist())
filt = S['completeness_filter'](log2, grp, 0.7)
print('completeness_filter:', len(log2), '->', len(filt))

print('\npca_batch_check(filt, info) with info as read_csv returns it:')
try:
    S['pca_batch_check'](filt, info)
except Exception as e:
    print('  ', type(e).__name__, e)
print('pca_batch_check(filt, info.set_index("sample")):')
coords, evr = S['pca_batch_check'](filt, info.set_index('sample'))
print('  explained', np.round(evr, 3))
from scipy.stats import f_oneway
for pc in ['PC1', 'PC2']:
    print(f'  {pc} ~ condition p={f_oneway(*[coords.loc[coords.condition == c, pc] for c in coords.condition.unique()])[1]:.4f}')
