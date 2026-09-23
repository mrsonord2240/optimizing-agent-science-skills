"""Synthetic unaligned PacBio-style HiFi BAM for the documented pbmarkdup command.

It contains 60 reads, twelve exact duplicated molecule sequences, and no clinical data.
"""
import random
import pysam

rng = random.Random(11)
header = pysam.AlignmentHeader.from_dict({
    "HD": {"VN": "1.6", "SO": "unknown", "pb": "5.0.0"},
    "RG": [{"ID": "ab12cd34/0--0", "PL": "PACBIO", "SM": "sample1", "LB": "lib1"}],
})
sequences = ["".join(rng.choice("ACGT") for _ in range(1200)) for _ in range(48)]
with pysam.AlignmentFile("hifi.bam", "wb", header=header) as bam:
    for index, sequence in enumerate(sequences + sequences[:12]):
        read = pysam.AlignedSegment(header)
        read.query_name = f"m84011_220902_175841_s1/{100 + index}/ccs"
        read.flag = 4
        read.query_sequence = sequence
        read.query_qualities = pysam.qualitystring_to_array("~" * len(sequence))
        read.set_tag("RG", "ab12cd34/0--0")
        read.set_tag("zm", 100 + index)
        read.set_tag("np", 10)
        read.set_tag("rq", 0.999, "f")
        bam.write(read)
print("hifi.bam: 60 reads; 12 planted exact duplicate sequences")
