# usage: python check.py aligned.bam UP_START UP_END DOWN_START DOWN_END SKIP_START SKIP_END
# intron coordinates 0-based half-open (BED12 block gaps): UP/DOWN = introns flanking the microexon, SKIP = exon1 end to exon3 start
import sys, pysam
bam, *c = sys.argv[1:]; c = list(map(int, c)); up, down, skip = tuple(c[0:2]), tuple(c[2:4]), tuple(c[4:6])
inc = exc = 0
for r in pysam.AlignmentFile(bam):
    if r.is_unmapped or r.is_secondary or r.is_supplementary: continue
    pos, introns = r.reference_start, set()
    for op, n in r.cigartuples:
        if op == 3: introns.add((pos, pos + n))
        if op in (0, 2, 3, 7, 8): pos += n
    inc += up in introns and down in introns
    exc += skip in introns
print("inclusion reads", inc, "skipping reads", exc)
