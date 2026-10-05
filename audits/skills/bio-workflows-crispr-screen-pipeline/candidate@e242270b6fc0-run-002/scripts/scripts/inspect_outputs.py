import pandas as pd, numpy as np, os, glob
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/../work')
g=pd.read_csv('rra/essentiality_rra.gene_summary.txt',sep='\t'); print('rra genes',len(g)); 
neg=pd.read_csv('rra/essentiality_rra_negative_hits.csv'); pos=pd.read_csv('rra/essentiality_rra_positive_hits.csv'); print('neg',len(neg),'pos',len(pos), list(neg.columns)[:6])
print(g[g['id'].isin(['RPL11','RPS6','POLR2L','PSMA1','AAVS1'])][['id','neg|lfc','neg|fdr','pos|fdr']])
b=pd.read_csv('bagel2/bayes_factor.txt',sep='\t'); print('bagel',len(b),(b.BF>6).sum(), b.sort_values('BF',ascending=False).head(3).GENE.tolist())
cef=set(pd.read_csv('F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline/bagel2/CEGv2.txt',sep='\t').iloc[:,0])
print('CEG mean BF',b[b.GENE.isin(cef)].BF.mean(), 'frac CEG BF>6', (b[b.GENE.isin(cef)].BF>6).mean())
pr=pd.read_csv('bagel2/pr_curve.txt',sep='\t'); print(pr.columns.tolist(), len(pr)); 
d=pd.read_csv('drugz/drugz_output.txt',sep='\t'); print('drugz',d.shape,d.isna().sum().sum(), d.columns.tolist())
m=pd.read_csv('mle/timecourse_mle.gene_summary.txt',sep='\t'); print('mle',m.shape,m.columns.tolist()); print(m[m.Gene.isin(['RPL11','RPS6','PSMA1','POLR2A'])].iloc[:, :8] if 'Gene' in m else '')
c=pd.read_csv('cn/screen_cleanr_corrected_counts.txt',sep='\t'); print('cn',c.shape,c.columns.tolist(), 'integer?',(c.iloc[:,2:]%1==0).all().all(), c.isna().sum().sum())
for p in glob.glob('consensus*/tier_consensus.csv'):
    t=pd.read_csv(p); print(p,t.shape,t.columns.tolist()); print(t.iloc[:,-1].value_counts().to_dict() if 'tier' not in t else t.tier.value_counts().to_dict())
