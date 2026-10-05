import pandas as pd, numpy as np, sys
def gini_all(x):
    x=np.sort(np.asarray(x,float)); n=len(x); c=np.cumsum(x)
    return (n+1-2*c.sum()/c[-1])/n
def gini_nz(x):
    x=np.asarray(x,float); return gini_all(x[x>0])
base='F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline/'
for name,path in [('HAP1 TKOv3','qc/hap1.count.txt'),('A375 KY (Project Score)','cn-correction/a375.count.txt'),('Project Score panel','jacks/panel.count.txt'),('simulated HAP1 qcpass','rra-qcpass/hap1.count.txt')]:
    t=pd.read_csv(base+path,sep='\t',index_col=0).drop(columns=lambda_cols if False else None) if False else pd.read_csv(base+path,sep='\t',index_col=0)
    t=t.iloc[:,1:]
    print(name,len(t),'guides')
    for c in t.columns[:6]:
        v=t[c].values
        print(f'  {c[:28]:28s} reads/guide {v.mean():8.1f} zeros {100*(v==0).mean():5.2f}% gini_all {gini_all(v):.3f} gini_nonzero {gini_nz(v):.3f} p90/p10 {np.percentile(v,90)/max(np.percentile(v,10),1):.2f}')
