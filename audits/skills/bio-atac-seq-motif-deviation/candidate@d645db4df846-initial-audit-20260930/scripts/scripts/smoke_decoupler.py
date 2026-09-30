# Skill references/single-cell.md DecoupleR snippet (decoupler 1.x) on chromVAR z-scores from the bulk ENCODE run
import os, pandas as pd, numpy as np, anndata as ad, decoupler as dc
md=os.environ['MD']; r=md+'/work/run_bulk_patched/'
print('decoupler', dc.__version__)
z=pd.read_csv(r+'chromvar_deviations.csv',index_col=0); v=pd.read_csv(r+'chromvar_variability.csv',index_col=0)
z.index=v.loc[z.index,'name']; z=z[~z.index.duplicated()]
adata=ad.AnnData(X=z.T.values.astype('float32'),obs=pd.DataFrame(index=z.columns),var=pd.DataFrame(index=z.index))
adata.obsm['chromvar']=pd.DataFrame(z.T.values,index=z.columns,columns=z.index)
net=dc.get_collectri(organism='human', split_complexes=False)
print('collectri', net.shape, net.columns.tolist())
mat=adata.obsm['chromvar']
try:
    a=dc.run_ulm(mat=mat, net=net, source='source', target='target'); print('ulm ok', type(a))
except Exception as e: print('ulm ERR', repr(e)[:300])
for nm,fn in [('ulm',dc.run_ulm),('mlm',dc.run_mlm)]:
    try:
        est,p=fn(mat=mat, net=net, source='source', target='target', verbose=False)
        print(nm, est.shape); print(est.T.assign(d=est.T.iloc[:,3:].mean(1)-est.T.iloc[:,:3].mean(1)).sort_values('d').iloc[[0,1,2,-3,-2,-1]][['d']])
    except Exception as e: print(nm,'ERR',repr(e)[:300])
try:
    r_=dc.run_consensus(mat=mat, net=net); print('consensus', [x.shape for x in r_])
except Exception as e: print('consensus ERR',repr(e)[:300])
