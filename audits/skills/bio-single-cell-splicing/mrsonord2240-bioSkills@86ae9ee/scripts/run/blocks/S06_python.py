import scanpy as sc
import pandas as pd

a = sc.read_h5ad('brie_quant.h5ad')    # only events that passed the gene filter
# a.varm['ELBO_gain' | 'pval' | 'fdr' | 'cell_coeff'] are events x tested features, in cell_metadata.tsv column order (a.uns['Xc_ids'])
lrt = pd.DataFrame({'ELBO_gain': a.varm['ELBO_gain'][:, 0], 'pval': a.varm['pval'][:, 0],
                    'fdr': a.varm['fdr'][:, 0], 'cell_coeff': a.varm['cell_coeff'][:, 0]}, index=a.var_names)
hits = lrt[lrt.fdr < 0.05].sort_values('fdr')     # the sign of cell_coeff gives the direction
psi = a.layers['Psi']                              # cells x events, shrunken per-cell PSI; layers 'Psi_95CI' (interval width) and 'Z_std' (SD on the logit scale) give its uncertainty
