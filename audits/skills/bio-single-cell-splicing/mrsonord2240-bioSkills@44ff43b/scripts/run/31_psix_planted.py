"""Input 6a: Psix on SYNTHETIC trajectory data with known dynamic exons; first the SKILL's snippet (literal), then the real API. Run in as-sc."""
import numpy as np, pandas as pd, scanpy as sc, anndata as ad, psix, traceback, os
R='/mnt/openscience/audits/bio-single-cell-splicing/run'; O=f'{R}/data/psix_planted'; os.makedirs(O, exist_ok=True)
rng=np.random.default_rng(3)
NC, NE = 300, 150
t = np.sort(rng.uniform(0,1,NC)); cells=[f'c{i:03d}' for i in range(NC)]
lat = pd.DataFrame({'d1':t+rng.normal(0,0.03,NC),'d2':rng.normal(0,0.05,NC)}, index=cells)
dyn = np.zeros(NE,bool); dyn[:30]=True
psi_true = np.zeros((NC,NE)); 
for e in range(NE):
    if dyn[e]:
        c=rng.uniform(0.3,0.7); k=rng.uniform(8,14); s=rng.choice([-1,1]); psi_true[:,e]=1/(1+np.exp(-s*k*(t-c)))
    else:
        psi_true[:,e]=rng.uniform(0.15,0.85)
mrna = rng.negative_binomial(1.5, 1.5/(1.5+8), size=(NC,NE))   # ~8 reads/event/cell, many zeros (sparse)
psi = np.where(mrna>0, rng.binomial(mrna, psi_true)/np.maximum(mrna,1), np.nan)
ev=[f'ev{e:03d}' for e in range(NE)]
pd.DataFrame(psi.T,index=ev,columns=cells).to_csv(f'{O}/psi.tsv',sep='\t')
pd.DataFrame(mrna.T.astype(float),index=ev,columns=cells).to_csv(f'{O}/mrna.tsv',sep='\t')
lat.to_csv(f'{O}/latent.tsv',sep='\t')
print('NaN fraction in PSI', np.isnan(psi).mean().round(3))
# --- (1) the Skill's snippet, literal
try:
    adata = ad.AnnData(np.zeros((NC,5)), obs=pd.DataFrame(index=cells)); adata.obsm['X_pca']=lat.values
    sc.pp.neighbors(adata, n_neighbors=30, use_rep='X_pca')
    psix_obj = psix.Psix(adata, psi_matrix_path=f'{O}/psi.tsv')
    print('Skill constructor: OK?!')
except Exception as e:
    print('SKILL literal psix.Psix(adata, psi_matrix_path=...) FAILED:', type(e).__name__, e)
# --- (2) real API
p = psix.Psix(psi_table=f'{O}/psi.tsv', mrna_table=f'{O}/mrna.tsv')
p.run_psix(latent=f'{O}/latent.tsv', n_jobs=4, n_random_exons=300, pvals_bins=3, n_neighbors=30)
r = p.psix_results
print(r.head(3)); print('columns', list(r.columns))
try:
    reg = r.query('psix_score > 1.5 and pvalue < 0.05'); print('Skill query OK', len(reg))
except Exception as e:
    print('SKILL literal .query("psix_score > 1.5 and pvalue < 0.05") FAILED:', type(e).__name__, str(e)[:120])
isdyn = pd.Series(dyn, index=ev).loc[r.index]
call = r.qvals<0.05
print('Psix q<0.05: dynamic', int((call&isdyn).sum()), '/30; static false pos', int((call&~isdyn).sum()), '/120')
call2 = (r.psix_score>1.5)&(r.pvals<0.05)
print('with (psix_score>1.5 & pvals<0.05): dynamic', int((call2&isdyn).sum()), '/30; static FP', int((call2&~isdyn).sum()), '/120')
print('psix_score dynamic median %.2f static median %.2f'%(r.psix_score[isdyn].median(), r.psix_score[~isdyn].median()))
assert (call&isdyn).sum()>=20 and (call&~isdyn).sum()<=6
print('ASSERT OK: Psix (real API) recovers planted trajectory-regulated exons')
