"""probe 2: second method for 'does stepper=all + fastafile apply BAQ?': compare the per-read base QUALITIES pysam hands out
in one BAQ-affected column under each stepper (BAQ rewrites qualities in place), and against samtools mpileup's quality column."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam
bam, ref = DATA + "/baq.bam", DATA + "/baq.fa"
mdef = mp_rows(ref, bam, "-Q 0", "bq1:1-1500")[0]
mB = mp_rows(ref, bam, "-Q 0 -B", "bq1:1-1500")[0]
diff = [p for (c, p), r in mdef.items() if r[5] != mB[(c, p)][5]]
print("positions where samtools quality column differs default vs -B (-Q 0):", len(diff), diff[:5])
pos = diff[0]
def quals(**kw):
    fa = pysam.FastaFile(ref)
    if kw.pop("_fa", False): kw["fastafile"] = fa
    with pysam.AlignmentFile(bam) as b:
        for c in b.pileup("bq1", pos - 1, pos, truncate=True, min_base_quality=0, **kw):
            return "".join(chr(33 + pr.alignment.query_qualities[pr.query_position]) for pr in c.pileups if not pr.is_del and not pr.is_refskip)
print("samtools default (-Q 0):", mdef[("bq1", pos)][5])
print("samtools -B      (-Q 0):", mB[("bq1", pos)][5])
for st in ("all", "samtools"):
    print(f"pysam stepper={st:9s} + fastafile qualities:", quals(stepper=st, _fa=True))
    print(f"pysam stepper={st:9s} no fastafile qualities:", quals(stepper=st))
