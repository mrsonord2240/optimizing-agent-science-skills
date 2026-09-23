#!/usr/bin/env python3
"""Create deterministic, small reference/BAM fixtures for the final-pass audit."""
from pathlib import Path
import pysam

out = Path(__file__).resolve().parent / "data"
out.mkdir(parents=True, exist_ok=True)
seq1 = ("ACGT" * 30)[:120]
seq1 = seq1[:60] + "NNNNNNNNNN" + seq1[70:]
seq2 = ("TGCA" * 20)[:80]
(out / "toy.fa").write_text(f">chr1\n{seq1}\n>chr2\n{seq2}\n", encoding="ascii")
(out / "toy_numeric.fa").write_text(f">1\n{seq1}\n>2\n{seq2}\n", encoding="ascii")
header = {"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "chr1", "LN": 120}, {"SN": "chr2", "LN": 80}]}
unsorted = out / "toy.unsorted.bam"
with pysam.AlignmentFile(unsorted, "wb", header=header) as bam:
    for i in range(10):
        rec = pysam.AlignedSegment()
        rec.query_name = f"left{i}"
        bases = list(seq1[:40])
        if i < 6:
            bases[9] = "T" if bases[9] != "T" else "A"
        rec.query_sequence = "".join(bases)
        rec.flag = 0
        rec.reference_id = 0
        rec.reference_start = 0
        rec.mapping_quality = 60
        rec.cigar = ((0, 40),)
        rec.query_qualities = pysam.qualitystring_to_array("I" * 40)
        bam.write(rec)
    for i in range(4):
        rec = pysam.AlignedSegment()
        rec.query_name = f"right{i}"
        rec.query_sequence = seq1[80:120]
        rec.flag = 0
        rec.reference_id = 0
        rec.reference_start = 80
        rec.mapping_quality = 60
        rec.cigar = ((0, 40),)
        rec.query_qualities = pysam.qualitystring_to_array("I" * 40)
        bam.write(rec)
pysam.sort("-o", str(out / "toy.bam"), str(unsorted))
unsorted.unlink()
pysam.index(str(out / "toy.bam"))
