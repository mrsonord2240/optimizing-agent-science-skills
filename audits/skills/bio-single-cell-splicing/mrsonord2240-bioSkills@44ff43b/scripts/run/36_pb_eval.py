import pandas as pd, numpy as np
R='/mnt/openscience/audits/bio-single-cell-splicing/run'; O=f'{R}/out/pb_lc'
truth = pd.read_csv(f'{R}/data/marvel_planted_truth.tsv', sep='\t', keep_default_na=False)
truth['clu']=[f'clu_{i+1}_+' for i in range(len(truth))]
for tag,desc in [('a','n=1 vs n=1 (Skill pseudobulk_junctions output)'),('b','5 v 5 replicate pseudobulks')]:
    s=pd.read_csv(f'{O}/{tag}_out_cluster_significance.txt',sep='\t')
    s['clu']=s.cluster.str.split(':').str[-1]; s=s.merge(truth[['clu','cls']],on='clu')
    tested=s[s.status=='Success']
    print(f'== {desc}: clusters tested {len(tested)}')
    print(tested.groupby('cls').agg(n=('p','size'),p05=('p',lambda x:(x<.05).sum()),fdr05=('p.adjust',lambda x:(x<.05).sum())).to_string())
