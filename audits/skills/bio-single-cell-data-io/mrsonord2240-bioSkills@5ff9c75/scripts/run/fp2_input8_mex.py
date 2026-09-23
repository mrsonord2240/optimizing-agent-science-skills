"""Phase-2 Input 8: synthetic 10x MEX, testing IDs, non-GEX retention and unique symbols."""
from pathlib import Path
import gzip
import numpy as np
from scipy.io import mmwrite
from scipy import sparse
import scanpy as sc
root = Path('F:/OpenScience/audits/bio-single-cell-data-io/data/fp2_mex')
root.mkdir(parents=True, exist_ok=True)
mmwrite(root / 'matrix.mtx', sparse.coo_matrix(np.array([[1,0,3],[0,2,1],[4,0,0],[0,5,2]], dtype=np.int32)))
with (root / 'matrix.mtx').open('rb') as source, gzip.open(root / 'matrix.mtx.gz', 'wb') as dest:
    dest.write(source.read())
with gzip.open(root / 'features.tsv.gz', 'wt') as f:
    f.write('ENSG1\tDUP\tGene Expression\nENSG2\tDUP\tGene Expression\nADT1\tCD3\tAntibody Capture\nGUIDE1\tG1\tCRISPR Guide Capture\n')
with gzip.open(root / 'barcodes.tsv.gz', 'wt') as f:
    f.write('cell1\ncell2\ncell3\n')
adata = sc.read_10x_mtx(root, var_names='gene_ids', gex_only=False)
print('shape', adata.shape, 'names', adata.var_names.tolist(), 'types', sorted(adata.var.feature_types.unique().tolist()))
assert adata.shape == (3,4)
assert adata.var_names.tolist() == ['ENSG1','ENSG2','ADT1','GUIDE1']
assert set(adata.var.feature_types) == {'Gene Expression','Antibody Capture','CRISPR Guide Capture'}
print('PASS input8')
