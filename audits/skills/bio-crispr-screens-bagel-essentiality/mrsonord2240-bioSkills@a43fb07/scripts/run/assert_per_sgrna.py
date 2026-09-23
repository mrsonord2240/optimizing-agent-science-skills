import pandas as pd

gene = pd.read_csv('canonical_bayes_factor.txt', sep='\t').set_index('GENE')
sgrna = pd.read_csv('sgrna_bayes_factor.txt', sep='\t')
rps3 = sgrna.loc[sgrna['GENE'] == 'RPS3', 'BF']
assert {'RNA', 'GENE', 'BF'}.issubset(sgrna.columns)
assert len(rps3) >= 3
assert abs(rps3.sum() - gene.loc['RPS3', 'BF']) < 1e-6
print(f'PASS per-sgRNA: {len(sgrna)} guides; RPS3={len(rps3)} contributions sum {rps3.sum():.3f}')
