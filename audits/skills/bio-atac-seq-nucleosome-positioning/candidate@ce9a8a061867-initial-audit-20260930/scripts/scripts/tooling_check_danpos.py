import os, glob, csv, numpy as np
W=os.environ['NP']+'/work/danpos'
res=[]
def chk(n,ok,i=''): res.append(ok); print('PASS' if ok else 'FAIL',n,i)
def rd(p):
    r=list(csv.reader(open(p),delimiter='\t')); return r[0],r[1:]
h,t=rd(glob.glob(W+'/tuned/pooled/*.smooth.positions.xls')[0]); print(h); print(t[0])
chk('tuned: positions called',len(t)>1000,len(t))
ci=h.index('smt_pos'); sp=np.diff(np.sort([int(x[ci]) for x in t if x[0]=='chr1']))
chk('tuned: spacing >= ~145 (-jd 145)', (sp>=140).mean()>0.98, f'frac>=140 {(sp>=140).mean():.3f}')
chk('tuned: median spacing 150-400', 150<=np.median(sp)<=400, f'{np.median(sp):.0f}')
h,d=rd(glob.glob(W+'/diff/*.positions.integrative.xls')[0]); print(h); print(d[0])
chk('diff: rows',len(d)>1000,len(d))
for c in h:
    if 'shift' in c.lower() or 'dis' in c.lower() or 'pval' in c.lower():
        v=np.array([float(x[h.index(c)]) for x in d if x[h.index(c)] not in ('NA','nan','')]); print(c, 'n',len(v),'min',v.min(),'med',np.median(v),'max',v.max())
print('SUMMARY',sum(res),'/',len(res))
j=h.index('point_diff_FDR'); k=h.index('treat2control_dis')
sh=[(float(x[k]), float(x[j]) if x[j] not in ('NA','') else 1) for x in d]
print('shift column = treat2control_dis (diff_smt_loca is a coordinate). rows shift>=30:', sum(1 for z,f in sh if z>=30), ' and point_diff_FDR<0.05:', sum(1 for z,f in sh if z>=30 and f<0.05))
