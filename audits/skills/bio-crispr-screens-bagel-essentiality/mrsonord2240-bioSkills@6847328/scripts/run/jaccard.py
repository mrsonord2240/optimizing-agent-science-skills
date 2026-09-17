import pandas as pd

bf = pd.read_csv("bayes_factor_seedA.txt", sep="\t")
mg = pd.read_csv("mageck_hap1.gene_summary.txt", sep="\t")
bagel_hits = set(bf[bf.BF > 6].GENE)
mageck_hits = set(mg[mg["neg|fdr"] < 0.05].id)
inter = bagel_hits & mageck_hits
union = bagel_hits | mageck_hits
print("bagel hits:", len(bagel_hits))
print("mageck hits:", len(mageck_hits))
print("intersection:", len(inter))
print("union:", len(union))
print("jaccard:", len(inter) / len(union))
print("mageck recovered by bagel:", len(inter), "/", len(mageck_hits), "=", len(inter) / len(mageck_hits))
