"""Input 4 (Variant B) - bio-single-cell-markers-annotation
The pseudobulk aggregation snippet, SKILL.md:150-156. The Skill's own rule (Defaults that bite,
last row) is "Aggregate RAW counts (summed), never normalized". Its Python snippet calls
sc.get.aggregate(cell_type, by='sample', func='sum') with no layer= argument. Does that sum raw
counts, or whatever happens to be in .X?
"""
import scanpy as sc, numpy as np, pandas as pd, inspect
R = r'F:/OpenScience/audits/bio-single-cell-markers-annotation/run'
D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
a = sc.read_h5ad(R + '/input1_markers.h5ad')
print('object state after the Skill\'s own upstream steps: X is log-normalized,',
      'layers =', sorted(k for k in a.layers if k))
print('sc.get.aggregate signature:', inspect.signature(sc.get.aggregate))

ct = a[a.obs['cell_type'] == 'CD14 Mono'].copy()
print(f'\n{ct.n_obs} CD14 Mono cells across {ct.obs["sample"].nunique()} samples')

# --- SKILL.md:153-156 verbatim ---
pseudobulk = sc.get.aggregate(ct, by='sample', func='sum')
counts_df = pseudobulk.layers['sum']
X = np.asarray(counts_df)
print('\nSKILL.md snippet, verbatim:')
print(f'  shape {X.shape}; dtype {X.dtype}; all values integral? {bool(np.all(X == np.round(X)))}')
print(f'  min {X.min():.4f} max {X.max():.4f}; row sums {np.round(X.sum(1)).tolist()[:4]} ...')

# --- what it should have been ---
pb_counts = sc.get.aggregate(ct, by='sample', func='sum', layer='counts')
Y = np.asarray(pb_counts.layers['sum'])
print('\nwith layer="counts" (what the Skill\'s own rule requires):')
print(f'  shape {Y.shape}; all values integral? {bool(np.all(Y == np.round(Y)))}')
print(f'  min {Y.min():.1f} max {Y.max():.1f}; row sums {Y.sum(1).astype(int).tolist()[:4]} ...')
print(f'  correlation between the two matrices (flattened): '
      f'{np.corrcoef(X.ravel(), Y.ravel())[0,1]:.4f}')

# --- does the difference change the DE answer? ---
try:
    from pydeseq2.dds import DeseqDataSet
    from pydeseq2.ds import DeseqStats
    ss = pd.read_csv(D + '/sample_sheet.csv').set_index('sample')
    truth = pd.read_csv(D + '/truth_de_genes.csv'); tr = set(truth.gene_symbol)
    meta = pd.DataFrame({'condition': ss.loc[list(pseudobulk.obs['sample']), 'condition'].values},
                        index=list(pseudobulk.obs['sample']))
    out = {}
    for tag, M in [('log-normalized sums (the snippet as written)', X),
                   ('raw count sums (layer="counts")', Y)]:
        cdf = pd.DataFrame(np.round(M).astype(int), index=meta.index, columns=list(ct.var_names))
        cdf = cdf.loc[:, cdf.sum(0) >= 10]
        dds = DeseqDataSet(counts=cdf, metadata=meta, design='~condition', quiet=True)
        dds.deseq2()
        st = DeseqStats(dds, contrast=('condition', 'treated', 'control'), quiet=True)
        st.summary()
        r = st.results_df
        sig = set(r.index[(r.padj < 0.05)])
        tp = sig & tr
        out[tag] = (len(sig), len(tp))
        print(f'\n  pyDESeq2 on {tag}:')
        print(f'    {len(sig)} genes padj<0.05 | TP {len(tp)} | precision '
              f'{len(tp)/max(len(sig),1):.3f} | recall {len(tp)/len(tr):.3f}')
except Exception as e:
    print('\npyDESeq2 comparison FAILED:', type(e).__name__, str(e)[:200])
print('DONE')
