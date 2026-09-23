import pandas as pd

bf = pd.read_csv('swapped_bayes_factor.txt', sep='\t')
numeric = pd.to_numeric(bf['BF'], errors='coerce')
assert len(bf) == 18053
assert numeric.isna().all(), numeric.notna().sum()
print(f'PASS guard regression: swapped file has {numeric.isna().sum()}/{len(bf)} NaN BF values and checker rejected it')
