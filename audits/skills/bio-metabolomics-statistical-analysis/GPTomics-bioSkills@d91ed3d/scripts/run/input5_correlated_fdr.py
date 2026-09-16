"""
Audit input 5 (Stress / multi-part) -- bio-metabolomics-statistical-analysis
User request: "I ran Welch t-tests + BH FDR and got '180 significant
metabolites' out of 900 features, but I know a lot of these are adducts and
isotopologues of the same handful of compounds. Is my hit list trustworthy,
and how many real independent signals does it actually represent?"

Synthetic data built explicitly to test the Skill's own claim ("one real
signal lights up its whole correlated cluster ... collapse features to
compounds before counting 'how many metabolites changed'"): 90 latent
"compounds", each represented by a block of 10 highly correlated features
(simulating adducts/isotopologues), with a known number of truly-differing
compounds. Ground truth = number of independent signals, known exactly.
"""
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(123)
n_per_group = 25
n_compounds = 90
block_size = 10
n_features = n_compounds * block_size          # 900 features
n_true_compounds = 12                           # only 12 independent true signals

samples = [f's{i}' for i in range(2 * n_per_group)]
group = np.array(['control'] * n_per_group + ['case'] * n_per_group)
case_cols = np.where(group == 'case')[0]

feature_names, compound_id = [], []
X = np.zeros((n_features, 2 * n_per_group))
row = 0
compound_shift = rng.uniform(0.8, 1.5, size=n_true_compounds)  # log2 fold change per true compound
for c in range(n_compounds):
    # shared compound-level abundance signal (drives within-block correlation)
    compound_level = rng.normal(loc=12, scale=1.0, size=2 * n_per_group)
    if c < n_true_compounds:
        compound_level[case_cols] += compound_shift[c]
    for k in range(block_size):
        # each "adduct/isotopologue" feature = shared compound signal + small feature-specific noise
        feat_noise = rng.normal(scale=0.15, size=2 * n_per_group)
        X[row, :] = compound_level + feat_noise
        feature_names.append(f'C{c}_adduct{k}')
        compound_id.append(c)
        row += 1

intensities = pd.DataFrame(X, index=feature_names, columns=samples)
case = [s for s, g in zip(samples, group) if g == 'case']
ctrl = [s for s, g in zip(samples, group) if g == 'control']

pvals, lfc = [], []
for feat in intensities.index:
    a = intensities.loc[feat, case].values
    b = intensities.loc[feat, ctrl].values
    pvals.append(ttest_ind(a, b, equal_var=False)[1])
    lfc.append(a.mean() - b.mean())

res = pd.DataFrame({'feature': feature_names, 'compound': compound_id, 'log2fc': lfc, 'pval': pvals})
res['padj'] = multipletests(res['pval'], method='fdr_bh')[1]
res['hit'] = res['padj'] < 0.05

n_feature_hits = int(res['hit'].sum())
hit_compounds = sorted(res.loc[res['hit'], 'compound'].unique())
n_independent_hits = len(hit_compounds)
true_compounds = set(range(n_true_compounds))
tp_compounds = len(set(hit_compounds) & true_compounds)
fp_compounds = len(set(hit_compounds) - true_compounds)

print(f'Naive feature-level count: "{n_feature_hits} significant metabolites" out of {n_features} features tested')
print(f'After collapsing to compound (block) level: {n_independent_hits} independent signals hit')
print(f'True independent signals planted: {n_true_compounds}')
print(f'Independent signals correctly recovered: {tp_compounds} of {n_true_compounds}')
print(f'False independent-signal compounds: {fp_compounds}')
print()
print(f'Inflation factor if the feature count were reported as "metabolites changed": '
      f'{n_feature_hits} features / {n_independent_hits} true independent signals = '
      f'{n_feature_hits / max(n_independent_hits, 1):.1f}x')
print()
print('Per-compound hit summary (block size = 10 features/compound):')
block_summary = res.groupby('compound')['hit'].sum()
print(f'  Mean features-per-hit-compound: {block_summary[block_summary > 0].mean():.1f} of 10')
print(f'  Compounds with ALL 10 features flagged: {(block_summary == 10).sum()} of {len(hit_compounds)} hit compounds')

# Effective-number-of-tests style correction: Bonferroni-on-features vs Bonferroni-on-compounds
bonf_features_thresh = 0.05 / n_features
bonf_compounds_thresh = 0.05 / n_compounds
n_bonf_feature_hits = int((res['pval'] < bonf_features_thresh).sum())
# min p-value per compound, tested against a compound-level Bonferroni threshold
min_p_per_compound = res.groupby('compound')['pval'].min()
n_bonf_compound_hits = int((min_p_per_compound < bonf_compounds_thresh).sum())
print(f'\nBonferroni-on-{n_features}-features threshold hits: {n_bonf_feature_hits} features '
      f'(over-conservative per-feature correction, per Skill guidance)')
print(f'Bonferroni-on-{n_compounds}-compounds (effective-tests-style) threshold hits: '
      f'{n_bonf_compound_hits} independent compounds (recovers {len(set(min_p_per_compound[min_p_per_compound < bonf_compounds_thresh].index) & true_compounds)} of {n_true_compounds} true signals)')
