#!/usr/bin/env python3
"""RE-AUDIT SYNTHETIC data generator (auditor's own, seed 5150; independent of the fixer's and the first auditor's generators).

Contig chrQ (~330 kb, random sequence, canonical GT..AG / CT..AC introns), 60 genes with ids G001..G060 (no underscores):
  G001-G020  planted DTU: 2 isoforms (A full / B skips one exon), ctrl 75:25 -> trt 25:75 (half swapped)   [truth_dtu.tsv]
  G021-G054  null genes: 2 isoforms 60:40 in both groups
  G055 (+ strand) 7-nt microexon, annotated, inclusion 50%
  G056 (- strand) 12-nt microexon, annotated, inclusion 50%
  G057 novel isoform N (exon skip, NOT in annotation) 15% of reads
  G058 novel alt-5'ss isoform (30-nt donor shift, NOT in annotation) 15% of reads
  G059/G060 3-isoform null genes
Platforms (3 v 3 design, 6 samples each): hifi (oriented), ontunstr (ONT cDNA, 50% reversed), ontstr (ONT cDNA oriented; ctrl1-3 only),
drna (ONT direct RNA: oriented, higher error, heavy 5' truncation).  Read name = <sample>_<TX>_<n> (TX has no dots).
The annotation (ref.gtf) is GENCODE-like: gene/transcript/exon/CDS (valid frames)/UTR/start_codon rows, and lacks the two novel isoforms.
"""
import os, random, json, math, sys
import numpy as np

SEED = 5150
rnd = random.Random(SEED)
nrng = np.random.default_rng(SEED)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "plant")
os.makedirs(OUT, exist_ok=True)
CHR = "chrQ"
comp = str.maketrans("ACGTacgt", "TGCAtgca")
rc = lambda s: s.translate(comp)[::-1]
rseq = lambda n: "".join(rnd.choice("ACGT") for _ in range(n))

genes = {}   # gid -> dict(strand, exons(list of (a,b) 1-based, left->right, all exons of full isoform), isoforms{tid:[exon idx or explicit list]}, kind)
pos = 3000
G = []       # genome as list, extended

def add_gap(n):
    global pos
    G.extend(rseq(n)); pos += n

G.extend(rseq(3000))

def make_exons(n_ex, strand, micro=None, micro_idx=None):
    """return exon list (1-based inclusive) placed from current pos; micro = length of the microexon at exon index micro_idx"""
    global pos
    exons = []
    x = pos + 1
    for i in range(n_ex):
        if micro is not None and i == micro_idx:
            L = micro
        else:
            L = rnd.randint(90, 280)
        exons.append((x, x + L - 1))
        # intron
        il = rnd.randint(350, 900)
        x = x + L + il
    return exons

def place_gene(gid, strand, n_ex, micro=None, micro_idx=None):
    global pos
    exons = make_exons(n_ex, strand, micro, micro_idx)
    end = exons[-1][1]
    # extend genome to end
    need = end + 1 - len(G)
    G.extend(rseq(need))
    # canonical introns
    for (a, b), (c, d) in zip(exons[:-1], exons[1:]):
        i0, i1 = b + 1, c - 1
        if strand == "+":
            G[i0 - 1:i0 + 1] = list("GT"); G[i1 - 2:i1] = list("AG")
        else:
            G[i0 - 1:i0 + 1] = list("CT"); G[i1 - 2:i1] = list("AC")
    pos = end
    add_gap(rnd.randint(3000, 6000))
    return exons

GENES = []
def gene(gid, strand, n_ex, kind, micro=None, micro_idx=None):
    ex = place_gene(gid, strand, n_ex, micro, micro_idx)
    genes[gid] = dict(strand=strand, exons=ex, kind=kind)
    GENES.append(gid)
    return ex

for i in range(1, 61):
    gid = "G%03d" % i
    st = rnd.choice("+-")
    if i <= 20:
        gene(gid, st, rnd.randint(4, 6), "dtu")
    elif i <= 54:
        gene(gid, st, rnd.randint(4, 6), "null")
    elif i == 55:
        gene(gid, "+", 5, "micro7", micro=7, micro_idx=2)
    elif i == 56:
        gene(gid, "-", 5, "micro12", micro=12, micro_idx=2)
    elif i == 57:
        gene(gid, "+", 5, "novel_skip")
    elif i == 58:
        gene(gid, "-", 5, "novel_alt5")
    else:
        gene(gid, rnd.choice("+-"), 5, "null3")

