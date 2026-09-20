#!/usr/bin/env python3
"""Input 3 supplement: shipped examples/allele_counts.py from the COPY (run/skill/) on edge inputs: contig names containing ':' (GRCh38 HLA
alt contigs and the real UMI BAM's 'chr22:16570000-16610000'), unindexed BAM, malformed regions, empty contig, position 0."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam

I = 3
EX = SKILL + "/examples/allele_counts.py"
W = WORK + "/in03b"; os.makedirs(W, exist_ok=True)

# tiny BAM whose contig looks like a GRCh38 HLA alt contig (contains ':')
hla = "HLA-A*01:01:01:01"
hdr = {"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": hla, "LN": 200}, {"SN": "plain", "LN": 200}]}
seq = "ACGT" * 12 + "AC"
with pysam.AlignmentFile(W + "/hla.bam", "wb", header=hdr) as o:
    for i in range(6):
        a = pysam.AlignedSegment(); a.query_name = f"r{i}"; a.flag = 0; a.reference_id = 0; a.reference_start = 40
        a.mapping_quality = 60; a.cigarstring = f"{len(seq)}M"; a.query_sequence = seq; a.query_qualities = pysam.qualitystring_to_array("I" * len(seq)); o.write(a)
pysam.index(W + "/hla.bam")

def run(args):
    rc, out, err = sh(f"python {EX} {args}")
    return rc, out.strip(), err.strip()

rc, out, err = run(f"{W}/hla.bam '{hla}:50'")
print("colon contig ->", rc, out[:100], "|", err.splitlines()[-1][:120] if err else "")
check(I, "example handles a contig name containing ':' (HLA-A*01:01:01:01:50)", rc == 0 and "Total depth: 6" in out, f"rc={rc} err={err.splitlines()[-1][:100] if err else ''}")
rc, out, err = run(f"{W}/hla.bam plain:50")
check(I, "example on contig 'plain' with no reads at :50 prints depth 0 without crashing", rc == 0 and "Total depth: 0" in out, out.replace("\n", " | "))
# a truly unindexed copy (no .bai beside it)
sh(f"cp {W}/hla.bam {W}/noidx2.bam")
rc, out, err = run(f"{W}/noidx2.bam plain:50")
print("no index ->", rc, err.splitlines()[-1][:120] if err else out)
check(I, "unindexed BAM gives a friendly message (not a raw traceback)", rc != 0 and "Traceback" not in err, f"rc={rc} last line: {err.splitlines()[-1][:100] if err else ''}")
rc, out, err = run(f"{DATA}/syn.bam synA:100-110")
print("range region ->", rc, err.splitlines()[-1][:120] if err else out)
check(I, "region 'synA:100-110' (range, as in mpileup -r) is accepted or explained", rc == 0 or "Traceback" not in err, f"rc={rc} last line: {err.splitlines()[-1][:100] if err else out[:60]}")
rc, out, err = run(f"{DATA}/syn.bam synA:1,000")
check(I, "region with thousands separator 'synA:1,000' is accepted or explained", rc == 0 or "Traceback" not in err, f"rc={rc} last line: {err.splitlines()[-1][:100] if err else ''}")
rc, out, err = run(f"{DATA}/syn.bam nosuch:100")
check(I, "unknown contig gives a friendly message", rc != 0 and "Traceback" not in err, f"rc={rc} last line: {err.splitlines()[-1][:100] if err else ''}")
rc, out, err = run(f"{DATA}/syn.bam synA:0")
print("pos 0 ->", rc, out.replace(chr(10), ' | ')[:120], err.splitlines()[-1][:120] if err else "")
check(I, "position 0 (invalid 1-based) is rejected rather than silently reporting the wrong base", rc != 0 or "Total depth" not in out, f"rc={rc} out={out[:60]!r} err={err.splitlines()[-1][:80] if err else ''}")
rc, out, err = run(f"{DATA}/syn.bam")
check(I, "missing region argument prints the usage line and exits non-zero", rc == 1 and "Usage" in out, out[:80])
rc, out, err = run(f"{DATA}/syn.bam synA:100")
check(I, "control: normal call from copy exits 0", rc == 0 and "T: 30" in out, out.replace("\n", " | ")[:100])
sh(f"rm -f {W}/*.bam {W}/*.bai")
json.dump([c for c in CHECKS if c[0] == I], open(os.path.join(RUN, "checks_in3b.json"), "w"), indent=1)
