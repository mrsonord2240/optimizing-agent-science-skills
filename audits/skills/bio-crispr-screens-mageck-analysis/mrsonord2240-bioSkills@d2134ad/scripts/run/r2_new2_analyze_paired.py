import pandas as pd

gs = pd.read_csv("r2_new2_paired_mle.gene_summary.txt", sep="\t")
hits = [f"GENE{i}" for i in range(10)]
rec = gs[gs['Gene'].isin(hits)]
print("MLE per-donor-covariate: recovered FDR<0.05:", (rec['treatment|fdr'] < 0.05).sum(), "/10")
print("MLE per-donor-covariate: recovered wald-fdr<0.05:", (rec['treatment|wald-fdr'] < 0.05).sum(), "/10")
print(rec[['Gene', 'treatment|beta', 'treatment|fdr', 'treatment|wald-fdr']].to_string())
nonhits = gs[~gs['Gene'].isin(hits)]
print("MLE false positives among 30 neutral genes:", (nonhits['treatment|fdr'] < 0.05).sum())

gs2 = pd.read_csv("r2_new2_paired_test.gene_summary.txt", sep="\t")
rec2 = gs2[gs2['id'].isin(hits)]
print("mageck test --paired: recovered neg|fdr<0.05:", (rec2['neg|fdr'] < 0.05).sum(), "/10")
nonhits2 = gs2[~gs2['id'].isin(hits)]
print("mageck test --paired: false positives:", (nonhits2['neg|fdr'] < 0.05).sum())
