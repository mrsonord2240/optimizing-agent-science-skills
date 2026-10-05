import math,pandas as pd
from mageck.mageckCount import mageckcount_gini
t=pd.read_csv('F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline/qc/hap1.count.txt',sep='\t',index_col=0).iloc[:,1:]
for c in t: print(c,round(mageckcount_gini([math.log(v+1.0) for v in t[c]]),3))
