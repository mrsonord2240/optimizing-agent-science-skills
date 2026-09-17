# Regression test for pre-fix Input 1 (Canonical): Welch t-test + explicit BH FDR with a
# detection-rate-confound block, independent synthetic data (not the Skill's own example).
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(20260916)
n_case, n_ctrl = 30, 30
n_features = 500
n_true = 30
n_confound = 10

base = rng.normal(loc=12, scale=1.0, size=(n_case + n_ctrl, n_features))
case_idx = np.arange(n_case)
ctrl_idx = np.arange(n_case, n_case + n_ctrl)

# planted true shifts, mixed direction, 1.5-3x on linear scale -> log2 shift of ~0.6-1.6
true_shift = rng.uniform(0.6, 1.6, n_true) * rng.choice([-1, 1], n_true)
base[np.ix_(case_idx, np.arange(n_true))] += true_shift

# detection-rate-confound block: same true concentration, but 50% of case values are
# non-detects (set to 0 pre-log) -- differs only in detection rate, not real concentration
conf_start = n_true
conf_cols = np.arange(conf_start, conf_start + n_confound)
intens = 2 ** base  # to linear scale
non_detect_mask = rng.random((n_case, n_confound)) < 0.5
for k, col in enumerate(conf_cols):
    intens[case_idx[non_detect_mask[:, k]], col] = 0

df = pd.DataFrame(intens.T, columns=[f'S{i}' for i in range(n_case + n_ctrl)])
df.index = [f'M{i}' for i in range(n_features)]
case_cols = df.columns[:n_case]
ctrl_cols = df.columns[n_case:]

logged = np.log2(df.replace(0, np.nan))
pvals, lfc, feats = [], [], []
detect_case, detect_ctrl = [], []
for feat in logged.index:
    a = logged.loc[feat, case_cols].dropna().values
    b = logged.loc[feat, ctrl_cols].dropna().values
    if len(a) >= 3 and len(b) >= 3:
        pvals.append(ttest_ind(a, b, equal_var=False)[1])
        lfc.append(a.mean() - b.mean())
        feats.append(feat)
        detect_case.append(len(a) / n_case)
        detect_ctrl.append(len(b) / n_ctrl)

res = pd.DataFrame({'feature': feats, 'log2fc': lfc, 'pval': pvals,
                     'detect_case': detect_case, 'detect_ctrl': detect_ctrl})
res['padj'] = multipletests(res['pval'], method='fdr_bh')[1]
hits = res[(res['padj'] < 0.05) & (res['log2fc'].abs() > 1)]

true_feat_names = set(f'M{i}' for i in range(n_true))
confound_feat_names = set(f'M{i}' for i in conf_cols)
hit_names = set(hits['feature'])

tp = len(hit_names & true_feat_names)
fp_other = len(hit_names - true_feat_names - confound_feat_names)
confound_flagged = len(hit_names & confound_feat_names)

print(f'Total hits (padj<0.05, |log2fc|>1): {len(hits)} of {n_features} tested features')
print(f'True positives recovered: {tp} of {n_true}')
print(f'False negatives (true but missed): {n_true - tp} of {n_true}')
print(f'Detection-rate-confound features flagged as hits (should be 0): {confound_flagged} of {n_confound}')
print(f'Other false positives: {fp_other}')
print()
print('Confound block detail (padj, detect rates):')
print(res[res['feature'].isin(confound_feat_names)][['feature', 'log2fc', 'padj', 'detect_case', 'detect_ctrl']].to_string(index=False))
