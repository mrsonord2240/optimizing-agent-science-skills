import sys; sys.path.insert(0,'.')
from common import *
import pysam
from collections import Counter
W=WORK+"/in05"; ART=W+"/artic.bam"; REF=AFDATA+"/sarscov2/MN908947.3.fasta"
def mp(opts):
    _,o,_=sh(f"samtools mpileup -f {REF} -aa -A -d 600000 {opts} {ART}")
    return {int(r[1]):int(r[3]) for r in mpileup_rows(o)}
def expd(minq, mapq=0):
    e=Counter()
    for a in pysam.AlignmentFile(ART):
        if a.flag & 0x704: continue
        for qp,rp in a.get_aligned_pairs():
            if rp is None: continue
            if qp is None or a.query_qualities[qp]>=minq: e[rp+1]+=1
    return e
print(Counter(a.flag for a in pysam.AlignmentFile(ART)))
for opts,minq in [("-B -Q 0",0),("-B -Q 20",20),("-Q 20",20),("-B -Q 13",13)]:
    m=mp(opts); e=expd(minq)
    diff=[p for p in m if m[p]!=e.get(p,0)]
    print(opts,"diff positions",len(diff),"sum m",sum(m.values()),"sum e",sum(e.values()), diff[:5])
print("--- depth minus '*' vs expected without deletions")
def expn(minq):
    e=Counter()
    for a in pysam.AlignmentFile(ART):
        if a.flag & 0x704: continue
        for qp,rp in a.get_aligned_pairs():
            if rp is None or qp is None: continue
            if a.query_qualities[qp]>=minq: e[rp+1]+=1
    return e
_,o,_=sh(f"samtools mpileup -f {REF} -aa -A -d 600000 -B -Q 20 {ART}")
rows=mpileup_rows(o)
e=expn(20)
diff=[]
for r in rows:
    n,c=parse_bases(r[4],r[2]) if r[3]!="0" else (0,Counter())
    if int(r[3])-c["*"]!=e.get(int(r[1]),0): diff.append(int(r[1]))
print("diff", len(diff), diff[:5])
