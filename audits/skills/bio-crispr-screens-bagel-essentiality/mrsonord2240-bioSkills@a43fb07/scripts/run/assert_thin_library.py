import pandas as pd

thin = pd.read_csv('thin_bayes_factor.txt', sep='\t')
real = pd.read_csv('canonical_bayes_factor.txt', sep='\t')
assert list(thin.columns) == ['GENE', 'BF', 'STD', 'NumObs'], thin.columns.tolist()
assert len(thin) == 200 and thin['BF'].notna().all()
ratio = thin['BF'].abs().max() / real['BF'].abs().max()
assert ratio > 1, ratio
print(f'PASS thin-library parse: {len(thin)} genes, max |BF|={thin.BF.abs().max():.1f}, real ratio={ratio:.1f}x (does not reproduce the Skill claim of ~2,400)')
