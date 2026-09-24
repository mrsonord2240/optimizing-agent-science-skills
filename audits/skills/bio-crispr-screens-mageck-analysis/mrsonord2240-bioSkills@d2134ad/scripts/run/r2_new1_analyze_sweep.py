import pandas as pd
pr1 = pd.read_csv("r2_new1_pr1.gene_summary.txt", sep="\t")
pr2 = pd.read_csv("r2_new1_pr2.gene_summary.txt", sep="\t")
pr5 = pd.read_csv("r2_new1_pr5.gene_summary.txt", sep="\t")
for label, df in [("pr1", pr1), ("pr2", pr2), ("pr5", pr5)]:
    print(label, "fdr<0.05:", (df['treatment|fdr'] < 0.05).sum(),
          " wald-fdr<0.05:", (df['treatment|wald-fdr'] < 0.05).sum())

sig2 = set(pr2[pr2['treatment|fdr'] < 0.05]['Gene'])
sig5 = set(pr5[pr5['treatment|fdr'] < 0.05]['Gene'])
flips = sig2.symmetric_difference(sig5)
print("flips between pr2 and pr5:", len(flips), "=",
      len(flips) / len(sig2) * 100 if sig2 else 0, "% of pr2 hit count")
