"""Planted-truth differential input for DANPOS3: take GM12878 rep1 chr1:10-14 Mb; 'treat' = the same reads with every pair in chr1:10-12 Mb shifted +40 bp
(both mates), reads in 12-14 Mb unchanged. Truth: shift 40 bp in 10-12 Mb, 0 in 12-14 Mb. Same reads => no biological difference otherwise."""
import os, pysam
D = os.environ['ATACDATA']; W = os.environ['NP'] + '/work/a4'
os.makedirs(W, exist_ok=True)
src = pysam.AlignmentFile(f'{D}/encode/GM12878_rep1_filtered.chr1_1-30000000.bam', 'rb')
ctl = pysam.AlignmentFile(f'{W}/ctl.unsorted.bam', 'wb', template=src)
trt = pysam.AlignmentFile(f'{W}/trt.unsorted.bam', 'wb', template=src)
n = ns = 0
for r in src.fetch('chr1', 10_000_000, 14_000_000):
    if r.is_unmapped or r.mate_is_unmapped or not r.is_proper_pair: continue
    if not (10_000_000 <= r.reference_start < 14_000_000 and 10_000_000 <= r.next_reference_start < 14_000_000): continue
    ctl.write(r); n += 1
    q = r  # shifting a copy
    q = pysam.AlignedSegment.fromstring(r.tostring(), src.header)
    if q.reference_start < 12_000_000 and q.next_reference_start < 12_000_000:
        q.reference_start += 40; q.next_reference_start += 40; ns += 1
    trt.write(q)
ctl.close(); trt.close(); print('records', n, 'shifted', ns)
