\
# Same as 03_cellphonedb_specificity.py, but wrapped in `if __name__ == '__main__':` to test
# whether that Windows multiprocessing entry-point guard is what SKILL.md's documented
# CellPhoneDB code block is missing (see cpdb_run1.log: RuntimeError from
# `score_interactions=True` -> `Pool(processes=threads)` without the guard).
import scanpy as sc
import pandas as pd
import anndata as ad
import time


def main():
    adata = sc.read_h5ad(r"F:\OpenScience\audits\bio-single-cell-cell-communication\data\adata_annotated.h5ad")

    counts_adata = ad.AnnData(X=adata.X, obs=adata.obs[[]], var=adata.var[[]])
    counts_adata.write(r"F:\OpenScience\audits\bio-single-cell-cell-communication\run\counts_normalized.h5ad")

    meta = pd.DataFrame({'Cell': adata.obs_names, 'cell_type': adata.obs['majority_voting'].astype(str)})
    meta.to_csv(r"F:\OpenScience\audits\bio-single-cell-cell-communication\run\meta.tsv", sep='\t', index=False)

    from cellphonedb.src.core.methods import cpdb_statistical_analysis_method
    t0 = time.time()

    results = cpdb_statistical_analysis_method.call(
        cpdb_file_path=r"F:\OpenScience\audits\bio-single-cell-cell-communication\run\cpdb_db\cellphonedb.zip",
        meta_file_path=r"F:\OpenScience\audits\bio-single-cell-cell-communication\run\meta.tsv",
        counts_file_path=r"F:\OpenScience\audits\bio-single-cell-cell-communication\run\counts_normalized.h5ad",
        counts_data='hgnc_symbol',
        threshold=0.1, iterations=100, pvalue=0.05,
        score_interactions=True, threads=1,
        output_path=r"F:\OpenScience\audits\bio-single-cell-cell-communication\run\cpdb_out")

    print(f"Elapsed: {time.time()-t0:.1f}s")
    pvalues = results['pvalues']
    means = results['means']
    print("pvalues shape:", pvalues.shape)
    print("means shape:", means.shape)

    sig_cols = [c for c in pvalues.columns if '|' in c]
    sig_long = pvalues.melt(id_vars=[c for c in pvalues.columns if c not in sig_cols],
                             value_vars=sig_cols, var_name='cell_pair', value_name='pval')
    sig_hits = sig_long[sig_long['pval'] < 0.05]
    print("Total significant (pair, interaction) combos at p<0.05:", len(sig_hits))

    mono_nk = [c for c in sig_cols if 'Classical monocytes' in c and 'CD16+ NK cells' in c]
    print("Monocyte<->NK columns found:", mono_nk[:5])
    if mono_nk:
        sub = pvalues[pvalues[mono_nk[0]] < 0.05][['interacting_pair', mono_nk[0]]]
        print(f"Significant pairs for {mono_nk[0]} (n={len(sub)}):")
        print(sub.head(20).to_string())


if __name__ == '__main__':
    main()
