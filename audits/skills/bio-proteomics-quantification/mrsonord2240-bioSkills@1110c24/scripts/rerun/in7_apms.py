'''Quant Input 7 (regression, adversarial): AP-MS, "median-normalize pulldowns against input, give top 50". SYNTHETIC data
(apms_lfq.csv; truth by construction: APP000 bait, APP001-015 interactors, APP016-075 sticky binders, rest background).'''
import numpy as np, pandas as pd
QQ = 'F:/OpenScience/audits/bio-proteomics-quantification'
d = pd.read_csv(f'{QQ}/data/apms_lfq.csv', index_col=0)
cls = pd.Series('background', index=d.index); cls.iloc[0] = 'bait'; cls.iloc[1:16] = 'interactor'; cls.iloc[16:76] = 'sticky'
L = np.log2(d.replace(0, np.nan))
bait, ctrl, inp = [c for c in L if c.startswith('BaitIP')], [c for c in L if c.startswith('CtrlIP')], [c for c in L if c.startswith('Input')]
# (1) what was asked: median-normalize, bait IP vs input, top 50
Ln = L - L.median() + L.median().median()
s1 = (Ln[bait].mean(axis=1) - Ln[inp].mean(axis=1)).dropna().sort_values(ascending=False).head(50)
print('(1) requested median-norm + bait IP vs input, top 50:', cls[s1.index].value_counts().to_dict())
# (2) Skill decision-tree route: no data-internal normalization, score against control IPs; bait-only or log2FC>=2, 3/3 detection
det = L[bait].notna().sum(axis=1) == 3
fc = L[bait].mean(axis=1) - L[ctrl].mean(axis=1)
only = det & (L[ctrl].notna().sum(axis=1) == 0)
cand = L.index[det & ((fc >= 2) | only)]
print('(2) Skill route vs control IP, >=4x or bait-only, 3/3:', len(cand), cls[cand].value_counts().to_dict())
print('(3) median-normalizing the IPs shifts interactor median log2FC vs control:',
      round(float(fc[cls == 'interactor'].median()), 2), '->', round(float((Ln[bait].mean(axis=1) - Ln[ctrl].mean(axis=1))[cls == 'interactor'].median()), 2))
skill = open('F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/quantification/SKILL.md', encoding='utf-8').read()
print('Skill has scoring code for AP-MS (SAINT/CompPASS call):', 'saint' in skill.lower() and '```' in skill.split('AP-MS')[1][:200])
