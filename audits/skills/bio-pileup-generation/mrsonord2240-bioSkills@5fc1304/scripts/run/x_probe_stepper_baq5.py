"""probe 5: reconcile: pysam defaults (stepper='all', no fastafile) vs samtools mpileup -B on the human BAM, region 1951-4617"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam
def depths(s, e, **kw):
    with pysam.AlignmentFile(HBAM) as b:
        if kw.pop("_fa", False): kw["fastafile"] = pysam.FastaFile(HREF)
        return {c.pos + 1: len(c.pileups) for c in b.pileup("chr22", s, e, truncate=True, **kw)}
mB = {p: int(x[3]) for (c, p), x in mp_rows(HREF, HBAM, "-B", "chr22:1952-4617")[0].items()}
for st in ("all", "samtools"):
    for fa in (False, True):
        d = depths(1951, 4617, stepper=st, _fa=fa)
        diff = [(p, mB.get(p), d.get(p)) for p in sorted(set(mB) | set(d)) if mB.get(p, 0) != d.get(p, 0)]
        print(f"pysam stepper={st:8s} fastafile={fa!s:5s} vs samtools -B (chr22:1952-4617): {len(diff)} differ; first {diff[:3]}")
