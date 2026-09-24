#!/usr/bin/env python3
"""NEW planted-truth data written by the RE-AUDITOR (not the pre-fix auditor, not the fixer). Everything is SYNTHETIC.

Writes data/new.fa(.fai), data/new.bam(.bai), data/new_truth.json.
Reference: contig nA (1500 bp, seed 7; soft-masked lowercase 901-1000 and 1201-1250; N at 800-805) and a contig whose name
contains colons, 'HLA-A*01:01:01:01' (300 bp).  Read design (1-based, all positions are from THIS design, hand-derived):

 E1  nA:81   30M2D20M   fwd x3, rev x3 + 4 plain 50M (2 fwd/2 rev)       deleted ref 111-112 -> '-2xx' after 110
 E2  nA:401  20M3I27M (ACG) fwd x2 rev x2; 20M1I5M2I15M (T, GG) fwd x2; 4 plain -> '+3ACG' after 420, '+1T' after 420, '+2GG' after 425
 E3  nA:501  50M reads with MAPQ 19 x3, 20 x3, 21 x3, 0 x2, 255 x2, 100 x1   (-q 20 boundary; '^~' cap)
 E4  nA:601  50M; alt base at 620 with baseQ 12 x3, 13 x3, 14 x3, 93 x2 ; 4 ref reads Q40   (-Q 13 boundary)
 E5  nA:701  6 proper pairs, R1 701-750 (99), R2 721-770 (147): pairs 0-2 both alt @730 Q40/Q40, pairs 3-5 R1 ref Q40 / R2 alt Q30
 E6  nA:781  N in the reference at 800-805 (6 reads) + 3 reads with a read base N at 790 (2 at Q2, 1 at Q40)
 E7  nA:901  8 reads over the lowercase (soft-masked) reference, alt at 920 in 3
 E8  nA:1101 flags: normal x6, supplementary(2048) x2, DUP x2, paired-not-proper(65) x2, mate-unmapped(73) x2, proper(99) x2
 E9  nA:1301 3S44M3S x3 and 5H45M x3 (clips never in the pileup)
 E10 nA:1401 10M2D5M50N10M x3 (deletion then ref-skip) and 10M2I2D10M x3 (insertion directly before a deletion)
 E11 HLA-A*01:01:01:01:101  10 reads 50M, SNP at 120 in 4 (2 fwd + 2 rev)
"""
import json, os, random, subprocess, sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)
rng = random.Random(7)
COMP = {"A": "G", "C": "T", "G": "A", "T": "C"}


def rnd(n):
    return "".join(rng.choice("ACGT") for _ in range(n))


nA = list(rnd(1500))
for i in range(799, 805):          # N at 800-805 (1-based)
    nA[i] = "N"
nA = "".join(nA)
HLA = "HLA-A*01:01:01:01"
refs = {"nA": nA, HLA: rnd(300)}
# soft-mask: lowercase in the FASTA only (the sequence content for read building stays uppercase)
fa_seq = {}
low = list(nA)
for a, b in ((901, 1000), (1201, 1250)):
    for i in range(a - 1, b):
        low[i] = low[i].lower()
fa_seq["nA"] = "".join(low)
fa_seq[HLA] = refs[HLA]
with open(os.path.join(OUT, "new.fa"), "w", newline="\n") as f:
    for k, s in fa_seq.items():
        f.write(f">{k}\n")
        for i in range(0, len(s), 60):
            f.write(s[i:i + 60] + "\n")

recs = []
truth = {}


def alt(b):
    return COMP[b.upper()]


def build(ref, pos, cig, muts=None, quals=None):
    """cig: list of (op, n[, seq]). Returns (cigar string, seq, qual). muts: {1-based ref pos: base}. quals: {1-based ref pos: char}"""
    muts = muts or {}
    quals = quals or {}
    s = refs[ref]
    rp = pos
    seq, q, cs = [], [], ""
    for c in cig:
        op, n = c[0], c[1]
        cs += f"{n}{op}"
        if op == "M":
            for k in range(n):
                b = muts.get(rp, s[rp - 1])
                seq.append('A' if b == 'N' and rp not in muts else b)   # reads carry ACGT where the reference is N
                q.append(quals.get(rp, "I"))
                rp += 1
        elif op == "D" or op == "N":
            rp += n
        elif op == "I":
            ins = c[2]
            assert len(ins) == n
            seq.extend(ins)
            q.extend("I" * n)
        elif op == "S":
            sq = c[2] if len(c) > 2 else rnd(n)
            seq.extend(sq)
            q.extend("I" * n)
        elif op == "H":
            pass
    return cs, "".join(seq), "".join(q)


def add(name, flag, ref, pos, cig, mapq=60, muts=None, quals=None, rnext="*", pnext=0, tlen=0):
    cs, seq, q = build(ref, pos, cig, muts, quals)
    recs.append([name, flag, ref, pos, mapq, cs, rnext, pnext, tlen, seq, q])


# E1
for i in range(3):
    add(f"e1f{i}", 0, "nA", 81, [("M", 30), ("D", 2), ("M", 20)])
    add(f"e1r{i}", 16, "nA", 81, [("M", 30), ("D", 2), ("M", 20)])
for i in range(4):
    add(f"e1p{i}", 0 if i < 2 else 16, "nA", 81, [("M", 50)])
truth["E1"] = dict(after=110, del_seq=nA[110:112], del_fwd=3, del_rev=3, plain=4, depth_at_110=10, depth_at_111=10, star_at_111=6)
# E2
for i in range(4):
    add(f"e2a{i}", 0 if i < 2 else 16, "nA", 401, [("M", 20), ("I", 3, "ACG"), ("M", 27)])
