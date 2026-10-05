# Smoke test for routes/chronos.md on a 5-cell-line slice of the Project Score panel (days assumed 14).
import pandas as pd, numpy as np, chronos
c = pd.read_csv('panel.count.txt', sep='\t'); rep = pd.read_csv('replicatemap.txt', sep='\t')
cols = [x for x in c.columns[2:]]
counts = c.set_index('sgRNA')[cols].T            # sequenced entities on rows, guides as columns
counts.index.name = 'sequence_ID'
smap = pd.DataFrame({'sequence_ID': cols})
smap['cell_line_name'] = np.where(smap.sequence_ID.str.contains('plasmid'), 'pDNA', smap.sequence_ID.str.split('_').str[0])
smap['days'] = np.where(smap.cell_line_name == 'pDNA', 0, 14); smap['pDNA_batch'] = 'b1'
gmap = c[['sgRNA', 'Gene']].rename(columns={'sgRNA': 'sgrna', 'Gene': 'gene'})
neg = pd.read_csv('F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/JACKS/jacks/example/NEGv1.txt', sep='	').Gene
negs = gmap[gmap.gene.isin(neg)].sgrna.tolist(); print('neg-control guides', len(negs))
model = chronos.Chronos(negative_control_sgrnas={'screen': negs}, sequence_map={'screen': smap}, guide_gene_map={'screen': gmap}, readcounts={'screen': counts})
model.train(nepochs=301)
ge = model.gene_effect
ge.to_csv('gene_effects.csv'); print(ge.shape)
rp = ge[[g for g in ge.columns if g.startswith(('RPL', 'RPS'))]].mean(1); print('ribosomal mean per line', rp.round(2).to_dict()); print('all-gene mean', ge.mean(1).round(2).to_dict())
