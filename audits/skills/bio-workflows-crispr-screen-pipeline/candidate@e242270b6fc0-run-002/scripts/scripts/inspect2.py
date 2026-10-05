import pandas as pd
m=pd.read_csv('mle/timecourse_mle.gene_summary.txt',sep='\t')
print(m.sort_values('KBM7|beta').head(6)[['Gene','KBM7|beta','KBM7|fdr','KBM7|wald-fdr']].to_string())
print('KBM7 fdr<0.05',(m['KBM7|fdr']<0.05).sum(),'beta<-0.5',(m['KBM7|beta']<-0.5).sum())
j=pd.read_csv('jacks/jacks_out_gene_JACKS_results.txt',sep='\t',index_col=0); print(j.shape, j.columns.tolist()[:6])
mean=j[[c for c in j.columns if not c.endswith('_std')]]
rp=mean.loc[[g for g in mean.index if g.startswith(('RPL','RPS'))]]; print('ribo mean',rp.mean().round(2).to_dict(),'all',mean.mean().round(2).to_dict())
c=pd.read_csv('chronos/gene_effects.csv',index_col=0); print(c.shape, c.loc[:,['RPL11','PSMA1','MYC']].round(2).to_string() if 'MYC' in c else '')
raw=pd.read_csv('cn/a375.count.txt',sep='\t'); cor=pd.read_csv('cn/screen_cleanr_corrected_counts.txt',sep='\t'); print(raw.shape,cor.shape, raw.columns[:3].tolist(), cor.columns[:3].tolist())
