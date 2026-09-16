import pandas as pd, numpy as np
counts = pd.read_csv('experiment.count.txt', sep='\t', index_col=0)
count_matrix = counts.drop('Gene', axis=1)
log_counts = np.log10(count_matrix + 1)
pearson = log_counts.corr()
print(pearson)
print()
true_replicate_pairs = [('T18_A','T18_B'), ('T18_A','T18_C'), ('T18_B','T18_C')]
nonreplicate_pairs = [('T0','T18_A'), ('T0','T18_B'), ('T0','T18_C')]
print('TRUE replicate pairs (T18 vs T18):', [round(pearson.loc[a,b],3) for a,b in true_replicate_pairs],
      'mean=', round(np.mean([pearson.loc[a,b] for a,b in true_replicate_pairs]),3))
print('Non-replicate pairs (T0 vs T18, different timepoints):', [round(pearson.loc[a,b],3) for a,b in nonreplicate_pairs],
      'mean=', round(np.mean([pearson.loc[a,b] for a,b in nonreplicate_pairs]),3))
print('SKILL.md formula (all off-diagonal pairs mixed):', pearson.values[pearson.values < 1].mean())
