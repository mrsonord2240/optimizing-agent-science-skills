import pandas as pd
wb = pd.read_csv("r2_input5_withbatch_pr2.gene_summary.txt", sep="\t")
nb = pd.read_csv("r2_input5_nobatch_pr2.gene_summary.txt", sep="\t")
wb10 = pd.read_csv("r2_input5_withbatch_pr10.gene_summary.txt", sep="\t")
hit_genes = [g for g in wb['Gene'] if g.startswith('HIT')]
print("n planted hits:", len(hit_genes))
print("withbatch pr=2 sig:", (wb[wb['Gene'].isin(hit_genes)]['treatment|fdr'] < 0.05).sum(), "/", len(hit_genes))
print("nobatch   pr=2 sig:", (nb[nb['Gene'].isin(hit_genes)]['treatment|fdr'] < 0.05).sum(), "/", len(hit_genes))
print("withbatch pr=10 sig:", (wb10[wb10['Gene'].isin(hit_genes)]['treatment|fdr'] < 0.05).sum(), "/", len(hit_genes))
print("beta withbatch mean:", wb[wb['Gene'].isin(hit_genes)]['treatment|beta'].mean())
print("beta nobatch   mean:", nb[nb['Gene'].isin(hit_genes)]['treatment|beta'].mean())
print("wald-fdr withbatch sig:", (wb[wb['Gene'].isin(hit_genes)]['treatment|wald-fdr'] < 0.05).sum(), "/", len(hit_genes))
print("wald-fdr nobatch sig:", (nb[nb['Gene'].isin(hit_genes)]['treatment|wald-fdr'] < 0.05).sum(), "/", len(hit_genes))
