"""probe 4: replicate the round-2 claim on the human chr22 test BAM (paired-end, the data the fixer names): stepper='all' + fastafile vs
samtools default / -B, depth per position.  Also with ignore_overlaps=False and ignore_orphans=False and -x -A on the samtools side to
remove the overlap/orphan differences between the two steppers."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam
bam, ref = HBAM, HREF
def depths(**kw):
    fa = pysam.FastaFile(ref)
    if kw.pop("_fa", False): kw["fastafile"] = fa
    with pysam.AlignmentFile(bam) as b:
        return {c.pos + 1: len(c.pileups) for c in b.pileup("chr22", 0, 4700, truncate=True, **kw)}
nd = lambda A, B: sum(1 for k in set(A) | set(B) if A.get(k, 0) != B.get(k, 0))
for so, kw0, lab in [("", {}, "default options"), ("-x -A", dict(ignore_overlaps=False, ignore_orphans=False), "-x -A / ignore_overlaps=False, ignore_orphans=False")]:
    mdef = {p: int(x[3]) for (c, p), x in mp_rows(ref, bam, so, "chr22:1-4700")[0].items()}
    mB = {p: int(x[3]) for (c, p), x in mp_rows(ref, bam, so + " -B", "chr22:1-4700")[0].items()}
    print(f"[{lab}] samtools default vs -B differ at", nd(mdef, mB))
    for st in ("all", "samtools"):
        d = depths(stepper=st, _fa=True, **kw0)
        print(f"   stepper={st:8s}+fa vs default: {nd(d, mdef):4d} differ | vs -B: {nd(d, mB):4d} differ")
