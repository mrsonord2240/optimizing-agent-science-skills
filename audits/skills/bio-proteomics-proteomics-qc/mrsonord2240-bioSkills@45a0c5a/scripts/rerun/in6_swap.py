# Re-audit 2026-09-15, Input 6 (NEW, Variant). Suspected sample swap: SYNTHETIC proteinGroups.txt with the C2 and T3
# columns exchanged (all column families). Skill decision tree: "check if it correlates better with a DIFFERENT group".
# replicate_correlation only returns within-group pairs, so the cross-group comparison is agent code on its corr matrix.
import numpy as np, pandas as pd
from skill import S
D = '../data/'
pg = pd.read_csv(D + 'proteinGroups.txt', sep='\t', low_memory=False)
fam = ['Intensity', 'iBAQ', 'LFQ intensity', 'MS/MS count']
for f in fam:
    pg[f'{f} C2'], pg[f'{f} T3'] = pg[f'{f} T3'].copy(), pg[f'{f} C2'].copy()
info = pd.read_csv(D + 'sample_annotation.csv').set_index('sample'); grp = info['condition']; S8 = info.index.tolist()
clean = S['strip_contaminant_rows'](pg)
raw = clean[[f'Intensity {s}' for s in S8]]; raw.columns = S8
print('raw_sample_qc flags (swap is not a loading failure):', S['raw_sample_qc'](raw, grp).query('flag').index.tolist())
lfq = clean[[f'LFQ intensity {s}' for s in S8]].replace(0, np.nan); lfq.columns = S8
log2 = np.log2(lfq)
rc = S['replicate_correlation'](log2, grp)
print('within-group r:'); print(rc.round(3).to_string(index=False))
# follow the decision-tree row on the same correlation (restricted to the top-variance proteins so condition drives it)
filt = S['completeness_filter'](log2, grp, 0.7).dropna()
top = filt.loc[filt.var(axis=1).sort_values(ascending=False).index[:300]]
corr = top.sub(top.mean(axis=1), axis=0).corr()
for s in S8:
    own = corr.loc[s, [x for x in S8 if grp[x] == grp[s] and x != s]].mean()
    oth = corr.loc[s, [x for x in S8 if grp[x] != grp[s]]].mean()
    print(f'  {s} ({grp[s]}): mean centred r own {own:+.3f} other {oth:+.3f}' + ('  <-- better with other group' if oth > own else ''))
coords, _ = S['pca_batch_check'](filt, info)
print(coords[['PC1', 'PC2', 'condition', 'batch']].round(1).to_string())
