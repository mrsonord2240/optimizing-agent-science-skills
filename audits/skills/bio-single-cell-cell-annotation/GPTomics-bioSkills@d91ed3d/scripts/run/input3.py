"""Input 3 (Edge) - bio-single-cell-cell-annotation
The Skill's Common Errors row 3: "CellTypist returns confident but nonsensical labels /
Gene-ID space mismatch (query var_names are Ensembl IDs vs symbol-based model); few genes
matched / Set var_names to gene symbols; check the matched-gene fraction reported by annotate
before trusting labels."

The synthetic Cell Ranger matrices carry Ensembl IDs in features.tsv column 1, so this is the
real thing, not a contrivance. Question: does anything actually warn, and is the "matched-gene
fraction reported by annotate" a thing you can read?
"""
import os
os.environ.setdefault('CELLTYPIST_FOLDER',
                      r'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/cache/celltypist')
import scanpy as sc
import celltypist
import numpy as np
import pandas as pd
import warnings

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['true_cell_type'] = tc['true_cell_type'].values
a = a[(~tc['true_doublet'].astype(bool) & ~tc['true_low_quality'].astype(bool)).values].copy()
a = a[:2000].copy()
print(f'{a.n_obs} cells; symbols: {list(a.var_names[:3])}; '
      f'Ensembl IDs in var: {list(a.var["gene_ids"][:3])}')

LIN = {'CD4 T cells': 'T', 'CD8 T cells': 'T', 'NK cells': 'NK', 'B cells': 'B',
       'CD14+ Monocytes': 'Mono', 'FCGR3A+ Monocytes': 'Mono', 'Dendritic cells': 'DC',
       'Megakaryocytes': 'Mk'}


def lineage(lbl):
    s = str(lbl).lower()
    if 'megakaryo' in s or 'platelet' in s: return 'Mk'
    if 'ilc' in s or ('nk' in s and 'cell' in s): return 'NK'
    if 'dendritic' in s or s.startswith('dc') or 'pdc' in s: return 'DC'
    if 'monocyt' in s or 'macrophage' in s: return 'Mono'
    if 'b cell' in s or 'plasma' in s or 'germinal' in s: return 'B'
    if ('t cell' in s or 'tcm' in s or 'tem' in s or 'treg' in s or 'mait' in s
            or 'helper' in s or 'cytotoxic' in s): return 'T'
    return 'other'


true_lin = a.obs['true_cell_type'].map(LIN).values

for name, use_ensembl in [('gene SYMBOLS (correct)', False), ('Ensembl IDs (the trap)', True)]:
    c = a.copy()
    if use_ensembl:
        c.var_names = c.var['gene_ids'].astype(str).values
        c.var_names_make_unique()
    sc.pp.normalize_total(c, target_sum=1e4); sc.pp.log1p(c)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        try:
            p = celltypist.annotate(c, model='Immune_All_Low.pkl', majority_voting=False)
        except Exception as e:
            model = celltypist.models.Model.load('Immune_All_Low.pkl')
            matched = len(set(model.classifier.features) & set(c.var_names))
            print(f'\n{name}:')
            print(f'  HARD ERROR RAISED: {type(e).__name__}: {e}')
            print(f'  genes in the model that matched the query: {matched}/'
                  f'{len(model.classifier.features)}')
            continue
        warns = [f'{x.category.__name__}: {str(x.message)[:130]}' for x in w]
    pl = np.array([lineage(x) for x in p.predicted_labels['predicted_labels']])
    acc = float((pl == true_lin).mean())
    conf = float(p.probability_matrix.max(axis=1).mean())
    print(f'\n{name}:')
    print(f'  lineage accuracy {acc:.3f} | mean max-probability {conf:.3f} | '
          f'distinct labels {p.predicted_labels["predicted_labels"].nunique()}')
    print(f'  top labels: {p.predicted_labels["predicted_labels"].value_counts().head(4).to_dict()}')
    print(f'  Python warnings raised: {warns if warns else "none"}')
    # is a matched-gene fraction retrievable, as Common Errors row 3 claims?
    model = celltypist.models.Model.load('Immune_All_Low.pkl')
    mfeat = set(model.classifier.features)
    matched = len(mfeat & set(c.var_names))
    print(f'  genes in the model that matched the query: {matched}/{len(mfeat)} '
          f'({100*matched/len(mfeat):.1f}%)')
    print(f'  is that fraction reported by annotate()? '
          f'{[k for k in vars(p) if "gene" in k.lower() or "match" in k.lower()] or "no such attribute"}')
print('DONE')
