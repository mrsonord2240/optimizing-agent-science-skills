#!/usr/bin/env python3
"""SYNTHETIC data generator for the bio-long-read-splicing audit (auditor script, seed fixed).

Makes a toy genome (chrS1) with 3 annotated genes (GA +, GC +, GB -), a reference GTF, a
"query isoform" GTF with KNOWN SQANTI3 categories, and simulated long reads for a 3 v 3
design with planted differential isoform usage in GA (GA.1 vs GA.2 = 70:30 in ctrl, 20:80 in trt).
All sequences are random; introns carry canonical GT..AG (or CT..AC on the - strand).
Outputs go to run/data/synth (labelled synthetic).
"""
import os, random, json, sys

SEED = 20260920
rnd = random.Random(SEED)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "synth")
os.makedirs(OUT, exist_ok=True)
CHR = "chrS1"
L = 26000
comp = str.maketrans("ACGTacgt", "TGCAtgca")


def rc(s):
    return s.translate(comp)[::-1]


def rseq(n):
    return "".join(rnd.choice("ACGT") for _ in range(n))


genome = list(rseq(L))

# ---- gene models (1-based inclusive genome coords) -------------------------------------
# strand + : GA exons E1..E5 ; GC exons C1..C3 ; strand - : GB exons F1..F4 (listed left->right)
GA = [(1000, 1200), (2000, 2150), (3000, 3120), (4200, 4500), (5300, 5700)]
GC = [(8000, 8300), (9000, 9200), (10500, 10900)]
GB = [(14000, 14300), (15000, 15150), (16200, 16400), (17500, 18000)]
ALT_SHIFT = 24  # novel acceptor 24 nt upstream of GA E3 start (inside intron 2)


def plant_introns(exons, strand):
    for (a, b), (c, d) in zip(exons[:-1], exons[1:]):
        i0, i1 = b + 1, c - 1  # intron 1-based
        if strand == "+":
            genome[i0 - 1:i0 + 1] = list("GT")
            genome[i1 - 2:i1] = list("AG")
        else:
            genome[i0 - 1:i0 + 1] = list("CT")
            genome[i1 - 2:i1] = list("AC")


plant_introns(GA, "+")
plant_introns(GC, "+")
plant_introns(GB, "-")
# novel acceptor inside GA intron 2 (between E2 end 2150 and E3 start 3000): AG ending at 3000-ALT_SHIFT-1
alt_acc_end = GA[2][0] - 1 - ALT_SHIFT  # last intron base of the novel acceptor 'AG'
genome[alt_acc_end - 2:alt_acc_end] = list("AG")
alt_e3 = (alt_acc_end + 1, GA[2][1])
G = "".join(genome)
with open(os.path.join(OUT, "chrS1.fa"), "w") as f:
    f.write(">%s\n" % CHR)
    for i in range(0, len(G), 60):
        f.write(G[i:i + 60] + "\n")


def tx_seq(exons, strand):
    s = "".join(G[a - 1:b] for a, b in exons)
    return s if strand == "+" else rc(s)


# ---- reference annotation --------------------------------------------------------------
ref = {
    "GA.1": ("GA", "+", GA),                                   # full
    "GA.2": ("GA", "+", [GA[0], GA[1], GA[3], GA[4]]),         # E3 skipped (annotated)
    "GC.1": ("GC", "+", GC),
    "GB.1": ("GB", "-", GB),
}


def gtf_lines(models, source="synth"):
    out = []
    for tid, (gid, strand, exons) in models.items():
        s, e = exons[0][0], exons[-1][1]
        out.append('%s\t%s\ttranscript\t%d\t%d\t.\t%s\t.\tgene_id "%s"; transcript_id "%s";' % (CHR, source, s, e, strand, gid, tid))
        ex = exons if strand == "+" else exons[::-1]
        for n, (a, b) in enumerate(ex, 1):
            out.append('%s\t%s\texon\t%d\t%d\t.\t%s\t.\tgene_id "%s"; transcript_id "%s"; exon_number "%d";' % (CHR, source, a, b, strand, gid, tid, n))
    return out


