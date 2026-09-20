"""SYNTHETIC test BAMs for the duplicate-handling audit (labelled synthetic; written to run/data/).
1. synth_optical.bam  : Illumina-style read names, PE 100bp, all pairs at the same coordinates -> all duplicate sets.
   Groups (each group = 2 pairs at identical position, tile identical):
     G1 dx=50   dy=50    -> optical at -d 100 and -d 2500
     G2 dx=1000 dy=1000  -> optical at -d 2500 only (dist ~1414? -> pixel distance uses each axis <= d)
     G3 dx=5000 dy=5000  -> never optical (PCR)
     G4 different tile   -> never optical (PCR)
   plus 20 unique singleton pairs at distinct positions.
   Expected duplicate PAIRS (any -d): 4 ; optical pairs: -d0:0 ; -d100:1 ; -d2500:2
2. synth_multilib.bam : 2 read groups / 2 libraries (RG1/LibA, RG2/LibB). 30 pairs at identical positions,
   one in each library (different molecules). Expect: default markdup marks 30 pairs (wrongly over-marks);
   --use-read-groups marks 0; Picard (library aware) marks 0.
"""
import pysam, random
random.seed(7)
D = "/mnt/openscience/audits/bio-duplicate-handling/run/data"
ref_len = 40001
def header(rgs):
    h = {"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "chr22", "LN": ref_len}],
         "RG": rgs}
    return pysam.AlignmentHeader.from_dict(h)
def mk_pair(h, name, pos1, pos2, rg, seq_seed):
    rnd = random.Random(seq_seed)
    L = 100
    def rec(nm, flag, pos, mpos, tlen, rev):
        a = pysam.AlignedSegment(h)
        a.query_name = nm; a.flag = flag; a.reference_id = 0; a.reference_start = pos
        a.mapping_quality = 60; a.cigartuples = [(0, L)]
        a.query_sequence = "".join(rnd.choice("ACGT") for _ in range(L))
        a.query_qualities = pysam.qualitystring_to_array("I" * L)
        a.next_reference_id = 0; a.next_reference_start = mpos; a.template_length = tlen
        a.set_tag("RG", rg)
        return a
    tl = pos2 + L - pos1
    r1 = rec(name, 99, pos1, pos2, tl, False)
    r2 = rec(name, 147, pos2, pos1, -tl, True)
    return [r1, r2]
def write(path, h, recs):
    recs.sort(key=lambda a: (a.reference_start, a.query_name))
    with pysam.AlignmentFile(path, "wb", header=h) as o:
        for a in recs: o.write(a)
    pysam.index(path)

# ---- 1. optical
h = header([{"ID": "rg1", "LB": "libA", "SM": "s", "PL": "ILLUMINA"}])
recs = []
def nm(tile, x, y): return f"A00001:10:HXXXXDSXX:1:{tile}:{x}:{y}"
def pair_seq(seed_group): return seed_group
base = 1000
groups = [("G1", (1101, 5000, 5000), (1101, 5050, 5050)),
          ("G2", (1101, 8000, 8000), (1101, 9000, 9000)),
          ("G3", (1101, 2000, 2000), (1101, 7000, 7000)),
          ("G4", (1101, 3000, 3000), (1102, 3000, 3000))]
for gi, (g, a, b) in enumerate(groups):
    p1, p2 = base + gi * 500, base + gi * 500 + 150
    # both pairs identical alignments; same sequence seed so they are true duplicates
    recs += mk_pair(h, nm(*a), p1, p2, "rg1", 100 + gi)
    recs += mk_pair(h, nm(*b), p1, p2, "rg1", 100 + gi)
for i in range(20):
    p1 = 5000 + i * 300
    recs += mk_pair(h, nm(1101, 100 + i * 37, 200 + i * 53), p1, p1 + 200, "rg1", 500 + i)
write(f"{D}/synth_optical.bam", h, recs)

# ---- 2. multi-library
h = header([{"ID": "rg1", "LB": "libA", "SM": "s", "PL": "ILLUMINA"},
            {"ID": "rg2", "LB": "libB", "SM": "s", "PL": "ILLUMINA"}])
recs = []
for i in range(30):
    p1 = 2000 + i * 400
    recs += mk_pair(h, f"A00001:10:FC1:1:1101:{1000+i}:{2000+i}", p1, p1 + 180, "rg1", 900 + i)
    recs += mk_pair(h, f"B00001:11:FC2:2:1101:{3000+i}:{4000+i}", p1, p1 + 180, "rg2", 900 + i)
write(f"{D}/synth_multilib.bam", h, recs)
print("wrote synth_optical.bam (expected dup pairs 4) and synth_multilib.bam (60 pairs)")
