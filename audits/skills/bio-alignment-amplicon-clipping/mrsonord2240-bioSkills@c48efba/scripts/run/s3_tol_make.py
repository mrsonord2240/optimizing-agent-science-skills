"""SYNTHETIC: forward reads (60 bp, error-free) whose 5' start sits at 300+d for d in -8..12 against the '+' primer [300,325) on amp1,
to measure what --tolerance means. Output data/tol_cases.bam (coordinate-sorted, indexed). WSL env python."""
import pysam
D = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/data"
ref = pysam.FastaFile(f"{D}/synth.fa").fetch("amp1")
hdr = {"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "amp1", "LN": len(ref)}]}
recs = []
for d in range(-8, 13):
    s = 300 + d
    a = pysam.AlignedSegment(); a.query_name = f"d{d:+03d}"; a.reference_id = 0; a.reference_start = s; a.flag = 0; a.mapping_quality = 60
    a.query_sequence = ref[s:s + 60]; a.cigartuples = [(0, 60)]; a.query_qualities = pysam.qualitystring_to_array("I" * 60); recs.append(a)
recs.sort(key=lambda a: a.reference_start)
with pysam.AlignmentFile(f"{D}/tol_cases.bam", "wb", header=hdr) as o:
    for a in recs: o.write(a)
pysam.index(f"{D}/tol_cases.bam"); print("wrote", len(recs))
