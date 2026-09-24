"""probe: does stepper='all' + fastafile apply BAQ?  (round-2 claim) -- on syn.bam (previous auditors' data) and my baq.bam / sarscov2 SE"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam
def depths(bam, ref, chrom, s, e, **kw):
    fa = pysam.FastaFile(ref)
    if kw.pop("_fa", False): kw["fastafile"] = fa
    with pysam.AlignmentFile(bam) as b:
        return {c.pos + 1: len(c.pileups) for c in b.pileup(chrom, s, e, truncate=True, **kw)}
def nd(A, B): return sum(1 for k in set(A) | set(B) if A.get(k, 0) != B.get(k, 0))
for name, bam, ref, c, s, e in [("syn", SYN, SYNREF, "synA", 0, 1000), ("own baq", DATA + "/baq.bam", DATA + "/baq.fa", "bq1", 0, 1500),
        ("sc SE", DATA + "/sc_test.single_end.sorted.bam", AFDATA + "/sarscov2/genome.fasta", "MT192765.1", 0, 29829)]:
    r = {}
    for st in ("all", "samtools"):
        r[st + "+fa"] = depths(bam, ref, c, s, e, stepper=st, _fa=True)
        r[st + " nofa"] = depths(bam, ref, c, s, e, stepper=st)
        r[st + "+fa,nobaq"] = depths(bam, ref, c, s, e, stepper=st, _fa=True, compute_baq=False)
    mdef = {p: int(x[3]) for (cc, p), x in mp_rows(ref, bam, "", f"{c}:{s+1}-{e}")[0].items()}
    mB = {p: int(x[3]) for (cc, p), x in mp_rows(ref, bam, "-B", f"{c}:{s+1}-{e}")[0].items()}
    print(name, "| samtools default vs -B differ at", nd(mdef, mB))
    for k, v in r.items():
        print(f"   pysam {k:22s} differs from mpileup default at {nd(v, mdef):5d}, from -B at {nd(v, mB):5d}")
