import os
import numpy as np
from scquint.data import load_adata_from_starsolo, add_gene_annotation, group_introns
from scquint.differential_splicing import run_differential_splicing

root = '/mnt/openscience/audits/bio-single-cell-splicing/run/out/in6_planted_big'
os.chdir(root)
adata = load_adata_from_starsolo('Solo.out/SJ/raw')
adata = add_gene_annotation(adata, 'annotation.gtf.gz')
if adata.n_vars == 0 or not adata.var['gene_id'].notna().any():
    raise ValueError('scQuint annotated zero introns: junctions must use chr-prefixed contigs and the GTF must use unprefixed contigs')
adata = group_introns(adata, by='three_prime')
# Bounded final-pass fixture: preserve four complete intron groups so the exact
# documented call completes within the interactive execution window.
groups = adata.var['intron_group'].drop_duplicates().iloc[:4]
adata = adata[:, adata.var['intron_group'].isin(groups)].copy()
adata.obs['cell_type'] = ['neuron'] * 20 + ['glia'] * 20
a = np.where(adata.obs.cell_type == 'neuron')[0]
b = np.where(adata.obs.cell_type == 'glia')[0]
intron_groups, introns = run_differential_splicing(adata, a, b,
    min_cells_per_intron_group=10, min_total_cells_per_intron=10)
assert len(intron_groups) > 0 and len(introns) > 0
print(f'PASS scQuint vars={adata.n_vars} groups={len(intron_groups)} introns={len(introns)}')
