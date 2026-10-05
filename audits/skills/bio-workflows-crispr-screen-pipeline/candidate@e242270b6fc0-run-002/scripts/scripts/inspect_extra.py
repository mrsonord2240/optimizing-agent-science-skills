import pandas as pd, numpy as np, os
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/../work')
# CN correction: amplified genes before/after via gene-level mean LFC; and MYC/BRAF
raw=pd.read_csv('cn/a375.count.txt',sep='\t'); cor=pd.read_csv('cn/screen_cleanr_corrected_counts.txt',sep='\t')
def lfc(df,g):
    d=df.set_index(df.columns[0]); c=d.columns[1:]
    n=d[c]/d[c].sum()*1e6
    return np.log2((n.iloc[:,1:].mean(1)+0.5)/(n.iloc[:,0]+0.5)).groupby(d[d.columns[0]]).mean()
a,b=lfc(raw,0),lfc(cor,0)
for g in ['BRAF','MYC','RPS6','AAVS1']:
    print(g, round(a.get(g,np.nan),2), round(b.get(g,np.nan),2))
# RRA: ribosomal / known
g=pd.read_csv('rra/essentiality_rra.gene_summary.txt',sep='\t')
print('RRA RPL/RPS', g[g.id.str.match('^(RPL|RPS)\d')].shape[0], 'hit',(g[g.id.str.match('^(RPL|RPS)\d')]['neg|fdr']<0.05).sum())
print(g[g.id=='RPS6'].T)
# bagel
bf=pd.read_csv('bagel2/bayes_factor.txt',sep='\t'); print(bf[bf.GENE.isin(['RPS6','RPL11','POLR2L','AAVS1'])])
pr=pd.read_csv('bagel2/pr_curve.txt',sep='\t'); print(pr.tail(2))
# drugz sanity
d=pd.read_csv('drugz/drugz_output.txt',sep='\t'); print((d.fdr_synth<0.05).sum(),(d.fdr_supp<0.05).sum())
