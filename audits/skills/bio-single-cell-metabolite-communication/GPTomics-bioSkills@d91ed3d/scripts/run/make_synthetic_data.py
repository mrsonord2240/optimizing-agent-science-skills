"""Build a synthetic scRNA-seq AnnData for auditing bio-single-cell-metabolite-communication.

Scenario: immunosuppressive tumor microenvironment.
  - Myeloid cells: high NT5E (CD73, produces adenosine) and high PTGES (produces PGE2)
  - Tumor cells:   high PTGES (produces PGE2), low NT5E
  - TCell cells:   high ADORA2A (adenosine sensor) and PTGER2/PTGER4 (PGE2 sensors)
Two conditions ('tumor', 'normal'): the signaling genes are strong in 'tumor' and
weak/absent in 'normal', so a differential-condition analysis should show the
CD73-adenosine-A2A and PTGES-PGE2-EP2/EP4 axes appearing only in the tumor condition.

All randomness is seeded (np.random.default_rng(0)) so the dataset is reproducible.
"""
import numpy as np
import pandas as pd
import scanpy as sc
import anndata as ad

rng = np.random.default_rng(0)

cell_types = ['Myeloid', 'Tumor', 'TCell']
n_per_type = 150
conditions = ['tumor', 'normal']

# Key signaling genes
signal_genes = ['NT5E', 'ADORA1', 'ADORA2A', 'ADORA2B', 'PTGES', 'PTGES2', 'PTGES3',
                 'PTGER1', 'PTGER2', 'PTGER4', 'ADA', 'PNP']
# additional real sensor/receptor genes (background expression only) so the MEBOCOST
# internal gene-overlap check (>=10 sensor genes must be present in the matrix) passes
filler_sensors = ['CASR', 'CNR1', 'FFAR2', 'GPBAR1', 'GPR35', 'GPR55', 'HCAR1',
                   'OXGR1', 'P2RX7', 'P2RY1', 'S1PR1', 'SUCNR1', 'TRPV1']
housekeeping = ['ACTB', 'GAPDH', 'B2M', 'RPL13A']
noise_genes = [f'NOISE{i}' for i in range(1, 31)]
genes = signal_genes + filler_sensors + housekeeping + noise_genes
n_genes = len(genes)

rows = []
obs_celltype = []
obs_condition = []

# baseline mean expression (counts) per gene, low background
base_mean = {g: 0.3 for g in genes}
for g in housekeeping:
    base_mean[g] = 15.0

# Elevated means per (cell_type, condition) -> gene -> mean
elevated = {
    ('Myeloid', 'tumor'): {'NT5E': 25.0, 'PTGES': 12.0, 'ADA': 4.0},
    ('Myeloid', 'normal'): {'NT5E': 1.0, 'PTGES': 1.0, 'ADA': 3.5},
    ('Tumor', 'tumor'): {'PTGES': 20.0, 'PTGES2': 6.0},
    ('Tumor', 'normal'): {'PTGES': 1.0, 'PTGES2': 1.0},
    ('TCell', 'tumor'): {'ADORA2A': 18.0, 'PTGER2': 14.0, 'PTGER4': 10.0},
    ('TCell', 'normal'): {'ADORA2A': 1.5, 'PTGER2': 1.0, 'PTGER4': 1.0},
}

for ct in cell_types:
    for cond in conditions:
        n = n_per_type
        for _ in range(n):
            means = np.array([elevated.get((ct, cond), {}).get(g, base_mean[g]) for g in genes])
            counts = rng.poisson(means)
            rows.append(counts)
            obs_celltype.append(ct)
            obs_condition.append(cond)

X = np.vstack(rows).astype(np.float32)
obs = pd.DataFrame({'cell_type': obs_celltype, 'condition': obs_condition})
obs.index = [f'cell_{i}' for i in range(X.shape[0])]
var = pd.DataFrame(index=genes)

adata = ad.AnnData(X=X, obs=obs, var=var)
adata.layers['counts'] = adata.X.copy()

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)

adata.write_h5ad('adata_annotated.h5ad')
print('Wrote adata_annotated.h5ad:', adata.shape)
print(adata.obs.groupby(['cell_type', 'condition']).size())

# --- Edge-case variant: mouse-style lowercase symbols but requesting species='human' ---
mouse_like_genes = [g.capitalize() if g not in noise_genes and g not in housekeeping else g for g in genes]
adata_mouse_labeled = adata.copy()
adata_mouse_labeled.var_names = mouse_like_genes
adata_mouse_labeled.write_h5ad('adata_mouse_labeled.h5ad')
print('Wrote adata_mouse_labeled.h5ad (edge case: mouse-style symbols, will be run with species=human)')
