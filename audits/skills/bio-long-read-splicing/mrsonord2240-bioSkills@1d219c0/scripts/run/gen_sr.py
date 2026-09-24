#!/usr/bin/env python3
"""SYNTHETIC single-end 100-nt Illumina-like reads (0.2% substitutions) from the planted truth transcripts (ALL isoforms incl. the two novel ones), sample ctrl1 proportions,
~15 reads per long read, both orientations. Used only for IsoQuant --illumina_bam. Output data/plant/sr_ctrl1.fastq"""
import random, os, re
rnd = random.Random(99)
HERE = os.path.dirname(os.path.abspath(__file__)); D = HERE + "/data/plant"
comp = str.maketrans("ACGT", "TGCA"); rc = lambda s: s.translate(comp)[::-1]
g = "".join(l.strip() for l in open(D + "/chrQ.fa") if not l.startswith(">"))
ex = {}; st = {}
for ln in open(D + "/truth.gtf"):
    f = ln.split("\t")
    if len(f) > 8 and f[2] == "exon":
        t = re.search(r'transcript_id "([^"]+)"', f[8]).group(1); ex.setdefault(t, []).append((int(f[3]), int(f[4]))); st[t] = f[6]
cnt = {}
for ln in list(open(D + "/hifi/truth_counts.tsv"))[1:]:
    p, s, t, n = ln.split("\t")
    if s == "ctrl1": cnt[t] = int(n)
with open(D + "/sr_ctrl1.fastq", "w") as fh:
    n = 0
    for t, c in cnt.items():
        seq = "".join(g[a - 1:b] for a, b in sorted(ex[t]))
        if st[t] == "-": seq = rc(seq)
        for _ in range(c * 15):
            if len(seq) < 110: continue
            p = rnd.randint(0, len(seq) - 100); r = list(seq[p:p + 100])
            for i in range(100):
                if rnd.random() < 0.002: r[i] = rnd.choice("ACGT")
            r = "".join(r)
            if rnd.random() < 0.5: r = rc(r)
            n += 1; fh.write("@sr%d_%s\n%s\n+\n%s\n" % (n, t, r, "I" * 100))
print("short reads:", n)
