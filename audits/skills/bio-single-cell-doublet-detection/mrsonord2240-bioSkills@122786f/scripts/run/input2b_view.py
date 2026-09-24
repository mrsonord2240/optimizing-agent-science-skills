"""Follow-up to input 2: SKILL.md:105 says to loop
`sc.pp.scrublet(adata[adata.obs.sample == s], ...)` per sample. That indexes a VIEW.
Does the result reach the parent object?"""
import scanpy as sc, pandas as pd, warnings
D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
a = a[a.obs['sample'].isin(['S1', 'S2'])].copy()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    for s in ['S1', 'S2']:
        sc.pp.scrublet(a[a.obs['sample'] == s], expected_doublet_rate=0.006, random_state=0)
    print('warnings raised:', [f'{x.category.__name__}: {str(x.message)[:90]}' for x in w][:4])
print("'doublet_score' in parent .obs after the verbatim loop:", 'doublet_score' in a.obs.columns)
print("'predicted_doublet' in parent .obs:", 'predicted_doublet' in a.obs.columns)
