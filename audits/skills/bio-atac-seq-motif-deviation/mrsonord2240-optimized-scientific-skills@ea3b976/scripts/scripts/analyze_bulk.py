import pandas as pd, numpy as np
R='F:/OpenScience/audits/bio-atac-seq-motif-deviation/reaudit-run/'
a=pd.read_csv(R+'bulk_A/chromvar_deviations.csv',index_col=0); u=pd.read_csv(R+'bulk_U/chromvar_deviations.csv',index_col=0)
print('shape',a.shape,'NA',int(a.isna().sum().sum()),'cols',list(a.columns))
print('A vs unseeded max|dz| %.3f'%np.abs(a.values-u.reindex(a.index).values).max())
d=pd.read_csv(R+'bulk_A/chromvar_differential.csv',index_col=0); du=pd.read_csv(R+'bulk_U/chromvar_differential.csv',index_col=0)
f=lambda x:set(x.index[(x['adj.P.Val']<.05)&(x.logFC.abs()>=.5)])
sa,su=f(d),f(du); print('sig A',len(sa),'sig U',len(su),'jaccard %.3f'%(len(sa&su)/len(sa|su)))
print('cols',list(d.columns)); print('has FDR col','FDR' in d.columns)
for k in ['GATA2','GATA1::TAL1','GATA1','Spi1','EBF1','SPIB','IRF4','TAL1','RUNX1','PAX5']:
    r=d[d.index.str.contains(r'\('+k.replace('::','::')+r'\)$',regex=True)]
    print(k,[(i,round(x,2)) for i,x in r.logFC.items()][:4])
v=pd.read_csv(R+'bulk_A/chromvar_variability.csv',index_col=0); print(v.head(5)); print('var cols',list(v.columns),'n',len(v))
print('K562 mean z GATA2 vs GM', a[a.index.str.contains(r'\(GATA2\)')].round(2).to_string())
