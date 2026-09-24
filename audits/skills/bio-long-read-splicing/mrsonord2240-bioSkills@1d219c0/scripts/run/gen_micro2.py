#!/usr/bin/env python3
"""RE-AUDIT #2 SYNTHETIC microexon set (second re-auditor's own generator; new seed and design, NOT the fixer's seeds 5151/6161/7171/8181 and NOT the first re-auditor's 4242/4343).

Contig chrM2 (GC ~ 0.58, different from the earlier uniform-base genomes). Each gene: E1 - MICRO - E3 - E4 with FLANKING exons of 70-140 nt
(shorter than the earlier sets) and introns of 300-900 nt; inclusion isoform 'inc' = E1,M,E3,E4 ; skipping isoform 'skip' = E1,E3,E4.
Microexon sizes 3,5,6,8,9,11,13,16,19,22,25,27 nt (12 genes; strands alternate + -), plus TWO tandem-microexon genes (T1: 6+9 nt with a 250-nt intron between;
T2: 4+12 nt) whose 'inc' isoform has both microexons and 'skip' has neither.
Reads: N_INC inclusion + N_SKIP skipping per gene and platform, first/last exon randomly trimmed (0-40%) to mimic truncation; 3' polyA 10-25 nt.
Platforms: hifi (oriented), ontunstr (ONT cDNA, 50% reverse-complemented; 2/0.8/1.2 % sub/ins/del), drna (oriented; 3.5/1.2/2.5 %).
Annotation: ref_full.gtf (both isoforms of every gene). truth_chains.tsv: intron chains (1-based-inclusive exon ends -> 0-based half-open introns as in eval_bam.py).
usage: gen_micro2.py [seed=9191] [n_per_isoform=150]
"""
import os, random, sys
import numpy as np
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 9191
NR = int(sys.argv[2]) if len(sys.argv) > 2 else 150
rnd = random.Random(SEED); nrng = np.random.default_rng(SEED)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "micro2"); os.makedirs(OUT, exist_ok=True)
CHR = "chrM2"
comp = str.maketrans("ACGTacgt", "TGCAtgca"); rc = lambda s: s.translate(comp)[::-1]
rb = lambda: rnd.choices("ACGT", weights=[21, 29, 29, 21])[0]        # GC 0.58
G = [rb() for _ in range(1500)]
genes = {}
def canon(ex, strand):
    for (a, b), (c, d) in zip(ex[:-1], ex[1:]):
        i0, i1 = b + 1, c - 1
        if strand == "+":
            G[i0 - 1:i0 + 1] = list("GT"); G[i1 - 2:i1] = list("AG")
        else:
            G[i0 - 1:i0 + 1] = list("CT"); G[i1 - 2:i1] = list("AC")
def place(gid, strand, micros):
    """micros: list of microexon lengths (1 or 2) placed between E1 and the next long exon"""
    x = len(G) + 1
    ex = [(x, x + rnd.randint(70, 140) - 1)]
    for k, L in enumerate(micros):
        s = ex[-1][1] + (rnd.randint(300, 900) if k == 0 else 250)
        ex.append((s, s + L - 1))
    s = ex[-1][1] + rnd.randint(300, 900); ex.append((s, s + rnd.randint(70, 140) - 1))
    s = ex[-1][1] + rnd.randint(300, 900); ex.append((s, s + rnd.randint(70, 140) - 1))
    G.extend(rb() for _ in range(ex[-1][1] + 1 - len(G)))
    canon(ex, strand)
    G.extend(rb() for _ in range(2000))
    genes[gid] = (strand, ex, len(micros))
SIZES = [3, 5, 6, 8, 9, 11, 13, 16, 19, 22, 25, 27]
for i, L in enumerate(SIZES, 1):
    place("M%02d" % i, "+" if i % 2 else "-", [L])
place("T1", "+", [6, 9]); place("T2", "-", [4, 12])
genome = "".join(G)
open(OUT + "/chrM2.fa", "w").write(">%s\n" % CHR + "\n".join(genome[i:i + 60] for i in range(0, len(genome), 60)) + "\n")
iso = {}
for gid, (st, ex, nm) in genes.items():
    iso[gid + "inc"] = (gid, st, ex)
    iso[gid + "skip"] = (gid, st, [ex[0]] + ex[1 + nm:])
def rows(tid, gid, st, ex):
    o = ['%s\tsynth\ttranscript\t%d\t%d\t.\t%s\t.\tgene_id "%s"; transcript_id "%s";' % (CHR, ex[0][0], ex[-1][1], st, gid, tid)]
    for n, (a, b) in enumerate(ex if st == "+" else ex[::-1], 1):
        o.append('%s\tsynth\texon\t%d\t%d\t.\t%s\t.\tgene_id "%s"; transcript_id "%s"; exon_number %d;' % (CHR, a, b, st, gid, tid, n))
    return o
with open(OUT + "/ref_full.gtf", "w") as f:
    for t, (g, st, ex) in iso.items(): f.write("\n".join(rows(t, g, st, ex)) + "\n")
with open(OUT + "/truth_chains.tsv", "w") as f:
    f.write("tx\tgene\tstrand\tannotated\tchain\tmicro_len\n")
    for t, (g, st, ex) in iso.items():
        ch = ";".join("%d-%d" % (ex[i][1], ex[i + 1][0] - 1) for i in range(len(ex) - 1))
        ml = ",".join(str(b - a + 1) for a, b in genes[g][1][1:1 + genes[g][2]]) if t.endswith("inc") else ""
        f.write("%s\t%s\t%s\t1\t%s\t%s\n" % (t, g, st, ch, ml))
def mutate(seq, sub, ins, dele):
    L = len(seq); s = list(seq)
    for p in nrng.integers(0, L, nrng.poisson(L * sub)): s[p] = rnd.choice([c for c in "ACGT" if c != s[p]])
    dels = set(nrng.integers(0, L, nrng.poisson(L * dele)).tolist()); inss = {p: rnd.choice("ACGT") for p in nrng.integers(0, L, nrng.poisson(L * ins)).tolist()}
    o = []
    for i, ch in enumerate(s):
        if i not in dels: o.append(ch)
        if i in inss: o.append(inss[i])
    return "".join(o)
PROF = {"hifi": (0.0004, 0.0002, 0.0002), "ontunstr": (0.02, 0.008, 0.012), "drna": (0.035, 0.012, 0.025), "drnalow": (0.02, 0.007, 0.013)}   # drnalow = ~4% total error (last, so the other files are unchanged)
for plat, prof in PROF.items():
    with open(OUT + "/%s.fastq" % plat, "w") as f:
        n = 0
        for t, (g, st, ex) in iso.items():
            for _ in range(NR):
                ex2 = list(ex)
                a, b = ex2[0]; ex2[0] = (a + int((b - a) * rnd.uniform(0, 0.4)), b)      # trim the 5'-most genomic exon (either end of the read after strand flip)
                a, b = ex2[-1]; ex2[-1] = (a, b - int((b - a) * rnd.uniform(0, 0.4)))
                s = "".join(genome[a - 1:b] for a, b in ex2)
                if st == "-": s = rc(s)
                s = mutate(s + "A" * rnd.randint(10, 25), *prof)
                if plat == "ontunstr" and rnd.random() < 0.5: s = rc(s)
                n += 1
                f.write("@x_%s_%d\n%s\n+\n%s\n" % (t, n, s, ("I" if plat == "hifi" else "5") * len(s)))
print("micro2 set ->", OUT, {g: [b - a + 1 for a, b in ex[1:1 + nm]] for g, (st, ex, nm) in genes.items()})
