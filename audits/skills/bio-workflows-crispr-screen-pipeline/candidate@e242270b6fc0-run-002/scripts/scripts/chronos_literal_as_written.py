import chronos, pandas as pd
c = pd.read_csv('panel.count.txt', sep='\t')
cols=list(c.columns[2:])
counts=c.set_index('sgRNA')[cols].T; counts.index.name='sequence_ID'
sequence_map=pd.DataFrame({'sequence_ID':cols,'cell_line':[x.split('_')[0] for x in cols],'days':14})
guide_gene_map=c[['sgRNA','Gene']].rename(columns={'sgRNA':'sgrna','Gene':'gene'})
counts_df=counts
model = chronos.Chronos(sequence_map={'screen': sequence_map},
                        guide_gene_map={'screen': guide_gene_map},
                        readcounts={'screen': counts_df})
model.train(nepochs=301)
gene_effects = model.gene_effect
