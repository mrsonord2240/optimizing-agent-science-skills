'''Input 4 (regression): 12 v 12 plasma DIA matrix, Python only. SYNTHETIC data. Skill block executed verbatim via exec of the extracted file.'''
import warnings
import numpy as np
import pandas as pd
RR = 'F:/OpenScience/audits/bio-proteomics-differential-abundance'
warnings.simplefilter('always')
ns = {}
exec(open(f'{RR}/rerun/blocks/b05_Python_Workflow.py', encoding='utf-8').read(), ns)

raw = pd.read_csv(f'{RR}/data/plasma_12v12.csv', index_col=0)
truth = pd.read_csv(f'{RR}/data/plasma_truth.csv', index_col=0)
ctrl_cols = [c for c in raw.columns if c.startswith('ctrl')]
case_cols = [c for c in raw.columns if c.startswith('case')]
with warnings.catch_warnings(record=True) as w:
    normalized = ns['preprocess'](raw)
    res = ns['differential_abundance'](normalized, case_cols, ctrl_cols)
    print('warnings:', [str(x.message) for x in w])
cls = truth.loc[res['protein'], 'class'].values
called = res[res['padj'] < 0.05]
cc = truth.loc[called['protein'], 'class']
print(f'tested {len(res)} of {len(raw)} | called {len(called)} | null FP {int((cc == "null").sum())} | '
      f'realized FDR {100 * (cc == "null").mean():.1f}% | up {int((cc == "up").sum())}/{int((truth["class"] == "up").sum())} '
      f'down {int((cc == "down").sum())}/{int((truth["class"] == "down").sum())}')
dropped = sorted(set(raw.index) - set(res['protein']))
print('dropped silently by the >=2-per-group rule:', len(dropped), truth.loc[dropped, 'class'].value_counts().to_dict())
onoff = [p for p in dropped if normalized.loc[p, ctrl_cols].notna().sum() >= 9 and normalized.loc[p, case_cols].notna().sum() == 0
         or normalized.loc[p, case_cols].notna().sum() >= 9 and normalized.loc[p, ctrl_cols].notna().sum() == 0]
print('agent-added undetected-in-one-group list (>=9/12 vs 0/12):', len(onoff), truth.loc[onoff, 'class'].value_counts().to_dict())
from scipy import stats
from statsmodels.stats.multitest import multipletests
p_student = [stats.ttest_ind(normalized.loc[p, case_cols].dropna(), normalized.loc[p, ctrl_cols].dropna()).pvalue for p in res['protein']]
print('Student default calls:', int((multipletests(p_student, method='fdr_bh')[1] < 0.05).sum()),
      '| Holm-Sidak default calls:', int((multipletests(res['pvalue'])[1] < 0.05).sum()))
