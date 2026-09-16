# Verbatim from SKILL.md Step 3, adapted only for the actual column name ('Gene' not 'Gene' capital-G matches; counts file
# uses 'Gene' column same as SKILL.md's example which drops 'Gene' too)
import pandas as pd
import numpy as np

counts = pd.read_csv('experiment.count.txt', sep='\t', index_col=0)
genes = counts['Gene']
count_matrix = counts.drop('Gene', axis=1)

def gini(x):
    x = np.sort(x[x > 0].astype(float))
    if x.size == 0:
        return np.nan
    n = x.size
    cumx = np.cumsum(x)
    return (n + 1 - 2 * np.sum(cumx) / cumx[-1]) / n

per_sample = pd.DataFrame({
    'pct_zero': (count_matrix == 0).sum() / len(count_matrix) * 100,
    'gini': count_matrix.apply(gini),
    'reads_per_sgrna': count_matrix.sum() / len(count_matrix),
})

log_counts = np.log10(count_matrix + 1)
pearson = log_counts.corr()
print(per_sample)
print('Replicate Pearson:', pearson.values[pearson.values < 1].mean())
