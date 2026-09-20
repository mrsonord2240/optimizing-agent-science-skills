"""probe 3: which pysam argument makes stepper='all' + fastafile apply BAQ?  own baq.bam (single-end, no overlaps, no orphans).
Reference = samtools mpileup default (BAQ on) and -B, both at -d 1000000 and at the default -d 8000."""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam
bam, ref = DATA + "/baq.bam", DATA + "/baq.fa"
def depths(**kw):
    fa = pysam.FastaFile(ref)
    if kw.pop("_fa", False): kw["fastafile"] = fa
    with pysam.AlignmentFile(bam) as b:
        return {c.pos + 1: len(c.pileups) for c in b.pileup("bq1", 0, 1500, truncate=True, **kw)}
nd = lambda A, B: sum(1 for k in set(A) | set(B) if A.get(k, 0) != B.get(k, 0))
mdef = {p: int(x[3]) for (c, p), x in mp_rows(ref, bam, "-d 1000000", "bq1:1-1500")[0].items()}
mB = {p: int(x[3]) for (c, p), x in mp_rows(ref, bam, "-B -d 1000000", "bq1:1-1500")[0].items()}
print("samtools default vs -B differ at", nd(mdef, mB), "positions (-d 1000000)")
for label, kw in [("all+fa", {}), ("all+fa max_depth=1000000", dict(max_depth=1000000)), ("all+fa max_depth=8000", dict(max_depth=8000)),
                  ("all+fa redo_baq=True", dict(redo_baq=True)), ("all+fa compute_baq=True", dict(compute_baq=True)),
                  ("all+fa max_depth=1000000 + redo_baq", dict(max_depth=1000000, redo_baq=True)),
                  ("all+fa ignore_overlaps=False", dict(ignore_overlaps=False)),
                  ("all+fa min_base_quality=0 -> vs samtools -Q 0 not compared", dict(min_base_quality=13))]:
    d = depths(stepper="all", _fa=True, **kw)
    print(f"{label:60s} vs samtools default: {nd(d, mdef):4d} differ | vs -B: {nd(d, mB):4d} differ")
for label, kw in [("samtools+fa", {}), ("samtools+fa max_depth=1000000", dict(max_depth=1000000))]:
    d = depths(stepper="samtools", _fa=True, **kw)
    print(f"{label:60s} vs samtools default: {nd(d, mdef):4d} differ | vs -B: {nd(d, mB):4d} differ")
