"""Input 2 eval: does brie-quant LRT + per-cell Psi recover PLANTED truth? Also runs the example script's differential helper."""
import sys, numpy as np, pandas as pd, scanpy as sc
from scipy import stats
sys.path.insert(0,'/mnt/openscience/audits/bio-single-cell-splicing/run/skill/examples')
import sc_splicing_brie2 as ex
R='/mnt/openscience/audits/bio-single-cell-splicing/run'
a = sc.read_h5ad(f'{R}/out/planted_ss2/quant.h5ad')
truth = pd.read_csv(f'{R}/data/synth_ss2/truth.tsv', sep='\t', keep_default_na=False).set_index('gene')  # 'null' would be parsed as NaN otherwise
cells = pd.read_csv(f'{R}/data/synth_ss2/cells.tsv', sep='\t').set_index('cell')
print(a)
t = truth.loc[a.var_names]
t['dpsi_true'] = t.psiB - t.psiA
elbo = a.varm['ELBO_gain'][:,0]; fdr = a.varm['fdr'][:,0]; pv = a.varm['pval'][:,0]; coef = a.varm['cell_coeff'][:,0]
res = pd.DataFrame({'cls':t.cls,'dpsi_true':t.dpsi_true,'elbo':elbo,'fdr':fdr,'p':pv,'coef':coef}, index=a.var_names)
print(res.groupby('cls').agg(n=('elbo','size'), median_elbo=('elbo','median'), n_fdr05=('fdr', lambda x:(x<0.05).sum()), n_p05=('p', lambda x:(x<0.05).sum())))
big = res[res.cls=='big']; mid = res[res.cls=='mid']; nul=res[res.cls=='null']
print('events kept after brie-quant gene filter:', len(res), 'of 100 (big/mid/null =', len(big), len(mid), len(nul),')')
print('sign(coef)==sign(dpsi_true) big:', (np.sign(big.coef)==np.sign(big.dpsi_true)).mean(), ' mid:', (np.sign(mid.coef)==np.sign(mid.dpsi_true)).mean())
print('null events fdr<0.05:', int((nul.fdr<0.05).sum()), 'of', len(nul), ' raw p<0.05:', int((nul.p<0.05).sum()), '; ELBO_gain>3:', int((nul.elbo>3).sum()))
print('big/mid fdr<0.05:', int((big.fdr<0.05).sum()), '/', len(big), ',', int((mid.fdr<0.05).sum()), '/', len(mid), '; ELBO_gain>3:', int((big.elbo>3).sum()), int((mid.elbo>3).sum()))
# per-cell Psi accuracy vs group truth, split by dropout
psi = a.layers['Psi']
grp = cells.loc[a.obs_names,'group'].values; drop = cells.loc[a.obs_names,'dropout'].values.astype(bool)
tp = np.array([[truth.loc[g,'psiA'] if gr=='A' else truth.loc[g,'psiB'] for g in a.var_names] for gr in grp])
err_hi = np.abs(psi[~drop]-tp[~drop]).mean(); err_lo = np.abs(psi[drop]-tp[drop]).mean()
print(f'mean |Psi - true group PSI|: normal cells {err_hi:.3f}  dropout cells {err_lo:.3f}  (n dropout cells={drop.sum()})')
# naive raw PSI from counts for comparison
i1 = np.asarray(a.layers['isoform1'].todense() if hasattr(a.layers['isoform1'],'todense') else a.layers['isoform1']); i2 = np.asarray(a.layers['isoform2'].todense() if hasattr(a.layers['isoform2'],'todense') else a.layers['isoform2'])
print('dropout cells: mean unique reads/event', (i1+i2)[drop].mean().round(2), ' normal cells', (i1+i2)[~drop].mean().round(2))
# spread of dropout-cell Psi (shrinkage toward prior?)
print('sd of Psi across dropout cells (all events):', psi[drop].std().round(3), ' normal:', psi[~drop].std().round(3))
# The example helper: differential_splicing_pseudobulk
a.obs['cell_type']=grp
g1=(grp=='A'); g2=(grp=='B')
d = ex.differential_splicing_pseudobulk(a, g1, g2).set_index('event')
d['cls']=truth.loc[d.index,'cls']; d['dpsi_true']=(truth.loc[d.index,'psiA']-truth.loc[d.index,'psiB'])
print('example differential_splicing_pseudobulk: tested', len(d))
print(d.groupby('cls').agg(n=('fdr','size'), n_fdr05=('fdr', lambda x:(x<0.05).sum())))
sgn = (np.sign(d.delta_psi)==np.sign(d.dpsi_true))[d.cls!='null'].mean()
print('example helper: sign(delta_psi)==sign(true A-B) among planted:', round(sgn,3))
v, mp = ex.find_variable_splicing(a, 'cell_type', 40)
print('find_variable_splicing top10 planted?:', truth.loc[v.index[:10],'cls'].tolist())
# assertions
assert (big.fdr<0.05).mean()>=0.8, 'BRIE LRT misses >20% of large planted effects'
fdp = (nul.fdr<0.05).sum()/max(1,(res.fdr<0.05).sum()); print('observed FDP among fdr<0.05 calls:', round(fdp,3))
assert fdp <= 0.15, 'FDR not controlled (FDP>15% at nominal 5%)'
assert (np.sign(big.coef)==np.sign(big.dpsi_true)).mean()>=0.9
print('ASSERTIONS OK')
