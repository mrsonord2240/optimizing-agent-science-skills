import numpy as np,pandas as pd
rng=np.random.default_rng(2026092304); n=1000; tags=['HTO_A','HTO_B','HTO_C','HTO_D']; classes=np.array(['negative']*80+['singlet']*840+['doublet']*80); rng.shuffle(classes)
x=rng.poisson(4,(n,4)).astype(float); truth=[]
for i,c in enumerate(classes):
    if c=='singlet': j=int(rng.integers(4)); x[i,j]+=rng.poisson(220); truth.append(j+1)
    elif c=='doublet': js=rng.choice(4,2,replace=False); x[i,js]+=rng.poisson(170,2); truth.append(5+sum(2**j for j in js))
    else: truth.append(0)
pd.DataFrame(x,columns=tags,index=[f'c{i}' for i in range(n)]).rename_axis('barcode').reset_index().to_csv('gmm_input.csv',index=False)
pd.DataFrame({'truth_cluster':truth}).to_csv('gmm_truth.csv',index=False)
