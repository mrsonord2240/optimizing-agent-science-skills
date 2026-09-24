import os
from scquint.data import load_adata_from_starsolo, add_gene_annotation

os.chdir('/mnt/openscience/audits/bio-single-cell-splicing/run/out/in6_scquint')
adata = load_adata_from_starsolo('Solo.out/SJ/raw')
adata = add_gene_annotation(adata, 'annotation.gtf.gz')
try:
    if adata.n_vars == 0 or not adata.var['gene_id'].notna().any():
        raise ValueError('scQuint annotated zero introns: junctions must use chr-prefixed contigs and the GTF must use unprefixed contigs')
except ValueError as exc:
    assert 'chr-prefixed' in str(exc)
    print(f'PASS scQuint incompatible-contig guard vars={adata.n_vars}')
else:
    raise AssertionError('incompatible contigs unexpectedly passed')
