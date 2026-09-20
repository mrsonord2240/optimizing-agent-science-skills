"""SYNTHETIC planted-duplicate BAM #2 (auditor's own truth, not the fixer's, not the env's planted_dups.bam).
Exercises what a real library does and the first planted BAM does not: 5' soft clips, reverse-strand single-end reads whose 5' end is the
alignment END, mixed paired + single-end records in one file, and near-miss (off-by-one) non-duplicates.
Truth (flagged reads under any correct 5'-unclipped-position marker, one read group / one library):
  A 20 groups x 3 identical FR pairs                      -> 2 dup pairs each = 80 reads
  B 15 groups x 2 pairs, copy 2 has left read 5S95M (pos+5, same unclipped 5') -> 1 dup pair each = 30 reads
  C 15 groups x 2 pairs, copy 2 starts 1 base later (NOT duplicates)            -> 0
  E1 10 groups x 3 single-end forward reads, same start   -> 2 dup reads each = 20
  E2 10 groups x 2 single-end REVERSE reads, copy 2 has 6S at the 3' end (same unclipped end) -> 1 dup read each = 10
  F 100 unique pairs                                       -> 0
  TRUTH TOTAL = 140 flagged reads (70 of them in pairs... printed by the script)
"""
import pysam, random, json, sys
out = sys.argv[1]
rnd = random.Random(20260920)
L = 100
hd = {"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "chr22", "LN": 40001}],
      "RG": [{"ID": "rg1", "LB": "lib1", "SM": "s", "PL": "ILLUMINA"}]}
h = pysam.AlignmentHeader.from_dict(hd)
recs = []
def seq(n): return "".join(rnd.choice("ACGT") for _ in range(n))
def rec(name, flag, pos, cigar, mpos=-1, tlen=0, s=None):
    a = pysam.AlignedSegment(h)
    a.query_name = name; a.flag = flag; a.reference_id = 0; a.reference_start = pos
    a.mapping_quality = 60; a.cigartuples = cigar
    a.query_sequence = s or seq(L); a.query_qualities = pysam.qualitystring_to_array("I" * L)
    if flag & 1:
        a.next_reference_id = 0; a.next_reference_start = mpos; a.template_length = tlen
    a.set_tag("RG", "rg1"); return a
def pair(name, p1, p2, clip5=0, clip3_right=0):
    """FR pair: left read forward at p1 (optionally clip5 soft-clipped bases, start shifted), right read reverse ending at p2+L"""
    s1, s2 = seq(L), seq(L)
    lc = [(4, clip5), (0, L - clip5)] if clip5 else [(0, L)]
    lpos = p1 + clip5
    tl = p2 + L - p1
    return [rec(name, 99, lpos, lc, p2, tl, s1), rec(name, 147, p2, [(0, L)], lpos, -tl, s2)]
cursor = [500]
def nxt(step=300):
    cursor[0] += step; return cursor[0]
truth = 0
for g in range(20):
    p1 = nxt(); p2 = p1 + 150; base = None
    s1, s2 = seq(L), seq(L)
    for k in range(3):
        rs = pair(f"A{g}c{k}", p1, p2)
        rs[0].query_sequence, rs[1].query_sequence = s1, s2
        recs += rs
    truth += 4
for g in range(15):
    p1 = nxt(); p2 = p1 + 160
    recs += pair(f"B{g}c0", p1, p2); recs += pair(f"B{g}c1", p1, p2, clip5=5)
    truth += 2
for g in range(15):
    p1 = nxt(); p2 = p1 + 170
    recs += pair(f"C{g}c0", p1, p2); recs += pair(f"C{g}c1", p1 + 1, p2)
for g in range(10):
    p = nxt()
    for k in range(3):
        recs.append(rec(f"E1_{g}c{k}", 0, p, [(0, L)]))
    truth += 2
for g in range(10):
    p = nxt()   # reverse read, 5' end = alignment end; copy 2 carries a 6S right clip so its aligned end is 6 bases shorter
    recs.append(rec(f"E2_{g}c0", 16, p, [(0, L)]))
    recs.append(rec(f"E2_{g}c1", 16, p, [(0, L - 6), (4, 6)]))
    truth += 1
for g in range(100):
    p1 = nxt(150); recs += pair(f"F{g}", p1, p1 + 120 + (g % 7))
recs.sort(key=lambda a: (a.reference_start, a.query_name, a.flag))
with pysam.AlignmentFile(out, "wb", header=h) as o:
    for a in recs: o.write(a)
pysam.index(out)
print("wrote", out, "records", len(recs), "TRUTH flagged reads", truth)
json.dump({"truth_flagged_reads": truth, "records": len(recs)}, open(out + ".truth.json", "w"))
