# NEW input (not in the pre-fix audit): paired pre/post design -- exercises the Decision
# Tree row "2 groups, paired/pre-post -> Paired t-test or Wilcoxon signed-rank" and the
# "Discards within-subject pairing if analyzed unpaired -> underpowered" warning, neither of
# which the pre-fix audit's 7 inputs touched.
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, ttest_ind
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(31415)
n_subj = 25
n_feat = 200
n_true = 20

subj_baseline = rng.normal(loc=10, scale=2.0, size=(n_subj, n_feat))  # large between-subject variance
delta = np.zeros(n_feat)
true_idx = np.arange(n_true)
delta[true_idx] = rng.uniform(0.4, 1.0, n_true) * rng.choice([-1, 1], n_true)
noise = rng.normal(scale=0.3, size=(n_subj, n_feat))  # small within-subject noise
post = subj_baseline + delta + noise
pre = subj_baseline

pre_df = pd.DataFrame(pre.T, index=[f'M{i}' for i in range(n_feat)], columns=[f'S{i}' for i in range(n_subj)])
post_df = pd.DataFrame(post.T, index=[f'M{i}' for i in range(n_feat)], columns=[f'S{i}' for i in range(n_subj)])

# --- correct: paired Wilcoxon signed-rank, matched by subject ---
paired_p, paired_lfc = [], []
for feat in pre_df.index:
    a = pre_df.loc[feat].values
    b = post_df.loc[feat].values
    stat, p = wilcoxon(b, a)
    paired_p.append(p)
    paired_lfc.append(np.mean(b - a))
res_paired = pd.DataFrame({'feature': pre_df.index, 'lfc': paired_lfc, 'pval': paired_p})
res_paired['padj'] = multipletests(res_paired['pval'], method='fdr_bh')[1]
hits_paired = set(res_paired[res_paired['padj'] < 0.05]['feature'])

# --- wrong-but-tempting: unpaired Welch treating pre/post as two independent groups ---
unpaired_p = []
for feat in pre_df.index:
    a = pre_df.loc[feat].values
    b = post_df.loc[feat].values
    unpaired_p.append(ttest_ind(b, a, equal_var=False)[1])
res_unpaired = pd.DataFrame({'feature': pre_df.index, 'pval': unpaired_p})
res_unpaired['padj'] = multipletests(res_unpaired['pval'], method='fdr_bh')[1]
hits_unpaired = set(res_unpaired[res_unpaired['padj'] < 0.05]['feature'])

true_names = set(f'M{i}' for i in true_idx)
print(f'True planted pre/post changes: {n_true} of {n_feat} features')
print(f'Paired Wilcoxon hits (padj<0.05): {len(hits_paired)}  |  true positives: {len(hits_paired & true_names)} of {n_true}  |  false positives: {len(hits_paired - true_names)}')
print(f'Unpaired Welch hits (padj<0.05):  {len(hits_unpaired)}  |  true positives: {len(hits_unpaired & true_names)} of {n_true}  |  false positives: {len(hits_unpaired - true_names)}')
print()
print('Skill claim under test: analyzing paired data as unpaired is "underpowered" (loses the within-subject '
      'variance reduction) -- expect the unpaired test to recover fewer true positives than the paired test '
      'given identical data, because large between-subject variance (SD=2.0) swamps the within-subject signal '
      '(noise SD=0.3) when subjects are not matched.')
