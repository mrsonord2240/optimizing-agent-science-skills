import pandas as pd

bf = pd.read_csv('canonical_bayes_factor.txt', sep='\t')
mg = pd.read_csv('mageck_hap1.gene_summary.txt', sep='\t')
bagel = set(bf.loc[bf.BF > 6, 'GENE'])
mageck = set(mg.loc[mg['neg|fdr'] < 0.05, 'id'])
intersection = bagel & mageck
jaccard = len(intersection) / len(bagel | mageck)
assert len(mageck) > 500 and len(intersection) / len(mageck) > 0.90
print(f'PASS comparison: BAGEL={len(bagel)}, MAGeCK={len(mageck)}, intersection={len(intersection)}, Jaccard={jaccard:.3f}')
