"""Residual primer-derived positions at the 3' end (real ARTIC nanopore BAM, full-length amplicon reads). WSL env python.
A read is 'residual' if its aligned 3' end still lies inside a primer footprint of the opposite strand
(fwd read: end inside a '-' primer; rev read: start inside a '+' primer)."""
import pysam
D = "/mnt/openscience/audit-envs/alignment-files/public-data/sarscov2"; W = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/out/i1"
prim = [l.rstrip("\n").split("\t") for l in open(f"{D}/v5.3.2.primer.bed") if l.strip()]
L = [(int(p[1]), int(p[2])) for p in prim if p[5] == "+"]; Rr = [(int(p[1]), int(p[2])) for p in prim if p[5] == "-"]
for tag in ["default", "strand", "both", "both_strand", "hard"]:
    n = res = 0
    for r in pysam.AlignmentFile(f"{W}/m_{tag}.bam").fetch(until_eof=True):
        n += 1
        if not r.is_reverse: res += any(s < r.reference_end <= e for s, e in Rr)
        else: res += any(s <= r.reference_start < e for s, e in L)
    print(f"{tag:12s} reads={n} reads with 3' end still inside an opposite-strand primer footprint: {res} ({100*res/n:.1f}%)")
