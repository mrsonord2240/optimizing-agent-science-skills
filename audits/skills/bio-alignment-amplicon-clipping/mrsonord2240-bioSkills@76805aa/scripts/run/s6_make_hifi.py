"""SYNTHETIC PacBio-HiFi-like full-length 16S amplicon data (no real HiFi BAM is available offline; the fixer never tested HiFi).
3 'rRNA operon variant' contigs (rrn1..rrn3, ~1.5 kb, random seq, seed 20260920). Amplicon = 27F .. 1492R style: forward primer
(20 nt) at the contig start, reverse primer (19 nt) at the contig end, both matching the reference (primer-derived bases carry REF).
Reads: 300 per contig, 50/50 orientation, whole amplicon, HiFi-like errors (0.10% substitutions, 0.03% indels), 5% end jitter of 1-3 bp
(within ampliconclip tolerance), 5% deep truncation (25-40 bp lost at one end: primer absent, must stay unclipped).
Outputs (run/data): hifi_ref.fa(+fai), hifi_reads.fq, hifi_primers.bed (6 col), hifi_truth.tsv. Alignment is done by s6_hifi.sh (minimap2 -ax map-hifi).
Run in the WSL env python."""
import random
R = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/data"
random.seed(20260920)
comp = str.maketrans("ACGT", "TGCA")
def rc(s): return s.translate(comp)[::-1]
contigs = {}
for i, L in enumerate([1503, 1489, 1521], 1):
    contigs[f"rrn{i}"] = "".join(random.choice("ACGT") for _ in range(L))
PF, PR = 20, 19
with open(f"{R}/hifi_ref.fa", "w") as f:
    for n, s in contigs.items():
        f.write(f">{n}\n"); [f.write(s[i:i + 70] + "\n") for i in range(0, len(s), 70)]
with open(f"{R}/hifi_primers.bed", "w") as f:
    for n, s in contigs.items():
        f.write(f"{n}\t0\t{PF}\t{n}_27F\t60\t+\n{n}\t{len(s) - PR}\t{len(s)}\t{n}_1492R\t60\t-\n")
def mutate(s):
    out = []
    for ch in s:
        r = random.random()
        if r < 0.0010: out.append(random.choice([b for b in "ACGT" if b != ch]))
        elif r < 0.0013: continue                      # deletion
        elif r < 0.0016: out.append(ch); out.append(random.choice("ACGT"))   # insertion
        else: out.append(ch)
    return "".join(out)
n = 0
with open(f"{R}/hifi_reads.fq", "w") as fq, open(f"{R}/hifi_truth.tsv", "w") as tr:
    tr.write("read\tcontig\torient\tlost5\tlost3\n")
    for c, s in contigs.items():
        for k in range(300):
            a, b = 0, len(s)                           # amplicon span retained (0-based half-open on contig)
            u = random.random(); lost5 = lost3 = 0
            if u < 0.05:                               # small jitter
                lost5 = random.randint(1, 3) if random.random() < .5 else 0; lost3 = random.randint(1, 3) if lost5 == 0 else 0
            elif u < 0.10:                             # deep truncation at one end
                if random.random() < .5: lost5 = random.randint(25, 40)
                else: lost3 = random.randint(25, 40)
            seg = mutate(s[lost5:len(s) - lost3])
            rev = random.random() < 0.5
            seq = rc(seg) if rev else seg
            # orientation rev: the read holds the reverse complement, so read 5' end = contig right end
            l5, l3 = (lost3, lost5) if rev else (lost5, lost3)
            name = f"{c}_{k:03d}"
            fq.write(f"@{name}\n{seq}\n+\n{'I' * len(seq)}\n")
            tr.write(f"{name}\t{c}\t{'-' if rev else '+'}\t{lost5}\t{lost3}\n"); n += 1
print("wrote", n, "reads")
