import numpy as np, pandas as pd, anndata as ad
import scanpy.external as sce
rng=np.random.default_rng(2026092302); n=700; tags=['HTO_A','HTO_B']
truth=rng.choice(['singlet','doublet','negative'],n,p=[.84,.10,.06]); counts=rng.poisson(6,(n,2)); ids=[]
for i,c in enumerate(truth):
    if c=='singlet':
        j=int(rng.integers(2)); counts[i,j]+=rng.poisson(220); ids.append(tags[j])
    elif c=='doublet': counts[i]+=rng.poisson(170,2); ids.append('Doublet')
    else: ids.append('Negative')
obs=pd.DataFrame(counts,columns=tags,index=[f'c{i}' for i in range(n)])
def run():
    a=ad.AnnData(X=rng.poisson(1,(n,20)),obs=obs.copy())
    sce.pp.hashsolo(a,cell_hashing_columns=tags,priors=(.01,.8,.19),number_of_noise_barcodes=1)
    return a.obs['Classification'].copy()
x,y=run(),run(); pred=x.map(lambda z:'negative' if z=='Negative' else ('doublet' if z=='Doublet' else 'singlet')).to_numpy()
both=(pred=='singlet')&(truth=='singlet')
print(x.value_counts().to_string()); print(f'CLASS_ACCURACY={np.mean(pred==truth):.3f}')
print(f'SINGLET_ID_ACCURACY={np.mean(x[both].to_numpy()==np.asarray(ids)[both]):.3f}')
print(f'NEGATIVE_FRACTION={(x=="Negative").mean():.3f}'); print(f'DETERMINISTIC={x.equals(y)}')
