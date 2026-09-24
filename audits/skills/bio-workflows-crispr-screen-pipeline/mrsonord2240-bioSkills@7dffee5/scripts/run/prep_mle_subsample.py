# Subsample the real experiment.count.txt (HAP1 TKOv3, 18,056 genes) down to 1,500 genes
# so mageck mle (genuinely multi-hour at genome scale by design, per TOOLS.md) finishes in
# seconds for the Step 6b permutation-round regression test.
import pandas as pd

df = pd.read_csv('experiment.count.txt', sep='\t')
genes = df['Gene'].unique()[:1500]
sub = df[df['Gene'].isin(genes)].reset_index(drop=True)
sub.to_csv('mle_subsample.count.txt', sep='\t', index=False)
print(sub.shape, sub['Gene'].nunique())