# ---- isoform definitions -------------------------------------------------------------------
iso = {}   # tid -> (gid, strand, exons list, annotated?, kind)
def add_iso(tid, gid, exons, annotated=True):
    iso[tid] = (gid, genes[gid]["strand"], exons, annotated)

alt5_detail = None
for gid in GENES:
    g = genes[gid]; ex = g["exons"]; k = g["kind"]; n = len(ex)
    skip = rnd.randint(1, n - 2)            # a middle exon
    if k in ("dtu", "null"):
        add_iso(gid + "A", gid, ex); add_iso(gid + "B", gid, ex[:skip] + ex[skip + 1:])
    elif k in ("micro7", "micro12"):
        add_iso(gid + "A", gid, ex)                       # includes the microexon (index 2)
        add_iso(gid + "B", gid, ex[:2] + ex[3:])          # skips it
    elif k == "novel_skip":
        add_iso(gid + "A", gid, ex); add_iso(gid + "B", gid, ex[:2] + ex[3:])
        add_iso(gid + "N", gid, ex[:1] + ex[2:], annotated=False)   # skips exon 1 (index 1): not annotated
    elif k == "novel_alt5":
        add_iso(gid + "A", gid, ex); add_iso(gid + "B", gid, ex[:2] + ex[3:])
        # novel donor 30 nt downstream (inside intron) of exon index 1 (in transcript direction that is genome-right for +, but for - the
        # 'donor' is at the exon's LEFT edge). We shift the genomic exon boundary that faces the next exon in the READING direction.
        a, b = ex[1]
        st = g["strand"]
        if st == "+":
            nb = b + 30                          # exon end moves 30 nt into the intron; intron then starts at 1-based nb+1
            G[nb:nb + 2] = list("GT")            # donor GT (0-based indices nb, nb+1)
            new = (a, nb)
        else:
            na = a - 30                          # minus strand: the donor is the exon's LEFT edge; plus-strand intron ends 'AC'
            G[na - 3:na - 1] = list("AC")        # the two bases just left of the new exon start (1-based na-2, na-1)
            new = (na, b)
        exs = list(ex); exs[1] = new
        add_iso(gid + "N", gid, exs, annotated=False)
        alt5_detail = (gid, st, new, ex[1])
    elif k == "null3":
        add_iso(gid + "A", gid, ex); add_iso(gid + "B", gid, ex[:skip] + ex[skip + 1:])
        s2 = skip % (n - 2) + 1
        add_iso(gid + "C", gid, ex[:s2] + ex[s2 + 1:] if s2 != skip else ex[:1] + ex[2:])

genome = "".join(G)
GL = len(genome)
with open(os.path.join(OUT, "chrQ.fa"), "w") as f:
    f.write(">%s\n" % CHR)
    for i in range(0, GL, 60):
        f.write(genome[i:i + 60] + "\n")

def tx_seq(exons, strand):
    s = "".join(genome[a - 1:b] for a, b in exons)
    return s if strand == "+" else rc(s)

