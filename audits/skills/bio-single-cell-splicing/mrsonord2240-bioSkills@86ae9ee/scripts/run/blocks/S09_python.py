import pandas as pd
import scanpy as sc
import psix

adata = sc.read_h5ad('cells.h5ad')                       # normalised expression with X_pca
latent = pd.DataFrame(adata.obsm['X_pca'][:, :20], index=adata.obs_names)   # cells x dims (or a TSV path)

# psi_matrix.tsv, mrna_matrix.tsv: events x cells, first column = event id, header = cell ids.
# PSI may contain NaN; mrna = estimated mRNA molecules captured per event per cell (from TPM, or UMI counts).
psix_obj = psix.Psix(psi_table='psi_matrix.tsv', mrna_table='mrna_matrix.tsv')
psix_obj.run_psix(latent=latent, n_jobs=4)               # defaults n_random_exons=2000, n_neighbors=100

regulated = psix_obj.psix_results.query('qvals < 0.05')   # columns: psix_score, pvals, qvals
