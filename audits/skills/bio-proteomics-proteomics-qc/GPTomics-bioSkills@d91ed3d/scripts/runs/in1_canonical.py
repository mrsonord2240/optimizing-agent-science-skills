"""Input 1 (Canonical): QC a MaxQuant LFQ run before limma. Mode A: code an agent writes following SKILL.md.
Data: SYNTHETIC proteinGroups.txt (8 runs, 2 batches). Audit 2026-09-11."""
import os, sys, traceback
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from skill_funcs import *  # verbatim SKILL.md functions

D = os.path.join(os.path.dirname(__file__), '..', 'data')
OUT = os.path.join(os.path.dirname(__file__), 'out_in1')
os.makedirs(OUT, exist_ok=True)
pg = pd.read_csv(os.path.join(D, 'proteinGroups.txt'), sep='\t', low_memory=False)
info = pd.read_csv(os.path.join(D, 'sample_annotation.csv'))
samples = info['sample'].tolist()
int_cols = [f'Intensity {s}' for s in samples]
lfq_cols = [f'LFQ intensity {s}' for s in samples]
print('rows', len(pg), '| flags:', {c: int((pg[c] == '+').sum()) for c in contaminant_flags})

# ---- Step A: contaminant fraction on RAW Intensity (SKILL.md l.103: PTXQC flags >1%)
con = pg['Potential contaminant'].fillna('') == '+'
frac = 100 * pg.loc[con, int_cols].sum() / pg[int_cols].sum()
print('\nContaminant % of summed raw Intensity per sample:\n', frac.round(2).to_string())
con_lfq = 100 * pg.loc[con, lfq_cols].sum() / pg[lfq_cols].sum()
print('Contaminant % of summed LFQ per sample:\n', con_lfq.round(2).to_string())

# ---- Step B: strip contaminant / decoy / site-only rows (verbatim function)
clean = strip_contaminant_rows(pg)
print('\nAfter strip_contaminant_rows:', len(clean), 'rows (removed', len(pg) - len(clean), ')')

# ---- Step C: raw_sample_qc AS WRITTEN on the raw Intensity columns (MaxQuant stores missing as 0)
raw = clean[int_cols].copy(); raw.columns = samples
print('\nraw_sample_qc AS WRITTEN (zeros left in):')
print(raw_sample_qc(raw).to_string())
# ---- adaptation: MaxQuant 0 = missing -> NaN (not stated anywhere in SKILL.md)
rawn = raw.replace(0, np.nan)
q = raw_sample_qc(rawn)
grp = info.set_index('sample')['condition']
q['group'] = grp
q['fold_vs_group_median_total'] = q['total_signal'] / q.groupby('group')['total_signal'].transform('median')
q['fold_vs_group_median_median'] = q['median_intensity'] / q.groupby('group')['median_intensity'].transform('median')
print('\nraw_sample_qc with 0->NaN:')
print(q.round(3).to_string())
print('Samples >=2x below group median (total or median):',
      q.index[(q['fold_vs_group_median_total'] <= 0.5) | (q['fold_vs_group_median_median'] <= 0.5)].tolist())

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
np.log2(rawn).boxplot(ax=ax[0]); ax[0].set_title('RAW log2 Intensity (pre-normalization)')
lfq = clean[lfq_cols].replace(0, np.nan); lfq.columns = samples
np.log2(lfq).boxplot(ax=ax[1]); ax[1].set_title('log2 LFQ intensity (MaxLFQ-normalized)')
fig.savefig(os.path.join(OUT, 'boxplots.png'), dpi=80)

# ---- Step D: normalized matrix = log2 LFQ (MaxLFQ already normalizes); replicate correlation
log2 = np.log2(lfq)
sample_groups = grp.loc[samples]
rc = replicate_correlation(log2, sample_groups)
print('\nWithin-group Pearson r (log2 LFQ):\n', rc.round(3).to_string())
corr = log2.corr()
for s in samples:
    own = corr.loc[s, [x for x in samples if grp[x] == grp[s] and x != s]].mean()
    other = corr.loc[s, [x for x in samples if grp[x] != grp[s]]].mean()
    print(f'  {s}: mean r own={own:.3f} other={other:.3f}{"  <-- swap?" if other > own else ""}')

# ---- Step E: CV linear vs geometric vs base-formula-on-log (the "~14x" claim)
cvl = median_cv_linear(lfq, sample_groups)
print('\nmedian_cv_linear (LFQ linear):\n', cvl.round(2).to_string())
for g in sample_groups.unique():
    m = sample_groups[sample_groups == g].index
    gcv = geometric_cv_from_log(log2[m]).median()
    base_on_log = (100 * log2[m].std(axis=1) / log2[m].mean(axis=1)).median()
    lin = cvl.set_index('group').loc[g, 'median_cv_pct']
    print(f'  {g}: geometric CV from log2 = {gcv:.2f}% | base formula on log2 = {base_on_log:.2f}% '
          f'| linear/log ratio = {lin / base_on_log:.1f}x | mean log2 = {log2[m].stack().mean():.1f}')

# ---- Step F: missingness profile + completeness filter
mean_ab, present = missingness_profile(log2)
bins = pd.qcut(mean_ab, 5)
print('\nPresent fraction by mean-abundance quintile (rising = MNAR):\n', present.groupby(bins, observed=True).mean().round(3).to_string())
print('Note: missingness_profile computes abundance_bins but never returns/uses it; mean_abundance is over OBSERVED values only.')
filt = completeness_filter(log2, sample_groups, 0.7)
print(f'completeness_filter(0.7): {len(log2)} -> {len(filt)} rows; all-NaN rows before filter: {int(log2.isna().all(axis=1).sum())}')

# ---- Step G: pca_batch_check AS WRITTEN: (1) sample_info straight from read_csv, (2) on unfiltered matrix
print('\n[G1] pca_batch_check(filt, info) with info as read_csv returns it (RangeIndex):')
try:
    pca_batch_check(filt, info)
except Exception as e:
    print('  ERROR:', type(e).__name__, str(e).splitlines()[0])
print('[G2] pca_batch_check on the UNFILTERED normalized matrix (all-NaN rows present):')
try:
    pca_batch_check(log2, info.set_index('sample'))
except Exception as e:
    print('  ERROR:', type(e).__name__, str(e).splitlines()[0])
print('[G3] pca_batch_check(filt, info.set_index("sample")):')
coords, evr = pca_batch_check(filt, info.set_index('sample'))
print('  explained variance:', np.round(evr, 3))
for pc in ['PC1', 'PC2']:
    from scipy.stats import f_oneway
    _, p = f_oneway(*[coords.loc[coords['condition'] == c, pc] for c in coords['condition'].unique()])
    print(f'  {pc} ~ condition: p={p:.4f}')
print(coords[['PC1', 'PC2', 'condition', 'batch']].round(2).to_string())
