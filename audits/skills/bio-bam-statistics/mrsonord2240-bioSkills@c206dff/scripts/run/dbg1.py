import pysam, numpy as np, collections
bam='data/synth.bam'
d=np.zeros(5000,int)
with pysam.AlignmentFile(bam) as f:
    for col in f.pileup('synth2',0,5000,truncate=True):
        d[col.reference_pos]=col.n
cls=collections.Counter()
with pysam.AlignmentFile(bam) as f:
    for r in f.fetch('synth2'):
        if r.flag&(4|256|512|1024): continue
        seen = d[r.reference_start:r.reference_end]
        cls[(r.query_name[0], r.flag, r.mapping_quality, 'seen_all' if (seen>0).all() else 'seen_none' if (seen==0).all() else 'partial')]+=1
for k,v in sorted(cls.items()): print(k,v)
