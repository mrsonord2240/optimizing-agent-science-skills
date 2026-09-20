"""SYNTHETIC planted duplex-UMI paired-end BAM (auditor's own truth). Written to argv[1] (unsorted; RX dash-joined 'a-b' like the real nf-core UMI BAM).
  S1: 30 duplex molecules. Each: 3 top-strand copies (flags 99/147, RX 'a-b') + 2 bottom-strand copies (flags 83/163, RX 'b-a').
      In each molecule ONE top copy carries a 1-base error in its first UMI (a').
  S2: 20 'collision' molecules: 10 coordinates, each with 2 different molecules (UMIs differ in >= 3 bases), 3 top-strand copies each.
  UMIs across molecules differ by >= 3 bases (so nothing merges except the planted 1-base errors).
Truth (pairs):  total 210 pairs = 420 reads
  strand-aware UMI families ......... 30*2 + 20 = 80 pairs          (umi_tools directional / fgbio adjacency / Picard UmiAware)
  same, exact-match UMI ............. 80 + 30 (error copies stay unique) = 110 pairs   (umi_tools unique, samtools --barcode-tag RX)
  duplex molecules (paired strategy). 30 + 20 = 50 MI groups (/A /B)
"""
import pysam, random, json, sys
out = sys.argv[1]
rnd = random.Random(9)
L = 100
h = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "unsorted"}, "SQ": [{"SN": "chr22", "LN": 40001}],
                                     "RG": [{"ID": "A", "LB": "lib1", "SM": "s", "PL": "ILLUMINA"}]})
def seq(n): return "".join(rnd.choice("ACGT") for _ in range(n))
used = []
def umi():
    while True:
        u = seq(8)
        if all(sum(x != y for x, y in zip(u, v)) >= 3 for v in used):
            used.append(u); return u
def mut(u):
    i = rnd.randrange(8); c = rnd.choice([b for b in "ACGT" if b != u[i]])
    return u[:i] + c + u[i + 1:]
recs = []
def add_pair(name, start, insert, top, rx, sl, sr):
    end = start + insert                       # right read occupies [end-L, end)
    lpos, rpos = start, end - L
    tlen = insert
    fl_left, fl_right = (99, 147) if top else (163, 83)
    for fl, pos, mpos, tl, s in ((fl_left, lpos, rpos, tlen, sl), (fl_right, rpos, lpos, -tlen, sr)):
        a = pysam.AlignedSegment(h)
        a.query_name = name; a.flag = fl; a.reference_id = 0; a.reference_start = pos; a.mapping_quality = 60
        a.cigartuples = [(0, L)]; a.query_sequence = s; a.query_qualities = pysam.qualitystring_to_array("I" * L)
        a.next_reference_id = 0; a.next_reference_start = mpos; a.template_length = tl
        a.set_tag("RG", "A"); a.set_tag("RX", rx); recs.append(a)
pos = 1000
fam_strand = fam_exact = duplex = 0
for m in range(30):
    pos += 500; insert = 150 + (m % 11)
    a, b = umi(), umi(); sl, sr = seq(L), seq(L)
    for k in range(3):
        rx = (mut(a) if k == 2 else a) + "-" + b
        add_pair(f"S1m{m}t{k}", pos, insert, True, rx, sl, sr)
    for k in range(2):
        add_pair(f"S1m{m}b{k}", pos, insert, False, b + "-" + a, sl, sr)
    fam_strand += 2; fam_exact += 3; duplex += 1     # exact: top (a-b), top error (a'-b), bottom (b-a) ; strand-aware: 2
for c in range(10):
    pos += 500; insert = 155 + c
    for j in range(2):
        a, b = umi(), umi(); sl, sr = seq(L), seq(L)
        for k in range(3):
            add_pair(f"S2c{c}m{j}t{k}", pos, insert, True, a + "-" + b, sl, sr)
        fam_strand += 1; fam_exact += 1; duplex += 1
recs.sort(key=lambda r: r.query_name)             # deliberately name-ordered/unsorted like the real UMI BAM
with pysam.AlignmentFile(out, "wb", header=h) as o:
    for r in recs: o.write(r)
t = {"pairs": len(recs) // 2, "records": len(recs), "families_strand_aware": fam_strand, "families_exact_umi": fam_exact, "duplex_molecules": duplex}
print("wrote", out, t)
json.dump(t, open(out + ".truth.json", "w"))
