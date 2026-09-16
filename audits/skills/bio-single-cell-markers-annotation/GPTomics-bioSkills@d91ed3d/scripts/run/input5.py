"""Input 5 (Stress) - bio-single-cell-markers-annotation
"Just run FindMarkers / rank_genes_groups treated-vs-control on my cells and give me the DE
list." The Skill says the tool will run it and return tidy tiny p-values, and that this is
statistically invalid. Measured three ways against the SYNTHETIC ground truth, including a
NULL contrast where every call is a false positive by construction.
"""
import scanpy as sc, numpy as np, pandas as pd
R = r'F:/OpenScience/audits/bio-single-cell-markers-annotation/run'
D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
a = sc.read_h5ad(R + '/input1_markers.h5ad')
truth = pd.read_csv(D + '/truth_de_genes.csv'); tr = set(truth.gene_symbol)
ss = pd.read_csv(D + '/sample_sheet.csv').set_index('sample')
a.obs['condition'] = ss.loc[a.obs['sample'], 'condition'].values
ct = a[a.obs['cell_type'] == 'CD14 Mono'].copy()
print(f'{ct.n_obs} CD14 Mono cells, {ct.obs["sample"].nunique()} donors; '
      f'ground truth: {len(tr)} genes changed in this cell type')


def run(obj, key, label, truthset=None):
    sc.tl.rank_genes_groups(obj, groupby=key, method='wilcoxon', pts=True, key_added='k')
    df = sc.get.rank_genes_groups_df(obj, group=obj.obs[key].cat.categories[-1], key='k')
    sig = set(df.names[(df.pvals_adj < 0.05) & (df.logfoldchanges.abs() > 0.5)])
    if truthset is None:
        print(f'  {label}: {len(sig)} genes at padj<0.05 & |logFC|>0.5 '
              f'(ALL FALSE by construction); smallest padj {df.pvals_adj.min():.2e}')
    else:
        tp = sig & truthset
        print(f'  {label}: {len(sig)} called | TP {len(tp)} | precision '
              f'{len(tp)/max(len(sig),1):.3f} | recall {len(tp)/len(truthset):.3f} | '
              f'smallest padj {df.pvals_adj.min():.2e}')
    return sig


print('\n(a) the request as asked: cell-level Wilcoxon, condition contrast')
ct.obs['condition'] = pd.Categorical(ct.obs['condition'], categories=['control', 'treated'])
run(ct, 'condition', 'cell-level Wilcoxon, REAL contrast', tr)

print('\n(b) the same test on a NULL contrast (donors split so condition, batch and sex are')
print('    each balanced 2+2, so no real difference exists)')
grpX = ['S1', 'S3', 'S5', 'S7']
ct.obs['fake'] = pd.Categorical(np.where(ct.obs['sample'].isin(grpX), 'X', 'Y'),
                                categories=['X', 'Y'])
print('   balance check:')
print(pd.crosstab(ss.loc[sorted(ct.obs['sample'].unique()), 'condition'],
                  [s in grpX for s in sorted(ct.obs['sample'].unique())]).to_string())
run(ct, 'fake', 'cell-level Wilcoxon, NULL contrast')

print('\n(c) the pseudobulk route the Skill prescribes, same NULL contrast')
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
pb = sc.get.aggregate(ct, by='sample', func='sum', layer='counts')
M = pd.DataFrame(np.asarray(pb.layers['sum']).astype(int),
                 index=list(pb.obs['sample']), columns=list(ct.var_names))
M = M.loc[:, M.sum(axis=0) >= 10]
for tag, col in [('NULL contrast', [('X' if s in grpX else 'Y') for s in M.index]),
                 ('REAL contrast', list(ss.loc[M.index, 'condition']))]:
    meta = pd.DataFrame({'g': col}, index=M.index)
    dds = DeseqDataSet(counts=M, metadata=meta, design='~g', quiet=True)
    dds.deseq2()
    lv = sorted(set(col))
    st = DeseqStats(dds, contrast=('g', lv[1], lv[0]), quiet=True)
    st.summary()
    r = st.results_df
    sig = set(r.index[r.padj < 0.05])
    tp = sig & tr
    if tag == 'NULL contrast':
        print(f'  pseudobulk, {tag}: {len(sig)} genes at padj<0.05 (ALL would be false); '
              f'smallest padj {r.padj.min():.3g}')
    else:
        print(f'  pseudobulk, {tag}: {len(sig)} called | TP {len(tp)} | precision '
              f'{len(tp)/max(len(sig),1):.3f} | recall {len(tp)/len(tr):.3f}')
print('DONE')
