# Verbatim from the FIXED SKILL.md Step 3 (fork commit 6847328), run against real
# HAP1 TKOv3 data (experiment.count.txt: T0, T18_A, T18_B, T18_C).
import re
from itertools import combinations
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

def condition(sample_name):
    return re.sub(r'_(?:[Rr]ep|[Rr])?\d+$|_[A-Z]$', '', sample_name)

groups = {}
for col in count_matrix.columns:
    groups.setdefault(condition(col), []).append(col)

replicate_pairs = [pearson.loc[a, b] for cols in groups.values() for a, b in combinations(cols, 2)]

print(per_sample)
print('Groups:', groups)
if replicate_pairs:
    print('Replicate Pearson (within-condition pairs only):', np.mean(replicate_pairs))
else:
    print('Replicate Pearson: no condition has >=2 samples -- cannot assess replicate concordance')

# Cross-check against the naive (pre-fix) formula for comparison
naive = pearson.values[pearson.values < 1].mean()
print('Naive (pre-fix) formula for comparison:', naive)
