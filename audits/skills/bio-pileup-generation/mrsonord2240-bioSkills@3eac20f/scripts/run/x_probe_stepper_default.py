"""probe 6: what is pysam 0.24.1's DEFAULT stepper, and does the default + fastafile apply BAQ? (Skill: "either stepper ('all', the default, or 'samtools')")"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam
print("pysam", pysam.__version__)
doc = pysam.AlignmentFile.pileup.__doc__
i = doc.find("stepper")
print("docstring around 'stepper':", re.sub(r"\s+", " ", doc[i:i + 900]))
bam, ref = HBAM, HREF
def depths(**kw):
    with pysam.AlignmentFile(bam) as b:
        if kw.pop("_fa", False): kw["fastafile"] = pysam.FastaFile(ref)
        return {c.pos + 1: len(c.pileups) for c in b.pileup("chr22", 1951, 4617, truncate=True, **kw)}
nd = lambda A, B: sum(1 for k in set(A) | set(B) if A.get(k, 0) != B.get(k, 0))
mdef = {p: int(x[3]) for (c, p), x in mp_rows(ref, bam, "", "chr22:1952-4617")[0].items()}
mB = {p: int(x[3]) for (c, p), x in mp_rows(ref, bam, "-B", "chr22:1952-4617")[0].items()}
print("samtools default vs -B differ at", nd(mdef, mB))
for lab, kw in [("no stepper arg, no fastafile", {}), ("no stepper arg + fastafile", dict(_fa=True)),
                ("stepper='all' + fastafile", dict(stepper="all", _fa=True)), ("stepper='samtools' + fastafile", dict(stepper="samtools", _fa=True)),
                ("stepper='all' no fastafile", dict(stepper="all")), ("stepper='nofilter' no fastafile", dict(stepper="nofilter"))]:
    d = depths(**kw)
    print(f"   {lab:36s} vs samtools default {nd(d, mdef):4d} differ | vs -B {nd(d, mB):4d} differ")
