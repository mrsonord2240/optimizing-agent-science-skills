"""Write a small, deterministic 10x-v3 CITE-seq H5 fixture for the shipped muon example."""
from pathlib import Path
import h5py
import numpy as np
from scipy import sparse

rng = np.random.default_rng(923)
n_cells, n_genes, n_prot = 90, 400, 12
counts = rng.poisson(1.2, size=(n_genes + n_prot, n_cells)).astype(np.int32)
labels = np.repeat(np.arange(3), n_cells // 3)
for cell, label in enumerate(labels):
    counts[label * 10:(label + 1) * 10, cell] += rng.poisson(12, 10)
    counts[n_genes + label * 3:n_genes + (label + 1) * 3, cell] += rng.poisson(50, 3)
matrix = sparse.csc_matrix(counts)
gene_names = [f'MT-{i}' if i < 5 else f'GENE{i}' for i in range(n_genes)]
prot_names = ['CD3', 'CD4', 'CD8', 'CD14', 'CD19', 'CD16', 'CD56', 'CD27', 'PD1', 'CTLA4', 'IgG1', 'IgG2b']
names = np.array(gene_names + prot_names, dtype='S')
types = np.array(['Gene Expression'] * n_genes + ['Antibody Capture'] * n_prot, dtype='S')
out = Path('filtered_feature_bc_matrix.h5')
with h5py.File(out, 'w') as handle:
    group = handle.create_group('matrix')
    group.create_dataset('data', data=matrix.data)
    group.create_dataset('indices', data=matrix.indices)
    group.create_dataset('indptr', data=matrix.indptr)
    group.create_dataset('shape', data=matrix.shape)
    group.create_dataset('barcodes', data=np.array([f'CELL-{i}-1' for i in range(n_cells)], dtype='S'))
    features = group.create_group('features')
    features.create_dataset('id', data=names)
    features.create_dataset('name', data=names)
    features.create_dataset('feature_type', data=types)
    features.create_dataset('genome', data=np.array(['GRCh38'] * (n_genes + n_prot), dtype='S'))
print(f'WROTE_10X_H5 {out} {matrix.shape}')
