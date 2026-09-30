import gzip,os
W='/mnt/openscience/audits/bio-atac-seq-nucleosome-positioning/reaudit-run/out/na/'
reg=[l.split()[:3] for l in open(W+'regions.bed')]
tss=[int(l.split()[1]) for l in open(W+'tss.bed')]
rows=[l.split('\t') for l in gzip.open(W+'patched.nucpos.bed.gz','rt')]
inreg=sum(any(r[0]==x[0] and int(x[1])<=int(r[1])<int(x[2]) for x in reg) for r in rows)
print('nucpos',len(rows),'in regions',inreg)
z=[float(r[4]) for r in rows]; occ=[float(r[5]) for r in rows]
print('z range',min(z),max(z),'occ range',min(occ),max(occ),'NaN',sum(v!=v for v in z))
import statistics
d=[]
for r in rows:
    p=int(r[1]); near=min(tss,key=lambda t:abs(t-p)); d.append(p-near)
print('median dist to nearest TSS',statistics.median([abs(x) for x in d]))
occv=[float(l.split('\t')[3]) for l in gzip.open(W+'patched.occ.bedgraph.gz','rt')]
print('occ bedgraph rows',len(occv),'range',min(occv),max(occv))
print('ctrl nucpos',sum(1 for _ in gzip.open(W+'ctrl.nucpos.bed.gz','rt')))