with open(os.path.join(OUT, "ref.gtf"), "w") as f:
    f.write("\n".join(sorted(gtf_lines(ref), key=lambda x: (int(x.split("\t")[3]), x))) + "\n")
# also with gene features + transcript features for bambu/isoquant --complete_genedb
with open(os.path.join(OUT, "ref_genes.gtf"), "w") as f:
    rows = []
    for gid, exs, st in (("GA", GA, "+"), ("GC", GC, "+"), ("GB", GB, "-")):
        rows.append((exs[0][0], '%s\tsynth\tgene\t%d\t%d\t.\t%s\t.\tgene_id "%s";' % (CHR, exs[0][0], exs[-1][1], st, gid)))
    for ln in gtf_lines(ref):
        rows.append((int(ln.split("\t")[3]), ln))
    rows.sort(key=lambda x: (x[0], 0 if "\tgene\t" in x[1] else 1))
    f.write("\n".join(r[1] for r in rows) + "\n")

# ---- query isoforms with KNOWN SQANTI3 categories --------------------------------------
GA_E1_E2_RI = [(GA[0][0], GA[1][1])] + GA[2:]  # intron 1 retained (E1+I1+E2 merged)
query = {
    "Q01_GA1_exact": ("QA", "+", GA, "full-splice_match"),
    "Q02_GB1_exact": ("QB", "-", GB, "full-splice_match"),
    "Q03_GA_5trunc": ("QA", "+", [(3050, 3120)] + GA[3:], "incomplete-splice_match"),   # E3 partial + E4 + E5 : subset of GA.1 junctions
    "Q04_GA_skipE2": ("QA", "+", [GA[0], GA[2], GA[3], GA[4]], "novel_in_catalog"),     # known donor E1 -> known acceptor E3
    "Q05_GA_altAcc": ("QA", "+", [GA[0], GA[1], alt_e3, GA[3], GA[4]], "novel_not_in_catalog"),  # novel splice site
    "Q06_GA_retI1": ("QA", "+", GA_E1_E2_RI, "novel_in_catalog"),                       # intron retention (SQANTI: NIC)
    "Q07_GC_intron": ("QC", "+", [(8500, 8700)], "genic"),                              # mono-exon, exon lies in GC intron -> genic_intron
    "Q08_inter": ("QI", "+", [(21000, 21200), (21800, 22100)], "intergenic"),
    "Q09_GC_antisense": ("QX", "-", [(8100, 8250), (9020, 9150)], "antisense"),          # opposite strand across GC exon1/intron
    "Q10_GA_FSM_2": ("QA", "+", [GA[0], GA[1], GA[3], GA[4]], "full-splice_match"),      # = GA.2 (annotated)
}
# make intergenic + antisense introns canonical so they are not confounded by non-canonical flags
for (a, b), (c, d) in [((21000, 21200), (21800, 22100))]:
    genome[b:b + 2] = list("GT"); genome[c - 3:c - 1] = list("AG")
for (a, b), (c, d) in [((8100, 8250), (9020, 9150))]:
    genome[b:b + 2] = list("CT"); genome[c - 3:c - 1] = list("AC")
G = "".join(genome)
with open(os.path.join(OUT, "chrS1.fa"), "w") as f:
    f.write(">%s\n" % CHR)
    for i in range(0, len(G), 60):
        f.write(G[i:i + 60] + "\n")
with open(os.path.join(OUT, "query_isoforms.gtf"), "w") as f:
    lines = []
    for tid, (gid, strand, exons, cat) in query.items():
        lines += gtf_lines({tid: (gid, strand, exons)}, "query")
    f.write("\n".join(lines) + "\n")
with open(os.path.join(OUT, "query_truth.tsv"), "w") as f:
    f.write("isoform\texpected_category\n")
    for tid, (_, _, _, cat) in query.items():
        f.write("%s\t%s\n" % (tid, cat))

