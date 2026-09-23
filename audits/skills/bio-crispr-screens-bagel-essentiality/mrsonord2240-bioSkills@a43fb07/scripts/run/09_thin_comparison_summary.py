import pandas as pd

real = pd.read_csv('canonical_bayes_factor.txt', sep='\t')
thin = pd.read_csv('thin_bayes_factor.txt', sep='\t')
controls = {'LacZ', 'luciferase', 'EGFP'}
real_max = real.loc[~real['GENE'].isin(controls), 'BF'].abs().max()
thin_max = thin['BF'].abs().max()
ratio = thin_max / real_max
assert ratio > 10
print(f'PASS coverage contrast: thin max={thin_max:.3f}; real max excluding controls={real_max:.3f}; ratio={ratio:.3f}x')
