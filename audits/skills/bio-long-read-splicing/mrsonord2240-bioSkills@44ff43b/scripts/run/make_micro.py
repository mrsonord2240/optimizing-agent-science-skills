#!/usr/bin/env python3
"""SYNTHETIC microexon test data (separate seed so make_synth.py output is untouched).
Gene GM (+ strand): D1 [1001,1300], MICRO (10 nt) [1801,1810], D3 [2401,2700], D4 [3301,3600].
Isoform M.inc = D1-MICRO-D3-D4 (150 reads), M.skip = D1-D3-D4 (150 reads). Reads: HiFi-like (0.06% err) and ONT-like (2% sub, 0.8% ins, 1.2% del), sense orientation.
Truth: fraction of M.inc reads whose alignment must carry the 2 junctions around the microexon.
"""
import os, random
rnd = random.Random(777)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "synth_micro")
os.makedirs(OUT, exist_ok=True)
comp = str.maketrans("ACGT", "TGCA")
L = 4500
g = [rnd.choice("ACGT") for _ in range(L)]
ex_inc = [(1001, 1300), (1801, 1810), (2401, 2700), (3301, 3600)]
for (a, b), (c, d) in zip(ex_inc[:-1], ex_inc[1:]):
    g[b:b + 2] = list("GT"); g[c - 3:c - 1] = list("AG")
G = "".join(g)
open(OUT + "/chrM.fa", "w").write(">chrM\n" + "\n".join(G[i:i + 60] for i in range(0, L, 60)) + "\n")
ex_skip = [ex_inc[0], ex_inc[2], ex_inc[3]]


def gtf(tid, ex):
    o = ['chrM\tsynth\ttranscript\t%d\t%d\t.\t+\t.\tgene_id "GM"; transcript_id "%s";' % (ex[0][0], ex[-1][1], tid)]
    for n, (a, b) in enumerate(ex, 1):
        o.append('chrM\tsynth\texon\t%d\t%d\t.\t+\t.\tgene_id "GM"; transcript_id "%s"; exon_number "%d";' % (a, b, tid, n))
    return o


# annotation contains BOTH isoforms (so --junc-bed / annotation-guided mode can know the microexon)
open(OUT + "/ref.gtf", "w").write("\n".join(gtf("M.inc", ex_inc) + gtf("M.skip", ex_skip)) + "\n")
# BED12 of the annotated transcripts for minimap2 --junc-bed
with open(OUT + "/ref.bed12", "w") as f:
    for tid, ex in (("M.inc", ex_inc), ("M.skip", ex_skip)):
        s, e = ex[0][0] - 1, ex[-1][1]
        sizes = ",".join(str(b - a + 1) for a, b in ex) + ","
        starts = ",".join(str(a - 1 - s) for a, b in ex) + ","
        f.write("chrM\t%d\t%d\t%s\t0\t+\t%d\t%d\t0\t%d\t%s\t%s\n" % (s, e, tid, s, e, len(ex), sizes, starts))


def mutate(s, sub, ins, dele):
    o = []
    for ch in s:
        r = rnd.random()
        if r < dele:
            continue
        o.append(rnd.choice([c for c in "ACGT" if c != ch]) if r < dele + sub else ch)
        if rnd.random() < ins:
            o.append(rnd.choice("ACGT"))
    return "".join(o)


for tag, prof in (("hifi", (0.0004, 0.0001, 0.0001)), ("ont", (0.02, 0.008, 0.012))):
    with open(OUT + "/%s.fastq" % tag, "w") as f:
        n = 0
        for tid, ex in (("Minc", ex_inc), ("Mskip", ex_skip)):
            for _ in range(150):
                s = "".join(G[a - 1:b] for a, b in ex)
                s = mutate(s, *prof)
                n += 1
                f.write("@r%d_%s_%d\n%s\n+\n%s\n" % (n, tid, n, s, "I" * len(s)))
print("micro data ->", OUT)
