import pandas as pd, os
HERE=os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(HERE,'data','derived','pid_pairs_R.tsv'), sep='\t', keep_default_na=False)
r = df[df.name=='globin|MYG_PHYMC|HBAZ_HUMAN|global'].iloc[0]
print(r.a); print(r.b)
print('ps,pe,ss,se', r.ps, r.pe, r.ss, r.se, 'len pfull', len(r.pfull), 'len sfull', len(r.sfull), 'ungapped a,b', len(r.a.replace('-','')), len(r.b.replace('-','')))
print(r.PID1, r.PID2, r.PID3, r.PID4)
