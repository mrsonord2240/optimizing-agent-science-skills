"""Independent 3-prime residual count (no shipped code). cwd = out/i1. A read is residual if its aligned 3' end still lies
inside an opposite-strand primer footprint: forward read -> end inside a '-' primer; reverse read -> start inside a '+' primer."""
import pysam
prim = [l.rstrip("\n").split("\t") for l in open("primers.bed") if l.strip()]
L = [(int(p[1]), int(p[2])) for p in prim if p[5] == "+"]; Rr = [(int(p[1]), int(p[2])) for p in prim if p[5] == "-"]
for tag in ["default", "strand", "both", "both_strand"]:
    n = res = 0
    for r in pysam.AlignmentFile(f"m_{tag}.bam").fetch(until_eof=True):
        n += 1
        if not r.is_reverse: res += any(s < r.reference_end <= e for s, e in Rr)
        else: res += any(s <= r.reference_start < e for s, e in L)
    print(f"  {tag:12s} n={n} 3' residual={res} ({100 * res / n:.1f}%)")
