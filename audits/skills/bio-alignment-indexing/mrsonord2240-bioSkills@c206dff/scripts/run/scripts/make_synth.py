#!/usr/bin/env python3
"""SYNTHETIC test data for the bio-alignment-indexing audit. Everything written here is synthetic.
Run inside WSL:  python make_synth.py <outdir>
"""
import sys, random
import pysam

out = sys.argv[1]
random.seed(20260920)


def rec(hdr, name, flag, tid, pos, mapq=60, cigar="100M", seq=None, mtid=-1, mpos=-1, tlen=0):
    a = pysam.AlignedSegment(hdr)
    a.query_name = name
    a.flag = flag
    a.reference_id = tid
    a.reference_start = pos
    a.mapping_quality = mapq
    a.cigarstring = cigar if not (flag & 4) else None
    a.query_sequence = seq or ("ACGT" * 25)
    a.query_qualities = pysam.qualitystring_to_array("I" * 100)
    a.next_reference_id = mtid
    a.next_reference_start = mpos
    a.template_length = tlen
    return a


# ---- A. wheat-like: contigs > 2^29 (537 Mbp) -------------------------------------------------
hdr = pysam.AlignmentHeader.from_dict({
    "HD": {"VN": "1.6", "SO": "coordinate"},
    "SQ": [{"SN": "chr1A", "LN": 594102056}, {"SN": "chr3B", "LN": 830829764}],
})
positions = {0: [1000, 300_000_000, 540_000_000, 590_000_000], 1: [5000, 536_870_000, 600_000_000, 700_000_000, 830_000_000]}
with pysam.AlignmentFile(f"{out}/wheat_like.bam", "wb", header=hdr) as f:
    n = 0
    for tid in (0, 1):
        for p in positions[tid]:
            f.write(rec(hdr, f"w{n}", 0, tid, p)); n += 1
print("wheat_like.bam written, 9 reads: chr1A positions", positions[0], "chr3B positions", positions[1])

# ---- A2. 2.0 Gbp contig (still inside the BAM int32 limit) -----------------------------------
hdr2 = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "big2g", "LN": 2_000_000_000}]})
with pysam.AlignmentFile(f"{out}/big2g.bam", "wb", header=hdr2) as f:
    for i, p in enumerate([100, 700_000_000, 1_500_000_000, 1_900_000_000]):
        f.write(rec(hdr2, f"g{i}", 0, 0, p))
print("big2g.bam written (LN=2.0e9, reads at 100, 7e8, 1.5e9, 1.9e9)")

# ---- A3. contig LONGER than 2^31-1 (axolotl / pine scale) as a SAM text file ---------------
with open(f"{out}/huge_3g.sam", "w") as f:
    f.write("@HD\tVN:1.6\tSO:coordinate\n@SQ\tSN:huge3g\tLN:3000000000\n")
    f.write("r1\t0\thuge3g\t1000\t60\t100M\t*\t0\t0\t" + "ACGT" * 25 + "\t" + "I" * 100 + "\n")
    f.write("r2\t0\thuge3g\t2500000000\t60\t100M\t*\t0\t0\t" + "ACGT" * 25 + "\t" + "I" * 100 + "\n")
print("huge_3g.sam written")

# ---- B. idxstats semantics: PE orphans, secondary, supplementary, fully unmapped ----------
hdrB = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "chrA", "LN": 10000}]})
recs = []
# pair 1 both mapped
recs.append(rec(hdrB, "p1", 99, 0, 100, mtid=0, mpos=300, tlen=300))
recs.append(rec(hdrB, "p1", 147, 0, 300, mtid=0, mpos=100, tlen=-300))
# pair 2: R1 mapped, R2 unmapped placed at mate position (orphan)
recs.append(rec(hdrB, "p2", 73, 0, 500, mtid=0, mpos=500))
recs.append(rec(hdrB, "p2", 133, 0, 500, mtid=0, mpos=500))
# read with secondary + supplementary
recs.append(rec(hdrB, "s1", 0, 0, 700))
recs.append(rec(hdrB, "s1", 256, 0, 900, mapq=0))
recs.append(rec(hdrB, "s1", 2048, 0, 1100, cigar="50M50S"))
recs.append(rec(hdrB, "s1", 2048, 0, 1300, cigar="50S50M"))
recs.sort(key=lambda a: a.reference_start)
# fully unmapped pair (no RNAME) goes last
recs.append(rec(hdrB, "u1", 77, -1, -1, mtid=-1, mpos=-1))
recs.append(rec(hdrB, "u1", 141, -1, -1, mtid=-1, mpos=-1))
with pysam.AlignmentFile(f"{out}/semantics.bam", "wb", header=hdrB) as f:
    for a in recs:
        f.write(a)
print("semantics.bam written: 10 records")

# ---- C. HLA-style contig name containing ':' -----------------------------------------------
hdrC = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"},
    "SQ": [{"SN": "chr1", "LN": 100000}, {"SN": "HLA-A*01:01:01:01", "LN": 3503}]})
with pysam.AlignmentFile(f"{out}/hla_contig.bam", "wb", header=hdrC) as f:
    f.write(rec(hdrC, "c1", 0, 0, 100)); f.write(rec(hdrC, "c2", 0, 0, 500))
    f.write(rec(hdrC, "h1", 0, 1, 10)); f.write(rec(hdrC, "h2", 0, 1, 1000)); f.write(rec(hdrC, "h3", 0, 1, 3000))
print("hla_contig.bam written: 2 reads chr1, 3 reads HLA-A*01:01:01:01")

# ---- D. big BAM for -L / -M and threads tests ---------------------------------------------
N = int(sys.argv[2]) if len(sys.argv) > 2 else 1_200_000
hdrD = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "chr1", "LN": 200_000_000}]})
poss = sorted(random.randrange(0, 199_999_000) for _ in range(N))
bases = "ACGT"
with pysam.AlignmentFile(f"{out}/big.bam", "wb", header=hdrD, threads=4) as f:
    for i, p in enumerate(poss):
        s = "".join(random.choices(bases, k=100))
        f.write(rec(hdrD, f"b{i}", 0, 0, p, seq=s))
print("big.bam written:", N, "reads")
with open(f"{out}/big.positions.txt", "w") as fh:
    fh.write("\n".join(map(str, poss)))
