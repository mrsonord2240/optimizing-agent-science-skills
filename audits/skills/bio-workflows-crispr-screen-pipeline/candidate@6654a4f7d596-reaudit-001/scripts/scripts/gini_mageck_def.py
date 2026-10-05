import pandas as pd, numpy as np, mageck.mageckCount as m
B='F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline/'
for name,p in [('HAP1 TKOv3 (real)','qc/hap1.count.txt'),('A375 KY Project Score (real)','cn-correction/a375.count.txt'),('simulated qcpass HAP1','rra-qcpass/hap1.count.txt')]:
    t=pd.read_csv(B+p,sep='\t',index_col=0).iloc[:,1:]
    print(name)
    for c in t.columns:
        v=t[c].values.astype(float)
        print(f'  {c:26s} MAGeCK-definition Gini (ln(x+1)) {m.mageckcount_gini(list(np.log(v+1))):.3f} | raw-count Gini {m.mageckcount_gini(list(v)):.3f}')
