import pandas as pd

r1 = pd.read_csv("combo_mle_run1.gene_summary.txt", sep="\t")
r2 = pd.read_csv("combo_mle_run2.gene_summary.txt", sep="\t")

r1 = r1.set_index("Gene").sort_index()
r2 = r2.set_index("Gene").sort_index()

beta_col = "interaction|beta"
fdr_col = "interaction|fdr"

beta_diff = (r1[beta_col] - r2[beta_col]).abs()
fdr_diff = (r1[fdr_col] - r2[fdr_col]).abs()

n_beta_differs = (beta_diff > 1e-12).sum()
n_fdr_differs = (fdr_diff > 1e-12).sum()

print(f"Genes total: {len(r1)}")
print(f"interaction|beta differing between runs (tol 1e-12): {n_beta_differs}/{len(r1)}")
print(f"interaction|fdr differing between runs (tol 1e-12): {n_fdr_differs}/{len(r1)}")
print()
print("Planted hit GENE_SL:")
print("  run1 beta/fdr:", r1.loc["GENE_SL", beta_col], r1.loc["GENE_SL", fdr_col])
print("  run2 beta/fdr:", r2.loc["GENE_SL", beta_col], r2.loc["GENE_SL", fdr_col])
print()
print("Rank of GENE_SL by interaction|beta (most negative = rank 1), run1:",
      int((r1[beta_col] < r1.loc["GENE_SL", beta_col]).sum() + 1))
print("Full fdr comparison, all genes:")
print(pd.DataFrame({"run1_fdr": r1[fdr_col], "run2_fdr": r2[fdr_col], "diff": fdr_diff}).sort_values("diff", ascending=False))
