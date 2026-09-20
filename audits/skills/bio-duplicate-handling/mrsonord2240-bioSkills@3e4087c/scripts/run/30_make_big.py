"""SYNTHETIC 400k-pair (800k-read) coordinate-sorted PE BAM on a 5 Mb contig, ~15% duplicate pairs, for timing the SKILL.md '~30% faster' claim."""
import pysam, random, sys
out = sys.argv[1]; NP = int(sys.argv[2])
rnd = random.Random(3)
L = 100
h = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "big", "LN": 5000000}],
                                     "RG": [{"ID": "rg1", "LB": "lib1", "SM": "s", "PL": "ILLUMINA"}]})
bases = "ACGT"
seqs = ["".join(rnd.choice(bases) for _ in range(L)) for _ in range(64)]      # reuse a few sequences; the marker does not read them
recs = []; frags = []
for i in range(NP):
    if frags and rnd.random() < 0.15:
        p1, ins = rnd.choice(frags[-5000:])
    else:
        p1 = rnd.randrange(0, 4999000 - 400); ins = 150 + rnd.randrange(250); frags.append((p1, ins))
    p2 = p1 + ins - L
    n = "r%d" % i
    for fl, pos, mpos, tl in ((99, p1, p2, ins), (147, p2, p1, -ins)):
        a = pysam.AlignedSegment(h); a.query_name = n; a.flag = fl; a.reference_id = 0; a.reference_start = pos; a.mapping_quality = 60
        a.cigartuples = [(0, L)]; a.query_sequence = seqs[i & 63]; a.query_qualities = pysam.qualitystring_to_array("I" * L)
        a.next_reference_id = 0; a.next_reference_start = mpos; a.template_length = tl; a.set_tag("RG", "rg1"); recs.append(a)
recs.sort(key=lambda a: (a.reference_start, a.query_name))
with pysam.AlignmentFile(out, "wb", header=h) as o:
    for a in recs: o.write(a)
pysam.index(out); print("wrote", out, len(recs), "records")
