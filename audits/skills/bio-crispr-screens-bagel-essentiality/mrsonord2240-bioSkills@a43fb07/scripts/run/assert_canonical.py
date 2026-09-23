import pandas as pd

fc = pd.read_csv('canonical_fc.foldchange', sep='\t')
bf = pd.read_csv('canonical_bayes_factor.txt', sep='\t')
pr = pd.read_csv('canonical_precision_recall.txt', sep='\t')
assert len(fc) > 70000, len(fc)
assert len(bf) == 18053 and list(bf.columns) == ['GENE', 'BF'], bf.columns.tolist()
assert bf['BF'].notna().all()
assert (bf['BF'] > 6).sum() > 1000
assert len(pr) == 18053 and {'BF', 'Precision', 'Recall'}.issubset(pr.columns)
print(f'PASS canonical: {len(fc)} sgRNAs, {len(bf)} genes, {(bf.BF > 6).sum()} BF>6, {len(pr)} PR rows')
