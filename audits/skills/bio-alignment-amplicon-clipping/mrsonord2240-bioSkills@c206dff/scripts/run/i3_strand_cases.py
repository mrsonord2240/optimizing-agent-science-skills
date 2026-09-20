"""SYNTHETIC single-end reads that discriminate --strand / --both-ends semantics. Primers: run/data/synth_primers.bed
(L2 = [300,325) '+', R1 = [325,350) '-'). Reads are error-free copies of the reference. Run in WSL env python."""
import pysam
D = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/data"
ref = pysam.FastaFile(f"{D}/synth.fa").fetch("amp1")
cases = [  # name, start, end, reverse?
    ("c1_rev_5end_inside_plusprimer", 250, 310, True),
    ("c2_fwd_control_no_primer",      140, 200, False),
    ("c3_fwd_5end_inside_plusprimer", 310, 370, False),
    ("c4_fwd_3end_inside_minusprimer",250, 330, False),
    ("c5_fwd_3end_inside_plusprimer", 250, 315, False),
    ("c6_rev_3end_inside_plusprimer", 315, 375, True),
    ("c7_rev_3end_inside_minusprimer",330, 400, True),
    ("c8_rev_5end_inside_minusprimer",270, 335, True),
]
hdr = {"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "amp1", "LN": len(ref)}]}
with pysam.AlignmentFile(f"{D}/strand_cases.bam", "wb", header=hdr) as o:
    for n, s, e, rev in sorted(cases, key=lambda c: c[1]):
        a = pysam.AlignedSegment(); a.query_name = n; a.reference_id = 0; a.reference_start = s
        a.flag = 16 if rev else 0; a.mapping_quality = 60; a.query_sequence = ref[s:e]
        a.cigartuples = [(0, e - s)]; a.query_qualities = pysam.qualitystring_to_array("I" * (e - s)); o.write(a)
pysam.index(f"{D}/strand_cases.bam"); print("wrote", len(cases), "reads")
