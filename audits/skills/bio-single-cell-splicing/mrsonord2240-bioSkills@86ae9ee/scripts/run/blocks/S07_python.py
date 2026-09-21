import numpy as np
from scquint.data import load_adata_from_starsolo, add_gene_annotation, group_introns
from scquint.differential_splicing import run_differential_splicing

adata = load_adata_from_starsolo('Solo.out/SJ/raw')        # dir with matrix.mtx, barcodes.tsv, features.tsv (SJ.out.tab columns)
adata = add_gene_annotation(adata, 'annotation.gtf.gz')     # Ensembl-style contigs (1, 2, X): scQuint prepends 'chr' to match the junctions
adata = group_introns(adata, by='three_prime')
adata.obs['cell_type'] = cell_types                         # obs holds only the barcodes: add your labels, one per cell
cell_idx_a = np.where(adata.obs.cell_type == 'neuron')[0]
cell_idx_b = np.where(adata.obs.cell_type == 'glia')[0]

intron_groups, introns = run_differential_splicing(adata, cell_idx_a, cell_idx_b,
                                                   min_cells_per_intron_group=10, min_total_cells_per_intron=10)
hits = intron_groups[intron_groups.p_value_adj < 0.05]      # introns: psi_a, psi_b, delta_psi per intron
