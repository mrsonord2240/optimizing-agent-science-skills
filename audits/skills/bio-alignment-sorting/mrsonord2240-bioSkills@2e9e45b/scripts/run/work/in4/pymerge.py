import pysam
pysam.merge('-c', '-p', '-f', 'py_merged.bam', 'h.bam', 'p.bam')
def recs(p):
    with pysam.AlignmentFile(p,'rb') as f: return [r.to_string() for r in f.fetch(until_eof=True)]
a, b = recs('py_merged.bam'), recs('merged.bam')
print('pysam.merge == CLI merge:', a == b, 'n=', len(a)); assert a == b and len(a) == 6144
try:
    pysam.merge('-f', 'x.bam', 'nope1.bam', 'nope2.bam')
    print('pysam.merge on missing inputs: NO EXCEPTION')
except Exception as e:
    print('pysam.merge on missing inputs raised', type(e).__name__, '|', str(e)[:90].replace('\n',' '))
