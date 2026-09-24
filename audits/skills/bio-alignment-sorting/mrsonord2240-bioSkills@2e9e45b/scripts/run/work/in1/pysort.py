import pysam, hashlib
from skillfns import is_coordinate_sorted, ensure_coordinate_sorted
D='/mnt/openscience/audits/bio-alignment-sorting/run/data/'
pysam.sort('-o', 'py_sorted.bam', D+'shuffled_real.bam')
pysam.sort('-@', '4', '-m', '2G', '-T', '/tmp/sortpfx', '-o', 'py_sorted2.bam', D+'shuffled_real.bam')
def recs(p):
    with pysam.AlignmentFile(p,'rb') as f:
        return [r.to_string() for r in f.fetch(until_eof=True)]
a, b, c = recs('py_sorted.bam'), recs('py_sorted2.bam'), recs('sorted.bam')
print("pysam.sort == CLI:", a == c, "| pysam.sort(-@ -m -T) == CLI:", b == c, "| n=", len(a)); assert a == c and b == c
print("is_coordinate_sorted: sorted.bam", is_coordinate_sorted('sorted.bam'), "| shuffled", is_coordinate_sorted(D+'shuffled_real.bam'))
assert is_coordinate_sorted('sorted.bam') and not is_coordinate_sorted(D+'shuffled_real.bam')
r = ensure_coordinate_sorted(D+'shuffled_real.bam', 'ens.bam'); print('ensure(shuffled) ->', r)
assert r == 'ens.bam' and is_coordinate_sorted('ens.bam')
r2 = ensure_coordinate_sorted('sorted.bam', 'never.bam'); print('ensure(sorted) ->', r2); assert r2 == 'sorted.bam'
# the SKILL's stated point: a mislabelled SO:coordinate BAM must be re-sorted
with pysam.AlignmentFile(D+'shuffled_real.bam','rb') as i:
    hd=i.header.to_dict(); rs=list(i)
hd['HD']={'VN':'1.6','SO':'coordinate'}
with pysam.AlignmentFile('liar.bam','wb',header=pysam.AlignmentHeader.from_dict(hd)) as o:
    for x in rs: o.write(x)
r3 = ensure_coordinate_sorted('liar.bam','liar_fixed.bam'); print('ensure(liar) ->', r3)
assert r3 == 'liar_fixed.bam' and is_coordinate_sorted('liar_fixed.bam')
print("PASS: all pysam assertions")
