import h5py,pandas as pd
D=r'F:\OpenScience\audit-envs\atac-seq\public-data\scatac\outs'
f=h5py.File(D+r'\filtered_peak_bc_matrix.h5');g=f['matrix'];bc=[b.decode() for b in g['barcodes'][:]]
nz=pd.Series(0,index=bc);import numpy as np
# cells with >=200 peak features (CreateChromatinAssay min.features=200)
ip=g['indptr'][:];cnt=np.diff(ip);nfeat=pd.Series(cnt,index=bc)
d=pd.read_csv(D+r'\singlecell.csv',index_col=0).loc[bc]
r=d.blacklist_region_fragments/d.peak_region_fragments
k=nfeat>=200
print('matrix cells',len(bc),'with>=200 features',int(k.sum()),'max ratio (all matrix cells)',round(r.max(),4),'max among >=200 features',round(r[k].max(),4),'n>=0.05',int((r[k]>=0.05).sum()))
