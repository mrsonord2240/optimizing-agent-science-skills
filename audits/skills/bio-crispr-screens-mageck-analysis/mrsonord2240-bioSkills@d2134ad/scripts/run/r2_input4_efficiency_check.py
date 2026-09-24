import pandas as pd
test = pd.read_csv("r2_input4_test.gene_summary.txt", sep="\t")
hits_test = test[test['neg|fdr'] < 0.05]
print("test hits FDR<0.05:", len(hits_test))
eff = pd.read_csv("r2_input4_mle_eff.gene_summary.txt", sep="\t")
noeff = pd.read_csv("r2_input4_mle_noeff.gene_summary.txt", sep="\t")
hit_genes = [g for g in eff['Gene'] if g.startswith('HIT')]
print("mle+eff hits FDR<0.05:", (eff[eff['Gene'].isin(hit_genes)]['drug|fdr'] < 0.05).sum(), "/", len(hit_genes))
print("mle-noeff hits FDR<0.05:", (noeff[noeff['Gene'].isin(hit_genes)]['drug|fdr'] < 0.05).sum(), "/", len(hit_genes))
print("mean drug|beta eff:", eff[eff['Gene'].isin(hit_genes)]['drug|beta'].mean())
print("mean drug|beta noeff:", noeff[noeff['Gene'].isin(hit_genes)]['drug|beta'].mean())