for i in range(2):
    add(f"e2b{i}", 0, "nA", 401, [("M", 20), ("I", 1, "T"), ("M", 5), ("I", 2, "GG"), ("M", 15)])
for i in range(4):
    add(f"e2p{i}", 0, "nA", 401, [("M", 50)])
truth["E2"] = dict(after_a=420, after_b1=420, after_b2=425, depth=10)
# E3
mq = [19] * 3 + [20] * 3 + [21] * 3 + [0] * 2 + [255] * 2 + [100]
for i, m in enumerate(mq):
    add(f"e3_{i}", 0, "nA", 501, [("M", 50)], mapq=m)
truth["E3"] = dict(depth_all=14, depth_q20=9, depth_q19=12, note="q>=20: 3(20)+3(21)+2(255)+1(100)=9; q>=19 adds 3(19) -> 12")
# E4
p4 = 620
a4 = alt(nA[p4 - 1])
for i, (qc, nn) in enumerate([(chr(33 + 12), 3), (chr(33 + 13), 3), (chr(33 + 14), 3), (chr(33 + 93), 2)]):
    for j in range(nn):
        add(f"e4q{33 + ord(qc) - 33}_{j}", 0, "nA", 601, [("M", 50)], muts={p4: a4}, quals={p4: qc})
for j in range(4):
    add(f"e4ref{j}", 0, "nA", 601, [("M", 50)])
truth["E4"] = dict(pos=p4, ref=nA[p4 - 1], alt=a4, depth_Q0=15, depth_Q13=12, depth_Q14=9, alt_at_Q13=8, ref_reads=4)
# E5
p5 = 730
a5 = alt(nA[p5 - 1])
for i in range(6):
    r1 = dict(muts={p5: a5}) if i < 3 else {}
    add(f"pr{i}", 99, "nA", 701, [("M", 50)], rnext="=", pnext=721, tlen=70, **r1)
    add(f"pr{i}", 147, "nA", 721, [("M", 50)], muts={p5: a5}, quals=({p5: "?"} if i >= 3 else None), rnext="=", pnext=701, tlen=-70)
truth["E5"] = dict(pos=p5, alt=a5, depth_default=6, depth_x=12)
# E6
for i in range(6):
    add(f"e6n{i}", 0 if i % 2 == 0 else 16, "nA", 781, [("M", 50)])
for i in range(3):
    add(f"e6b{i}", 0, "nA", 781, [("M", 50)], muts={790: "N"}, quals={790: ("#" if i < 2 else "I")})
truth["E6"] = dict(n_pos="800-805", base_N_pos=790, base_N_reads=3, low_q_N=2)
# E7
p7 = 920
a7 = alt(nA[p7 - 1])
for i in range(8):
    add(f"e7_{i}", 0 if i % 2 == 0 else 16, "nA", 901, [("M", 50)], muts=({p7: a7} if i < 3 else None))
truth["E7"] = dict(pos=p7, ref=nA[p7 - 1], alt=a7, alt_reads=3, depth=8)
# E8
for i in range(6):
    add(f"e8n{i}", 0, "nA", 1101, [("M", 50)])
for i in range(2):
    add(f"e8s{i}", 2048, "nA", 1101, [("M", 50)])
for i in range(2):
    add(f"e8d{i}", 1024, "nA", 1101, [("M", 50)])
for i in range(2):
    add(f"e8o{i}", 65, "nA", 1101, [("M", 50)], rnext="=", pnext=50, tlen=0)
for i in range(2):
    add(f"e8m{i}", 73, "nA", 1101, [("M", 50)], rnext="=", pnext=1101, tlen=0)
for i in range(2):
    add(f"e8p{i}", 99, "nA", 1101, [("M", 50)], rnext="=", pnext=1201, tlen=150)
truth["E8"] = dict(default=10, A=14, ff0=12, ff0_A=16)
# E9
for i in range(3):
    add(f"e9s{i}", 0, "nA", 1301, [("S", 3, "TTT"), ("M", 44), ("S", 3, "AAA")])
    add(f"e9h{i}", 16, "nA", 1301, [("H", 5), ("M", 45)])
# E10
for i in range(3):
    add(f"e10a{i}", 0, "nA", 1401, [("M", 10), ("D", 2), ("M", 5), ("N", 50), ("M", 10)])
    add(f"e10b{i}", 16, "nA", 1401, [("M", 10), ("I", 2, "CA"), ("D", 2), ("M", 10)])
# E11
p11 = 120
a11 = alt(refs[HLA][p11 - 1])
for i in range(10):
    add(f"e11_{i}", 0 if i % 2 == 0 else 16, HLA, 101, [("M", 50)], muts=({p11: a11} if i < 4 else None))
truth["E11"] = dict(contig=HLA, pos=p11, ref=refs[HLA][p11 - 1], alt=a11, alt_reads=4, depth=10)

sam = os.path.join(OUT, "new.sam")
with open(sam, "w", newline="\n") as f:
    f.write("@HD\tVN:1.6\tSO:unsorted\n")
    for k, s in refs.items():
        f.write(f"@SQ\tSN:{k}\tLN:{len(s)}\n")
    f.write("@RG\tID:rgN\tSM:newsample\tPL:ILLUMINA\n")
    for r in recs:
        f.write("\t".join(map(str, r)) + "\tRG:Z:rgN\n")
json.dump({"truth": truth, "n_records": len(recs)}, open(os.path.join(OUT, "new_truth.json"), "w"), indent=1)
r = subprocess.run(f"cd {OUT} && samtools faidx new.fa && samtools sort -o new.bam new.sam && samtools index new.bam && rm new.sam && samtools view -c new.bam",
                   shell=True, capture_output=True, text=True, executable="/bin/bash")
print(r.stdout, r.stderr)
print("records written:", len(recs), "planted:", json.dumps(truth))
