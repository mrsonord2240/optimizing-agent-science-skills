#!/usr/bin/env python3
"""RE-AUDIT SYNTHETIC microexon set (auditor's own, seed 4242; NOT the fixer's chrM/10-nt set).

Contig chrU: three genes, each  D1 - MICRO - D3 - D4  (inclusion 'inc') versus D1 - D3 - D4 ('skip'):
  MX1 (+ strand) 7-nt microexon, MX2 (- strand) 12-nt microexon, MX3 (+ strand) 24-nt microexon.
200 inclusion + 200 skipping reads per gene per platform, full-length (no truncation), 3' polyA 10-25 nt.
Platforms: hifi (oriented, 0.08% err), ontunstr (ONT cDNA, 50% reverse-complemented, 2% sub 0.8% ins 1.2% del), drna (oriented, 3.5/1.2/2.5).
Annotation variants: ref_full.gtf (both isoforms), ref_noexon.gtf (skip isoform only), sj_out.tab (STAR SJ.out.tab layout, truth junctions of both isoforms).
"""
import os, random, sys
import numpy as np
# usage: gen_micro.py                      -> data/micro      (sizes 7,12,24; seed 4242)   [the main set]
#        gen_micro.py micro_scan 4,5,6,8,10,15,18,21 4343   -> data/micro_scan (size scan; strands alternate + - +)
NAME = sys.argv[1] if len(sys.argv) > 1 else "micro"
SIZES = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [7, 12, 24]
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 4242
rnd = random.Random(SEED); nrng = np.random.default_rng(SEED)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", NAME); os.makedirs(OUT, exist_ok=True)
CHR = "chrU"
comp = str.maketrans("ACGTacgt", "TGCAtgca"); rc = lambda s: s.translate(comp)[::-1]
G = [rnd.choice("ACGT") for _ in range(2000)]
genes = {}
def place(gid, strand, mlen):
    x = len(G) + 1
    d1 = (x, x + 259); m = (d1[1] + rnd.randint(450, 700), 0); m = (m[0], m[0] + mlen - 1)
    d3 = (m[1] + rnd.randint(450, 700), 0); d3 = (d3[0], d3[0] + 219)
    d4 = (d3[1] + rnd.randint(450, 700), 0); d4 = (d4[0], d4[0] + 239)
    end = d4[1] + 1
    G.extend(rnd.choice("ACGT") for _ in range(end - len(G) + 1))
    ex = [d1, m, d3, d4]
    for (a, b), (c, d) in zip(ex[:-1], ex[1:]):
        i0, i1 = b + 1, c - 1
        if strand == "+":
            G[i0 - 1:i0 + 1] = list("GT"); G[i1 - 2:i1] = list("AG")
        else:
            G[i0 - 1:i0 + 1] = list("CT"); G[i1 - 2:i1] = list("AC")
    G.extend(rnd.choice("ACGT") for _ in range(2500))
    genes[gid] = (strand, ex)
STR = ["+", "-", "+"] if NAME == "micro" else ["+", "-"] * 10
for i, L in enumerate(SIZES, 1):
    place("MX%d" % i, STR[i - 1], L)
genome = "".join(G)
open(OUT + "/chrU.fa", "w").write(">%s\n" % CHR + "\n".join(genome[i:i + 60] for i in range(0, len(genome), 60)) + "\n")

iso = {}
for gid, (st, ex) in genes.items():
    iso[gid + "inc"] = (gid, st, ex); iso[gid + "skip"] = (gid, st, [ex[0], ex[2], ex[3]])

def rows(tid, gid, st, ex):
    s, e = ex[0][0], ex[-1][1]
    o = ['%s\tsynth\ttranscript\t%d\t%d\t.\t%s\t.\tgene_id "%s"; transcript_id "%s";' % (CHR, s, e, st, gid, tid)]
    for n, (a, b) in enumerate(ex if st == "+" else ex[::-1], 1):
        o.append('%s\tsynth\texon\t%d\t%d\t.\t%s\t.\tgene_id "%s"; transcript_id "%s"; exon_number %d;' % (CHR, a, b, st, gid, tid, n))
    return o
with open(OUT + "/ref_full.gtf", "w") as f:
    for t, (g, st, ex) in iso.items():
        f.write("\n".join(rows(t, g, st, ex)) + "\n")
with open(OUT + "/ref_noexon.gtf", "w") as f:
    for t, (g, st, ex) in iso.items():
        if t.endswith("skip"):
            f.write("\n".join(rows(t, g, st, ex)) + "\n")
with open(OUT + "/truth_chains.tsv", "w") as f:
    f.write("tx\tgene\tstrand\tannotated\tchain\tmicro_idx\n")
    for t, (g, st, ex) in iso.items():
        ch = ";".join("%d-%d" % (ex[i][1], ex[i + 1][0] - 1) for i in range(len(ex) - 1))
        f.write("%s\t%s\t%s\t1\t%s\t%s\n" % (t, g, st, ch, "0,1" if t.endswith("inc") else ""))
# STAR SJ.out.tab layout: chr, intron first (1-based), intron last (1-based), strand 0/1/2, motif, annotated, unique, multi, overhang
sj = set()
for t, (g, st, ex) in iso.items():
    for i in range(len(ex) - 1):
        sj.add((ex[i][1] + 1, ex[i + 1][0] - 1, 1 if st == "+" else 2, 1 if st == "+" else 2))
with open(OUT + "/SJ.out.tab", "w") as f:
    for a, b, s, m in sorted(sj):
        f.write("%s\t%d\t%d\t%d\t%d\t0\t50\t0\t40\n" % (CHR, a, b, s, m))

def mutate(seq, sub, ins, dele):
    L = len(seq); s = list(seq)
    for p in nrng.integers(0, L, nrng.poisson(L * sub)):
        s[p] = rnd.choice([c for c in "ACGT" if c != s[p]])
    dels = set(nrng.integers(0, L, nrng.poisson(L * dele)).tolist()); inss = {p: rnd.choice("ACGT") for p in nrng.integers(0, L, nrng.poisson(L * ins)).tolist()}
    o = []
    for i, ch in enumerate(s):
        if i not in dels: o.append(ch)
        if i in inss: o.append(inss[i])
    return "".join(o)
PROF = {"hifi": (0.0004, 0.0002, 0.0002), "ontunstr": (0.02, 0.008, 0.012), "drna": (0.035, 0.012, 0.025)}
for plat, prof in PROF.items():
    with open(OUT + "/%s.fastq" % plat, "w") as f:
        n = 0
        for t, (g, st, ex) in iso.items():
            for _ in range(200):
                s = "".join(genome[a - 1:b] for a, b in ex)
                if st == "-": s = rc(s)
                s = mutate(s + "A" * rnd.randint(10, 25), *prof)
                if plat == "ontunstr" and rnd.random() < 0.5: s = rc(s)
                n += 1
                f.write("@x_%s_%d\n%s\n+\n%s\n" % (t, n, s, ("I" if plat == "hifi" else "5") * len(s)))
print("micro set ->", OUT, {g: ex[1] for g, (st, ex) in genes.items()})