# ---- transcripts to sample reads from --------------------------------------------------
tx = {
    "GA.1": (GA, "+"),
    "GA.2": ([GA[0], GA[1], GA[3], GA[4]], "+"),
    "GA.N1": ([GA[0], GA[2], GA[3], GA[4]], "+"),        # novel skipE2 (query Q04)
    "GA.N2": ([GA[0], GA[1], alt_e3, GA[3], GA[4]], "+"),  # novel alt acceptor (Q05)
    "GC.1": (GC, "+"),
    "GB.1": (GB, "-"),
    "GB.N1": ([GB[0], GB[2], GB[3]], "-"),               # novel GB skip of F2
}
with open(os.path.join(OUT, "read_tx.gtf"), "w") as f:
    m = {t: (t.split(".")[0], s, e) for t, (e, s) in tx.items()}
    f.write("\n".join(gtf_lines(m, "truth")) + "\n")


def counts_for(group):
    """planted isoform read counts per sample (mean); replicated with +-8% noise"""
    if group == "ctrl":
        ga1, ga2 = 175, 75
    else:
        ga1, ga2 = 50, 200
    return {"GA.1": ga1, "GA.2": ga2, "GA.N1": 25, "GA.N2": 20, "GC.1": 90, "GB.1": 120, "GB.N1": 60}


def mutate(seq, sub, ins, dele):
    out = []
    for ch in seq:
        r = rnd.random()
        if r < dele:
            continue
        if r < dele + sub:
            out.append(rnd.choice([c for c in "ACGT" if c != ch]))
        else:
            out.append(ch)
        if rnd.random() < ins:
            out.append(rnd.choice("ACGT"))
    return "".join(out)


def simulate(sample, group, profile, stranded, fq_path, truth_rows, scale=1.0):
    prof = {"hifi": (0.0004, 0.0002, 0.0002), "ont": (0.02, 0.008, 0.012)}[profile]
    cnts = counts_for(group)
    with open(fq_path, "w") as f:
        n = 0
        for t, c in cnts.items():
            c = int(round(c * scale * rnd.uniform(0.92, 1.08)))
            exons, strand = tx[t]
            full = tx_seq(exons, strand)
            for _ in range(c):
                s = full
                # 5' truncation (fragmentation): 30% of reads lose up to 250 nt
                if rnd.random() < 0.3 and len(s) > 500:
                    s = s[rnd.randint(1, 250):]
                s = s + "A" * rnd.randint(10, 25)  # polyA tail
                s = mutate(s, *prof)
                if not stranded and rnd.random() < 0.5:
                    s = rc(s)
                n += 1
                name = "%s_%s_%d" % (sample, t.replace(".", ""), n)
                q = ("I" if profile == "hifi" else "5") * len(s)
                f.write("@%s\n%s\n+\n%s\n" % (name, s, q))
            truth_rows.append((sample, t, c))


truth = []
design = [("ctrl1", "ctrl"), ("ctrl2", "ctrl"), ("ctrl3", "ctrl"), ("trt1", "trt"), ("trt2", "trt"), ("trt3", "trt")]
for prof, stranded, tag in (("hifi", True, "hifi"), ("ont", False, "ontunstr"), ("ont", True, "ontstr")):
    d = os.path.join(OUT, tag)
    os.makedirs(d, exist_ok=True)
    rows = []
    for s, g in design:
        simulate(s, g, prof, stranded, os.path.join(d, s + ".fastq"), rows)
    with open(os.path.join(d, "truth_counts.tsv"), "w") as f:
        f.write("sample\ttranscript\tn_reads\n")
        for r in rows:
            f.write("%s\t%s\t%d\n" % r)
json.dump({"seed": SEED, "genome": CHR, "length": L, "GA": GA, "GC": GC, "GB": GB, "alt_e3": alt_e3, "synthetic": True},
          open(os.path.join(OUT, "synth_meta.json"), "w"), indent=1)
print("synthetic data written to", OUT)
