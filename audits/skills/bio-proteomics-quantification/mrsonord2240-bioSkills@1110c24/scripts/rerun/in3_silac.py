'''Quant Input 3 (regression): forward-label SILAC, 3 replicates, keep heavy-only proteins, median-normalize, limma. SYNTHETIC data.'''
import numpy as np, pandas as pd, warnings
QQ = 'F:/OpenScience/audits/bio-proteomics-quantification'
warnings.simplefilter('always')
ns = {}
with open(f'{QQ}/rerun/blocks/b06_SILAC_Quantification.py', encoding='utf-8') as fh:
    exec(fh.read(), ns)
t = pd.read_csv(f'{QQ}/data/silac_proteins.csv', index_col=0)
truth = pd.read_csv(f'{QQ}/data/silac_truth.csv', index_col=0)
ratios, pres = {}, {}
with warnings.catch_warnings(record=True) as w:
    for r in ['rep1', 'rep2', 'rep3']:
        ratios[r], pres[r] = ns['silac_log2_ratio'](t[f'Intensity H {r}'], t[f'Intensity L {r}'])   # column-wise (vectorized) call
    print('warnings:', [str(x.message) for x in w])
R = pd.DataFrame(ratios, index=t.index); P = pd.DataFrame(pres, index=t.index)
print('inf cells:', int(np.isinf(R.values).sum()), '| NaN cells:', int(R.isna().sum().sum()))
print('presence rep1:', P['rep1'].value_counts().to_dict())
R = R - R.median() # median normalize each replicate's log2 H/L
print('column means finite:', bool(np.isfinite(R.mean()).all()), '| SD finite for both-channel rows:', bool(np.isfinite(R.dropna().std(axis=1)).all()))
hon = P.index[(P == 'H-only').sum(axis=1) >= 2]
print('H-only in >=2 reps:', len(hon), truth.loc[hon, 'class'].value_counts().to_dict())
unc = truth.index[truth['class'] == 'unchanged']
print('median raw log2 H/L on unchanged proteins (label-efficiency bias):', round(float(pd.DataFrame(ratios, index=t.index).loc[unc].median().median()), 3))
R.dropna(how='all').to_csv(f'{QQ}/rerun/in3_silac_log2_norm.csv')
P.to_csv(f'{QQ}/rerun/in3_silac_presence.csv')
