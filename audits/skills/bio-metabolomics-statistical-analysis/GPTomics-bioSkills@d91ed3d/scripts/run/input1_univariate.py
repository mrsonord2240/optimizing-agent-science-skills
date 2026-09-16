"""
Audit input 1 (Canonical) -- bio-metabolomics-statistical-analysis
User request: "I have LC-MS intensities for 60 case/control plasma samples
(synthetic). Run Welch t-tests with explicit BH FDR and report fold changes;
tell me how many of the real changes I actually recovered."

Independent synthetic dataset (not copied from the Skill's own example --
different N, effect sizes, and a detection-rate-confound feature block to
probe the Skill's own "Log with zeros / detection-rate confound" failure mode).
Ground truth is known so FDR control and recovery can be checked directly.
"""
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(42)
n_per_group = 30
n_features = 500
n_true = 30          # truly shifted features
n_confound = 10       # features with a detection-rate difference only (no true shift)

samples = [f's{i}' for i in range(2 * n_per_group)]
features = [f'M{i}' for i in range(n_features)]
group = np.array(['control'] * n_per_group + ['case'] * n_per_group)
case_cols = np.where(group == 'case')[0]
ctrl_cols = np.where(group == 'control')[0]

raw = rng.lognormal(mean=9, sigma=0.5, size=(n_features, 2 * n_per_group))

# Plant true fold changes, varying magnitude (1.5x - 3x), some up some down
true_idx = np.arange(n_true)
fc_truth = rng.uniform(np.log2(1.5), np.log2(3.0), size=n_true) * rng.choice([1, -1], size=n_true)
for i, fc in zip(true_idx, fc_truth):
    raw[i, case_cols] *= 2 ** fc

# Detection-rate-confound block: same true mean in both groups, but case group
# has a higher missing (non-detect) rate -> should NOT survive as a hit once
# detection rate is reported, per the Skill's own guidance.
confound_idx = np.arange(n_true, n_true + n_confound)
for i in confound_idx:
    drop_mask = rng.random(len(case_cols)) < 0.5   # 50% non-detect in case only
    raw[i, case_cols[drop_mask]] = 0.0

intensities = pd.DataFrame(raw, index=features, columns=samples)

case = [s for s, g in zip(samples, group) if g == 'case']
ctrl = [s for s, g in zip(samples, group) if g == 'control']

logged = np.log2(intensities.replace(0, np.nan))  # transform before testing; zeros -> NaN (left-censored)

pvals, lfc, n_case_detected, n_ctrl_detected = [], [], [], []
for feat in logged.index:
    a = logged.loc[feat, case].dropna().values
    b = logged.loc[feat, ctrl].dropna().values
    n_case_detected.append(len(a))
    n_ctrl_detected.append(len(b))
    if len(a) >= 3 and len(b) >= 3:
        pvals.append(ttest_ind(a, b, equal_var=False)[1])   # Welch, per Skill guidance
        lfc.append(a.mean() - b.mean())                      # geometric-mean ratio (difference of log-means)
    else:
        pvals.append(np.nan)
        lfc.append(np.nan)

res = pd.DataFrame({
    'feature': logged.index, 'log2fc': lfc, 'pval': pvals,
    'n_case_detected': n_case_detected, 'n_ctrl_detected': n_ctrl_detected,
}).dropna(subset=['pval'])
res['detect_rate_case'] = res['n_case_detected'] / n_per_group
res['detect_rate_ctrl'] = res['n_ctrl_detected'] / n_per_group
res['padj'] = multipletests(res['pval'], method='fdr_bh')[1]   # explicit BH per Skill guidance
res['hit'] = (res['padj'] < 0.05) & (res['log2fc'].abs() > 1)  # 2-fold + FDR 5%, per Skill's stated convention
res = res.sort_values('padj')

hits = set(res.loc[res['hit'], 'feature'])
true_set = set(features[i] for i in true_idx)
confound_set = set(features[i] for i in confound_idx)

n_hit = len(hits)
tp = len(hits & true_set)
fp_confound = len(hits & confound_set)   # would be a false positive driven purely by detection-rate confound
fp_other = n_hit - tp - fp_confound
fn = len(true_set - hits)

print(f'Total hits (padj<0.05, |log2fc|>1): {n_hit} of {len(res)} tested features')
print(f'True positives recovered: {tp} of {n_true}')
print(f'False negatives (true but missed): {fn} of {n_true}')
print(f'Detection-rate-confound features flagged as hits (should be 0 if guidance followed): {fp_confound} of {n_confound}')
print(f'Other false positives: {fp_other}')
print()
print('Detection-rate-confound block detail (per-feature detect rates):')
print(res[res['feature'].isin(confound_set)][['feature', 'log2fc', 'padj', 'detect_rate_case', 'detect_rate_ctrl']].to_string(index=False))
print()
print('Top 10 hits by padj:')
print(res.head(10)[['feature', 'log2fc', 'pval', 'padj', 'detect_rate_case', 'detect_rate_ctrl']].to_string(index=False))

# Empirical FDR check against ground truth
observed_fdr = fp_other / n_hit if n_hit else float('nan')
print(f'\nEmpirical false-discovery proportion among hits (excluding confound features): {observed_fdr:.3f} (nominal target 0.05)')
