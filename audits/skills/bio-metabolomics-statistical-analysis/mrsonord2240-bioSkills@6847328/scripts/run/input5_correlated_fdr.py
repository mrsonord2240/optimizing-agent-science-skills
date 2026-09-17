# Regression test for pre-fix Input 5 (Stress): correlated-feature (adduct/isotopologue block)
# multiple-testing check -- naive per-feature BH count vs collapsed-to-compound independent
# signal count.
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(777)
n_compounds = 90
block_size = 10
n_features = n_compounds * block_size
n_case, n_ctrl = 25, 25
n_true_compounds = 12

# each compound has a true latent signal; each of its 10 features (adducts/isotopologues)
# shares that signal plus independent feature-level noise
compound_true_shift = np.zeros(n_compounds)
true_compound_idx = rng.choice(n_compounds, n_true_compounds, replace=False)
compound_true_shift[true_compound_idx] = rng.uniform(0.8, 2.0, n_true_compounds) * rng.choice([-1, 1], n_true_compounds)

case_idx = np.arange(n_case)
X = rng.normal(loc=10, scale=1.0, size=(n_case + n_ctrl, n_features))
compound_id = np.repeat(np.arange(n_compounds), block_size)
for c in range(n_compounds):
    cols = np.where(compound_id == c)[0]
    X[np.ix_(case_idx, cols)] += compound_true_shift[c]

feat_names = [f'F{i}_cpd{compound_id[i]}' for i in range(n_features)]
df = pd.DataFrame(X.T, columns=[f'S{i}' for i in range(n_case + n_ctrl)], index=feat_names)
case_cols, ctrl_cols = df.columns[:n_case], df.columns[n_case:]

pvals = [ttest_ind(df.loc[f, case_cols], df.loc[f, ctrl_cols], equal_var=False)[1] for f in feat_names]
res = pd.DataFrame({'feature': feat_names, 'compound': compound_id, 'pval': pvals})
res['padj_feature'] = multipletests(res['pval'], method='fdr_bh')[1]
feature_hits = res[res['padj_feature'] < 0.05]
print(f'Naive feature-level count: "{len(feature_hits)} significant metabolites" out of {n_features} features tested')

# collapse to compound level: min p-value per compound (Bonferroni-within-block), then BH across compounds
compound_p = res.groupby('compound')['pval'].min() * block_size
compound_p = compound_p.clip(upper=1.0)
compound_padj = pd.Series(multipletests(compound_p.values, method='fdr_bh')[1], index=compound_p.index)
compound_hits = compound_padj[compound_padj < 0.05].index
true_recovered = len(set(compound_hits) & set(true_compound_idx))
false_compound_hits = len(set(compound_hits) - set(true_compound_idx))

print(f'After collapsing to compound (block) level: {len(compound_hits)} independent signals hit')
print(f'True independent signals planted: {n_true_compounds}')
print(f'Independent signals correctly recovered: {true_recovered} of {n_true_compounds}')
print(f'False independent-signal compounds: {false_compound_hits}')
inflation = len(feature_hits) / max(len(compound_hits), 1)
print(f'Inflation factor if feature count reported as "metabolites changed": '
      f'{len(feature_hits)} features / {len(compound_hits)} true independent signals = {inflation:.1f}x')

bonf_feature_hits = (res['pval'] < 0.05 / n_features).sum()
bonf_compound_p = compound_p[compound_p < 0.05 / n_compounds]
bonf_compound_recovered = len(set(bonf_compound_p.index) & set(true_compound_idx))
print(f'Bonferroni-on-{n_features}-features threshold hits: {bonf_feature_hits} features')
print(f'Bonferroni-on-{n_compounds}-compounds threshold hits: {len(bonf_compound_p)} independent compounds '
      f'(recovers {bonf_compound_recovered} of {n_true_compounds} true signals)')
