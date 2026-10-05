import pandas as pd, numpy as np
raw=pd.read_csv('cn/a375.count.txt',sep='\t'); cor=pd.read_csv('cn/screen_cleanr_corrected_counts.txt',sep='\t')
print(raw.columns.tolist(), cor.columns.tolist())
cols=list(raw.columns[2:]); 
def lfc(df):
    d=df.set_index('sgRNA'); x=d[cols]+0.5; x=x/x.sum()*1e6
    return np.log2(x.iloc[:,1:].mean(1)/x.iloc[:,0])
r=lfc(raw).groupby(raw.set_index('sgRNA').iloc[:,0]).mean(); 
rr=raw.set_index('sgRNA'); cc=cor.set_index('sgRNA')
lr=lfc(raw); lc=lfc(cor)
g=lambda s,df: s.groupby(df.set_index('sgRNA').iloc[:,0]).mean()
a=g(lr,raw); b=g(lc,cor)
for x in ['BRAF','MYC','RPS6','PSMA1']: print(x, round(a.get(x,np.nan),2), round(b.get(x,np.nan),2))
print('guide corr', lr.loc[lc.index].corr(lc))
print('integer frac', (cor[cols]%1==0).mean().mean())
