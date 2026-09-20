# SYNTHETIC ancient-DNA-like single-end BAM on the real 40 kb human slice: 6000 reads x 60 bp,
# C>T at the 5' end (p=0.35*0.6^i) and G>A at the 3' end. Run from work/in07/md (ref path relative).
import pysam, random
r = random.Random(5)
ref = pysam.FastaFile("ref.fa"); name = ref.references[0]; g = ref.fetch(name).upper()
hd = {"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": name, "LN": len(g)}], "RG": [{"ID": "d1", "SM": "anc", "LB": "l1", "PL": "ILLUMINA"}]}
h = pysam.AlignmentHeader.from_dict(hd)
recs = []
def damaged(s):
    s = list(s); n = len(s)
    for i in range(n):
        if s[i] == "C" and r.random() < 0.35 * 0.6 ** i: s[i] = "T"
        j = n - 1 - i
        if s[j] == "G" and r.random() < 0.35 * 0.6 ** i: s[j] = "A"
    return "".join(s)
for k in range(6000):
    p = r.randrange(0, len(g) - 60)
    s = g[p:p + 60]
    if "N" in s: continue
    a = pysam.AlignedSegment(h); a.query_name = "d%d" % k; a.flag = 0; a.reference_id = 0; a.reference_start = p
    a.mapping_quality = 60; a.cigartuples = [(0, 60)]; a.query_sequence = damaged(s)
    a.query_qualities = pysam.qualitystring_to_array("I" * 60); a.set_tag("RG", "d1"); recs.append(a)
recs.sort(key=lambda a: a.reference_start)
with pysam.AlignmentFile("marked.bam", "wb", header=h) as o:
    for a in recs: o.write(a)
pysam.index("marked.bam"); print("damaged marked.bam:", len(recs), "forward-strand reads")