# ---- GTF -------------------------------------------------------------------------------------
def gtf_rows(tid, gid, strand, exons, cds=True):
    rows = []
    s, e = exons[0][0], exons[-1][1]
    rows.append((s, 1, '%s	synth	transcript	%d	%d	.	%s	.	gene_id "%s"; transcript_id "%s"; gene_type "protein_coding";' % (CHR, s, e, strand, gid, tid)))
    ex = exons if strand == "+" else exons[::-1]          # transcript order
    cum = 0
    for n, (a, b) in enumerate(ex, 1):
        rows.append((a, 2, '%s	synth	exon	%d	%d	.	%s	.	gene_id "%s"; transcript_id "%s"; exon_number %d;' % (CHR, a, b, strand, gid, tid, n)))
        if not cds:
            continue
        # GENCODE-like: 40-nt 5'UTR in the first exon and 40-nt 3'UTR in the last exon (transcript order), CDS elsewhere with valid frames
        u5 = 40 if n == 1 else 0
        u3 = 40 if n == len(ex) else 0
        if strand == "+":
            ca, cb = a + u5, b - u3
        else:
            ca, cb = a + u3, b - u5
        if cb - ca + 1 >= 3:
            frame = (3 - cum % 3) % 3
            rows.append((ca, 3, '%s	synth	CDS	%d	%d	.	%s	%d	gene_id "%s"; transcript_id "%s"; exon_number %d;' % (CHR, ca, cb, strand, frame, gid, tid, n)))
            if n == 1 or cum == 0:
                if strand == "+":
                    rows.append((ca, 5, '%s	synth	start_codon	%d	%d	.	+	0	gene_id "%s"; transcript_id "%s"; exon_number %d;' % (CHR, ca, ca + 2, gid, tid, n)))
                else:
                    rows.append((cb - 2, 5, '%s	synth	start_codon	%d	%d	.	-	0	gene_id "%s"; transcript_id "%s"; exon_number %d;' % (CHR, cb - 2, cb, gid, tid, n)))
            cum += cb - ca + 1
        if u5:
            ua, ub = (a, a + u5 - 1) if strand == "+" else (b - u5 + 1, b)
            rows.append((ua, 4, '%s	synth	UTR	%d	%d	.	%s	.	gene_id "%s"; transcript_id "%s"; exon_number %d;' % (CHR, ua, ub, strand, gid, tid, n)))
        if u3:
            ua, ub = (b - u3 + 1, b) if strand == "+" else (a, a + u3 - 1)
            rows.append((ua, 4, '%s	synth	UTR	%d	%d	.	%s	.	gene_id "%s"; transcript_id "%s"; exon_number %d;' % (CHR, ua, ub, strand, gid, tid, n)))
    return rows

def write_gtf(path, only_annotated):
    rows = []
    for gid in GENES:
        g = genes[gid]
        tids = [t for t, v in iso.items() if v[0] == gid and (v[3] or not only_annotated)]
        allex = [x for t in tids for x in iso[t][2]]
        s, e = min(a for a, b in allex), max(b for a, b in allex)
        rows.append((s, 0, '%s\tsynth\tgene\t%d\t%d\t.\t%s\t.\tgene_id "%s"; gene_type "protein_coding";' % (CHR, s, e, g["strand"], gid)))
        for t in tids:
            rows += gtf_rows(t, gid, g["strand"], iso[t][2])
    rows.sort(key=lambda r: (r[0], r[1]))
    with open(path, "w") as f:
        f.write("\n".join(r[2] for r in rows) + "\n")

write_gtf(os.path.join(OUT, "ref.gtf"), True)
write_gtf(os.path.join(OUT, "truth.gtf"), False)

# truth chain (intron tuples, 0-based half-open) per transcript
with open(os.path.join(OUT, "truth_chains.tsv"), "w") as f:
    f.write("tx\tgene\tstrand\tannotated\tchain\n")
    for t, (gid, st, ex, ann) in iso.items():
        ex = sorted(ex)
        ch = ";".join("%d-%d" % (ex[i][1], ex[i + 1][0] - 1) for i in range(len(ex) - 1))
        f.write("%s\t%s\t%s\t%d\t%s\n" % (t, gid, st, int(ann), ch))

# ---- proportions ---------------------------------------------------------------------------------
base = {gid: max(60, int(rnd.lognormvariate(math.log(130), 0.4))) for gid in GENES}
dtu_dir = {}
def props(gid, group):
    k = genes[gid]["kind"]
    if k == "dtu":
        sw = dtu_dir.setdefault(gid, rnd.random() < 0.5)
        pa_c, pa_t = (0.75, 0.25) if not sw else (0.25, 0.75)
        pa = pa_c if group == "ctrl" else pa_t
        return {gid + "A": pa, gid + "B": 1 - pa}
    if k in ("null", "micro7", "micro12"):
        pa = 0.6 if k == "null" else 0.5
        return {gid + "A": pa, gid + "B": 1 - pa}
    if k in ("novel_skip", "novel_alt5"):
        return {gid + "A": 0.45, gid + "B": 0.40, gid + "N": 0.15}
    return {gid + "A": 0.5, gid + "B": 0.3, gid + "C": 0.2}

