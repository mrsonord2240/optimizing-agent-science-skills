import pandas as pd, numpy as np, os
W='F:/OpenScience/fix-evidence/recut-crispr-pipeline/reaudit-001/work/'
rd=lambda p,**k: pd.read_csv(W+p,sep='\t',**k)
c=rd('count/experiment.count.txt'); print('count',c.shape, 'zero-all rows',int((c.iloc[:,2:].sum(axis=1)==0).sum()), 'col sums',c.iloc[:,2:].sum().tolist())
s=rd('count/experiment.countsummary.txt'); print(s[['Label','Mapped','Percentage','GiniIndex']].to_string())
g=rd('rra/hap1_rra.gene_summary.txt'); print('rra hap1',len(g)); print(g.nsmallest(5,'neg|rank')[['id','neg|lfc','neg|fdr']].to_string())
print('pos top',g.nsmallest(3,'pos|rank')[['id','pos|lfc','pos|fdr']].to_string())
neg=pd.read_csv(W+'rra/hap1_rra_negative_hits.csv'); print('neg hits',len(neg),'all lfc<0',bool((neg['neg|lfc']<0).all()),'max fdr',neg['neg|fdr'].max())
g=rd('rra/essentiality_rra.gene_summary.txt'); print('rra qcpass',len(g)); 
ceg=set(rd('bagel2/CEGv2.txt')['GENE']); 
n=pd.read_csv(W+'rra/essentiality_rra_negative_hits.csv'); print('qcpass neg hits',len(n),'frac CEGv2',round(n['id'].isin(ceg).mean(),2))
b=rd('bagel2/bayes_factor.txt'); b2=rd('bagel2/bayes_factor2.txt'); print('bagel',len(b),'BF>6',int((b.BF>6).sum()),'maxdiff seeded rerun',float((b.BF-b2.BF).abs().max()), 'cols',b.columns.tolist()); print(b.nlargest(3,'BF')[['GENE','BF']].to_string())
print('CEG mean BF',b[b.GENE.isin(ceg)].BF.mean())
p=rd('bagel2/pr_curve.txt'); print('pr cols',p.columns.tolist()); 
m=rd('mle/timecourse_mle.gene_summary.txt'); print('mle',m.shape,m.columns.tolist()[:8]); print(m.nsmallest(3,'HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE|beta')[['Gene','HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE|beta','HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE|fdr']].to_string())
d=rd('drugz/drugz_output.txt'); print('drugz',d.shape,d.columns.tolist(),'nan',int(d.isna().sum().sum()))
j=rd('jacks/jacks_out_gene_JACKS_results.txt',index_col=0); print('jacks',j.shape); r=j[[i.startswith(('RPL','RPS')) for i in j.index]]; print('ribosomal mean',r.mean().round(2).to_dict(),'all',j.mean().round(2).to_dict())
ge=pd.read_csv(W+'chronos/gene_effects.csv',index_col=0); print('chronos',ge.shape,'nan',int(ge.isna().sum().sum())); rr=ge.loc[:,[x.startswith(('RPL','RPS')) for x in ge.columns]]; print('ribosomal mean',rr.mean(axis=1).round(2).to_dict(),'all',ge.mean(axis=1).round(2).to_dict())
cc=pd.read_csv(W+'cn/screen_cleanr_corrected_counts.txt',sep='\t'); print('cn',cc.shape,'NA',int(cc.isna().sum().sum()),'nonint',bool((cc.iloc[:,2:]!=cc.iloc[:,2:].round()).any().any()))
raw=pd.read_csv(W+'cn/a375.count.txt',sep='\t'); print('raw',raw.shape,list(raw.columns))
t=pd.read_csv(W+'consensus/tier_consensus.csv'); print('consensus',t.tier.value_counts().to_dict(), t.columns.tolist())
