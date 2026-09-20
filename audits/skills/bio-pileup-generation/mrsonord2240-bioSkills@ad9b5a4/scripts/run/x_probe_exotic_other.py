"""probe: what are the 'other' differences in the exotic-CIGAR fuzz (default options)?"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions
import pysam
pt = load_functions("SKILL.md")["pileup_text"]
bam, ref = DATA + "/fz_exotic.bam", DATA + "/fz_exotic.fa"
strip = lambda t: re.sub(r"[+-]\d+[A-Za-z]+", "", t)
n = 0
for c, L in (("fz1", 3000), ("fz2", 1500)):
    mpd, _, _, _ = mp_rows(ref, bam, "", c)
    for line in pt(bam, ref, c, 0, L):
        f = line.split("\t")
        a = mpd.get((f[0], int(f[1])))
        if a and a != f and not (strip(a[4]) == strip(f[4]) and a[3] == f[3] and a[5] == f[5]):
            n += 1
            print(f[0], f[1], "mpileup:", a[3:5], "| pileup_text:", f[3:5])
print("other rows:", n)