def mutate(seq, sub, ins, dele):
    L = len(seq)
    n_sub = nrng.poisson(L * sub); n_del = nrng.poisson(L * dele); n_ins = nrng.poisson(L * ins)
    s = list(seq)
    if n_sub:
        for p in nrng.integers(0, L, n_sub):
            s[p] = rnd.choice([c for c in "ACGT" if c != s[p]]) if s[p] in "ACGT" else s[p]
    # deletions and insertions by index (apply on the list; positions from original length)
    dels = set(nrng.integers(0, L, n_del).tolist()) if n_del else set()
    inss = {}
    for p in (nrng.integers(0, L, n_ins).tolist() if n_ins else []):
        inss[p] = rnd.choice("ACGT")
    out = []
    for i, ch in enumerate(s):
        if i not in dels:
            out.append(ch)
        if i in inss:
            out.append(inss[i])
    return "".join(out)

PROF = {"hifi": (0.0004, 0.0002, 0.0002), "ontunstr": (0.02, 0.008, 0.012), "ontstr": (0.02, 0.008, 0.012), "drna": (0.035, 0.012, 0.025)}
DESIGN = [("ctrl1", "ctrl"), ("ctrl2", "ctrl"), ("ctrl3", "ctrl"), ("trt1", "trt"), ("trt2", "trt"), ("trt3", "trt")]
TRUNC = {"hifi": 0.15, "ontunstr": 0.3, "ontstr": 0.3, "drna": 0.6}
ORIENTED = {"hifi": True, "ontunstr": False, "ontstr": True, "drna": True}
seqcache = {t: tx_seq(v[2], v[1]) for t, v in iso.items()}

def simulate(platform, sample, group, fq, rows):
    sub, ins, dele = PROF[platform]
    q = "I" if platform == "hifi" else "5"
    n = 0
    with open(fq, "w") as f:
        for gid in GENES:
            tot = base[gid] * rnd.uniform(0.85, 1.15)
            p = props(gid, group)
            # per-sample jitter of the proportion (biological dispersion)
            ks = list(p)
            w = np.array([max(1e-3, p[k] + nrng.normal(0, 0.04)) for k in ks]); w /= w.sum()
            cnt = nrng.multinomial(int(tot), w)
            for tid, c in zip(ks, cnt):
                rows.append((platform, sample, tid, int(c)))
                full = seqcache[tid]
                for _ in range(int(c)):
                    s = full
                    if rnd.random() < TRUNC[platform] and len(s) > 400:
                        # 5' truncation; direct RNA is read 3'->5' so its truncation is at the 5' end of the transcript as well
                        s = s[rnd.randint(1, min(len(s) - 250, 400)):]
                    s = s + "A" * rnd.randint(10, 25)
                    s = mutate(s, sub, ins, dele)
                    if not ORIENTED[platform] and rnd.random() < 0.5:
                        s = rc(s)
                    n += 1
                    f.write("@%s_%s_%d\n%s\n+\n%s\n" % (sample, tid, n, s, q * len(s)))

for platform in ("hifi", "ontunstr", "ontstr", "drna"):
    d = os.path.join(OUT, platform); os.makedirs(d, exist_ok=True)
    rows = []
    for s, g in DESIGN:
        if platform == "ontstr" and g == "trt":
            continue
        simulate(platform, s, g, os.path.join(d, s + ".fastq"), rows)
    with open(os.path.join(d, "truth_counts.tsv"), "w") as f:
        f.write("platform\tsample\ttranscript\tn_reads\n")
        for r in rows:
            f.write("%s\t%s\t%s\t%d\n" % r)

with open(os.path.join(OUT, "truth_dtu.tsv"), "w") as f:
    f.write("gene\tplanted_dtu\n")
    for gid in GENES:
        f.write("%s\t%d\n" % (gid, int(genes[gid]["kind"] == "dtu")))
json.dump({"seed": SEED, "contig": CHR, "length": GL, "n_genes": len(GENES), "alt5": alt5_detail,
           "micro": {g: genes[g]["exons"][2] for g in GENES if genes[g]["kind"].startswith("micro")}, "synthetic": True},
          open(os.path.join(OUT, "meta.json"), "w"), indent=1)
print("wrote", OUT, "genome", GL, "isoforms", len(iso))
