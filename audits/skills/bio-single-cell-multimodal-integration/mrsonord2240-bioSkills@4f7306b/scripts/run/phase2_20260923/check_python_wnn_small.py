"""Generate a second small valid 10x CITE-seq H5 and exercise the copied source example."""
from pathlib import Path
import h5py
import numpy as np
from scipy import sparse

rng = np.random.default_rng(20260923)
n_cells, n_genes, n_prot = 24, 320, 10
counts = rng.poisson(1.3, size=(n_genes + n_prot, n_cells)).astype(np.int32)
for cell in range(n_cells):
    label = cell % 3
    counts[label * 8:(label + 1) * 8, cell] += rng.poisson(15, 8)
    counts[n_genes + label * 3:n_genes + min(n_prot, (label + 1) * 3), cell] += rng.poisson(45, min(3, n_prot - label * 3))
matrix = sparse.csc_matrix(counts)
names = np.array([f"MT-{i}" if i < 4 else f"GENE{i}" for i in range(n_genes)] + [f"ADT{i}" for i in range(n_prot)], dtype="S")
types = np.array(["Gene Expression"] * n_genes + ["Antibody Capture"] * n_prot, dtype="S")
out = Path("filtered_feature_bc_matrix_small.h5")
with h5py.File(out, "w") as handle:
    group = handle.create_group("matrix")
    for name, value in (("data", matrix.data), ("indices", matrix.indices), ("indptr", matrix.indptr), ("shape", matrix.shape)):
        group.create_dataset(name, data=value)
    group.create_dataset("barcodes", data=np.array([f"SMALL-{i}-1" for i in range(n_cells)], dtype="S"))
    features = group.create_group("features")
    features.create_dataset("id", data=names)
    features.create_dataset("name", data=names)
    features.create_dataset("feature_type", data=types)
    features.create_dataset("genome", data=np.array(["GRCh38"] * (n_genes + n_prot), dtype="S"))
print(f"WROTE_SMALL_10X {out} {matrix.shape}; run copied source against this file by renaming it in its own directory")
