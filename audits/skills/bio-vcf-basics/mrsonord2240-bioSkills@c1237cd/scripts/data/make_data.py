#!/usr/bin/env python3
"""SYNTHETIC data generator for the variant-annotation-curation-analyst Skill audits (2026-09-11).

Everything written here is synthetic: a random reference genome (two contigs, chr1/chr2),
a toy protein-coding gene SYNG1 with engineered codons, synthetic caller VCFs, synthetic
dbSNP/gnomAD/ClinVar-style annotation VCFs (identifiers rs9000000xx are NOT real rsIDs),
a synthetic 8-sample cohort, a synthetic gVCF and a synthetic annotated trio.
No real individual's data is used.

Usage: python make_data.py <outdir>
"""
import math
import os
import random
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
rng = random.Random(20260911)

STOPS = {"TAA", "TAG", "TGA"}


def rand_seq(n):
    return [rng.choice("ACGT") for _ in range(n)]


chrom = {"chr1": rand_seq(20000), "chr2": rand_seq(15000)}


def put(c, pos1, s):
    chrom[c][pos1 - 1:pos1 - 1 + len(s)] = list(s)


def ref(c, pos1, n=1):
    return "".join(chrom[c][pos1 - 1:pos1 - 1 + n])


# ---- engineered repeat features -------------------------------------------------------
put("chr1", 500, "GAAAAAAAC")      # homopolymer A7 at 501-507
put("chr1", 800, "TCACACACAG")     # (CA)4 at 801-808

# ---- toy gene SYNG1 (+ strand), 3 exons, 90 codons ------------------------------------
codons = ["ATG"]
while len(codons) < 89:
    c = "".join(rng.choice("ACGT") for _ in range(3))
    if c not in STOPS:
        codons.append(c)
codons.append("TAA")
codons[5] = "GAT"    # Asp  -> G>C at codon pos1 gives CAT (His): missense
codons[10] = "CTA"   # Leu  -> C>T (TTA Leu) and A>C (CTC Leu) are each synonymous; CTA>TTC = Phe
codons[20] = "GCT"   # Ala  -> T>C at pos3 gives GCC (Ala): synonymous
codons[40] = "CAG"   # Gln  -> C>T gives TAG: stop_gained (exon 2, NMD-competent)
codons[85] = "CGA"   # Arg  -> C>T gives TGA: stop_gained in LAST exon (NMD-escape)
cds = "".join(codons)
assert len(cds) == 270
put("chr1", 1001, "".join(rand_seq(10)))          # 5'UTR 1001-1010
put("chr1", 1011, cds[0:90])                        # exon1 CDS 1011-1100
intron1 = "GT" + "".join(rand_seq(96)) + "AG"       # 1101-1200
put("chr1", 1101, intron1)
put("chr1", 1201, cds[90:190])                      # exon2 CDS 1201-1300
intron2 = "GT" + "".join(rand_seq(96)) + "AG"       # 1301-1400
put("chr1", 1301, intron2)
put("chr1", 1401, cds[190:270])                     # exon3 CDS 1401-1480
put("chr1", 1481, "".join(rand_seq(70)))           # 3'UTR 1481-1550
# plant known reference bases used by site-specific records
put("chr1", 2000, "A")
put("chr1", 4000, "C")


def cds_to_genomic(off):
    if off < 90:
        return 1011 + off
    if off < 190:
        return 1201 + (off - 90)
    return 1401 + (off - 190)


POS_MISSENSE = cds_to_genomic(5 * 3)        # 1026
POS_MNP = cds_to_genomic(10 * 3)            # 1041
POS_SYN = cds_to_genomic(20 * 3 + 2)        # 1073
POS_STOP = cds_to_genomic(40 * 3)           # 1231
POS_STOP_LAST = cds_to_genomic(85 * 3)      # 1446
POS_FS = cds_to_genomic(70 * 3) - 1         # 1420 (anchor) -> deletes 1421
assert ref("chr1", POS_MISSENSE) == "G" and ref("chr1", POS_MNP, 3) == "CTA"
assert ref("chr1", POS_SYN) == "T" and ref("chr1", POS_STOP) == "C" and ref("chr1", POS_STOP_LAST) == "C"

# ---- reference FASTA + .fai --------------------------------------------------------------
with open(os.path.join(OUT, "ref.fa"), "w", newline="\n") as fh, \
        open(os.path.join(OUT, "ref.fa.fai"), "w", newline="\n") as fai:
    offset = 0
    for c in ("chr1", "chr2"):
        header = f">{c} SYNTHETIC random contig\n"
        fh.write(header)
        offset += len(header)
        seq = "".join(chrom[c])
        fai.write(f"{c}\t{len(seq)}\t{offset}\t60\t61\n")
        for i in range(0, len(seq), 60):
            line = seq[i:i + 60] + "\n"
            fh.write(line)
            offset += len(line)

# ---- GFF3 (Ensembl-style, as bcftools csq expects) ----------------------------------------
gff = [
    "##gff-version 3",
    "chr1\tsynthetic\tgene\t1001\t1550\t.\t+\t.\tID=gene:SYNG1;Name=SYNG1;biotype=protein_coding",
    "chr1\tsynthetic\tmRNA\t1001\t1550\t.\t+\t.\tID=transcript:SYNT1;Parent=gene:SYNG1;Name=SYNG1-201;biotype=protein_coding",
    "chr1\tsynthetic\tfive_prime_UTR\t1001\t1010\t.\t+\t.\tParent=transcript:SYNT1",
    "chr1\tsynthetic\texon\t1001\t1100\t.\t+\t.\tParent=transcript:SYNT1",
    "chr1\tsynthetic\tCDS\t1011\t1100\t.\t+\t0\tParent=transcript:SYNT1",
    "chr1\tsynthetic\texon\t1201\t1300\t.\t+\t.\tParent=transcript:SYNT1",
    "chr1\tsynthetic\tCDS\t1201\t1300\t.\t+\t0\tParent=transcript:SYNT1",
    "chr1\tsynthetic\texon\t1401\t1550\t.\t+\t.\tParent=transcript:SYNT1",
    "chr1\tsynthetic\tCDS\t1401\t1480\t.\t+\t2\tParent=transcript:SYNT1",
    "chr1\tsynthetic\tthree_prime_UTR\t1481\t1550\t.\t+\t.\tParent=transcript:SYNT1",
]
with open(os.path.join(OUT, "genes.gff3"), "w", newline="\n") as fh:
    fh.write("\n".join(gff) + "\n")

CONTIGS = "##contig=<ID=chr1,length=20000>\n##contig=<ID=chr2,length=15000>\n"
FMT_HDR = (
    '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n'
    '##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths">\n'
    '##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">\n'
    '##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype quality">\n'
    '##FORMAT=<ID=PL,Number=G,Type=Integer,Description="Phred-scaled genotype likelihoods">\n'
    '##FORMAT=<ID=PS,Number=1,Type=Integer,Description="Phase set">\n'
)


def w(name, text):
    with open(os.path.join(OUT, name), "w", newline="\n") as fh:
        fh.write(text)


# ---- caller A (GATK-like, left-aligned, no MNPs; adjacent SNVs phased) --------------------
fs_anchor = ref("chr1", POS_FS, 2)
recsA = [
    ("chr1", 500, ".", "GA", "G", "0/1:14,12:26:99"),
    ("chr1", 800, ".", "TCA", "T", "0/1:15,13:28:99"),
    ("chr1", POS_MISSENSE, ".", "G", "C", "0/1:16,15:31:99"),
    ("chr1", POS_MNP, ".", "C", "T", "0|1:12,14:26:99:1041"),
    ("chr1", POS_MNP + 2, ".", "A", "C", "0|1:12,14:26:99:1041"),
    ("chr1", POS_SYN, ".", "T", "C", "0/1:13,13:26:99"),
    ("chr1", 1101, ".", "G", "A", "0/1:10,12:22:99"),
    ("chr1", POS_STOP, ".", "C", "T", "0/1:11,10:21:99"),
    ("chr1", POS_FS, ".", fs_anchor, fs_anchor[0], "0/1:14,11:25:99"),
    ("chr1", POS_STOP_LAST, ".", "C", "T", "0/1:12,12:24:99"),
    ("chr1", 2000, ".", "A", "C,G", "1/2:1,12,13:26:99"),
]
hdrA = ("##fileformat=VCFv4.2\n##source=SYNTHETIC_callerA_GATKlike\n" + CONTIGS
        + '##INFO=<ID=DP,Number=1,Type=Integer,Description="Depth">\n' + FMT_HDR
        + "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYN_S1\n")
bodyA = ""
for c, p, i, r, a, s in recsA:
    fmt = "GT:AD:DP:GQ:PS" if s.count(":") == 4 else "GT:AD:DP:GQ"
    bodyA += f"{c}\t{p}\t{i}\t{r}\t{a}\t200\tPASS\tDP=30\t{fmt}\t{s}\n"
w("callerA.vcf", hdrA + bodyA)

# ---- caller B (FreeBayes-like: right-shifted indels, MNP block, REF mismatch) --------------
recsB = [
    ("chr1", 506, ".", "AA", "A", "0/1:13,12:25"),                  # same A-deletion, not left-aligned
    ("chr1", 806, ".", "ACA", "A", "0/1:14,12:26"),                 # same CA-deletion, right-shifted
    ("chr1", POS_MISSENSE, ".", "G", "C", "0/1:15,15:30"),
    ("chr1", POS_MNP, ".", "CTA", "TTC", "0/1:12,13:25"),           # MNP/block substitution
    ("chr1", POS_SYN, ".", "T", "C", "0/1:12,13:25"),
    ("chr1", 1101, ".", "G", "A", "0/1:10,11:21"),
    ("chr1", POS_STOP, ".", "C", "T", "0/1:10,11:21"),
    ("chr1", 2000, ".", "A", "C,G", "1/2:0,11,12:23"),
    ("chr1", 4000, ".", "T", "G", "0/1:10,10:20"),                  # REF mismatch (reference is C)
]
hdrB = ("##fileformat=VCFv4.2\n##source=SYNTHETIC_callerB_FreeBayeslike\n" + CONTIGS
        + '##INFO=<ID=DP,Number=1,Type=Integer,Description="Depth">\n' + FMT_HDR
        + "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYN_S1\n")
bodyB = "".join(f"{c}\t{p}\t{i}\t{r}\t{a}\t150\t.\tDP=25\tGT:AD:DP\t{s}\n" for c, p, i, r, a, s in recsB)
w("callerB.vcf", hdrB + bodyB)

# ---- synthetic annotation databases (canonical, left-aligned, biallelic) --------------------
db = [  # chrom, pos, ref, alt, rsid, AF, AF_grpmax, fafmax, grpmax, CLNSIG, CLNREVSTAT, CLNDN, CLNSIGCONF
    ("chr1", 500, "GA", "G", "rs900000001", 0.00002, 0.00005, 0.000021, "afr",
     "Pathogenic", "criteria_provided,_multiple_submitters,_no_conflicts", "SYN_disorder_A", None),
    ("chr1", 800, "TCA", "T", "rs900000002", 0.012, 0.031, 0.027, "nfe",
     "Benign", "criteria_provided,_multiple_submitters,_no_conflicts", "SYN_disorder_A", None),
    ("chr1", POS_MISSENSE, "G", "C", "rs900000003", 0.0003, 0.0011, 0.00082, "sas",
     "Uncertain_significance", "criteria_provided,_single_submitter", "SYN_disorder_A", None),
    ("chr1", POS_MNP, "C", "T", "rs900000004", 0.08, 0.12, 0.11, "eas", None, None, None, None),
    ("chr1", POS_MNP + 2, "A", "C", "rs900000005", 0.07, 0.10, 0.09, "eas", None, None, None, None),
    ("chr1", 1101, "G", "A", None, None, None, None, None,
     "Likely_pathogenic", "criteria_provided,_single_submitter", "SYN_disorder_A", None),
    ("chr1", POS_STOP, "C", "T", "rs900000006", None, None, None, None,
     "Pathogenic", "reviewed_by_expert_panel", "SYN_disorder_A", None),
    ("chr1", 2000, "A", "C", "rs900000007", 0.2, 0.35, 0.33, "afr", None, None, None, None),
    ("chr1", 2000, "A", "G", "rs900000007", 0.001, 0.004, 0.0031, "nfe",
     "Conflicting_classifications_of_pathogenicity", "criteria_provided,_conflicting_classifications",
     "SYN_disorder_B", "Pathogenic(2)|Uncertain_significance(1)|Likely_benign(1)"),
]
hdr_db = "##fileformat=VCFv4.2\n" + CONTIGS
dbsnp = hdr_db + "##source=SYNTHETIC_dbSNP_like (rs9000000xx are NOT real rsIDs)\n" \
    + "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
gnom = hdr_db + "##source=SYNTHETIC_gnomAD_v4_like\n" \
    + '##INFO=<ID=AF,Number=A,Type=Float,Description="Alt allele frequency">\n' \
    + '##INFO=<ID=AF_grpmax,Number=A,Type=Float,Description="Max AF across non-bottlenecked groups">\n' \
    + '##INFO=<ID=grpmax,Number=A,Type=String,Description="Group with max AF">\n' \
    + '##INFO=<ID=fafmax_faf95_max,Number=A,Type=Float,Description="Max filtering AF (95% CI)">\n' \
    + "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
clin = hdr_db + "##source=SYNTHETIC_ClinVar_like\n" \
    + '##INFO=<ID=CLNSIG,Number=.,Type=String,Description="Clinical significance">\n' \
    + '##INFO=<ID=CLNREVSTAT,Number=.,Type=String,Description="Review status">\n' \
    + '##INFO=<ID=CLNDN,Number=.,Type=String,Description="Disease name">\n' \
    + '##INFO=<ID=CLNSIGCONF,Number=.,Type=String,Description="Conflicting significance">\n' \
    + "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
for c, p, r, a, rs, af, afg, faf, grp, sig, rev, dn, conf in db:
    if rs:
        dbsnp += f"{c}\t{p}\t{rs}\t{r}\t{a}\t.\t.\t.\n"
    if af is not None:
        gnom += f"{c}\t{p}\t.\t{r}\t{a}\t.\tPASS\tAF={af};AF_grpmax={afg};grpmax={grp};fafmax_faf95_max={faf}\n"
    if sig:
        info = f"CLNSIG={sig};CLNREVSTAT={rev};CLNDN={dn}" + (f";CLNSIGCONF={conf}" if conf else "")
        clin += f"{c}\t{p}\t.\t{r}\t{a}\t.\t.\t{info}\n"
w("dbsnp_syn.vcf", dbsnp)
w("gnomad_syn.vcf", gnom)
w("clinvar_syn.vcf", clin)

# ---- synthetic 8-sample cohort (raw joint callset, GATK-style annotations) -------------------
SAMPLES = [f"SYN_S{i}" for i in range(1, 9)]
TI = {("A", "G"), ("G", "A"), ("C", "T"), ("T", "C")}


def pick_alt(r, transition):
    if transition:
        return {"A": "G", "G": "A", "C": "T", "T": "C"}[r]
    return rng.choice([b for b in "ACGT" if b != r and (r, b) not in TI])


def lik(a, rr):
    out = []
    for q in (0.01, 0.5, 0.99):
        out.append(a * math.log10(q) + rr * math.log10(1 - q))
    m = max(out)
    pl = [int(round(-10 * (x - m))) for x in out]
    return pl


def geno_call(ref_n, alt_n):
    pl = lik(alt_n, ref_n)
    g = pl.index(0)
    gq = min(99, sorted(pl)[1])
    return g, pl, gq


def sample_reads(dp, q):
    alt = sum(1 for _ in range(dp) if rng.random() < q)
    return dp - alt, alt


cohort_lines = []
used = set()
site_classes = ([("true_snp", None)] * 240 + [("true_homalt", None)] * 25 + [("artifact_snp", None)] * 60
                + [("excess_het", None)] * 6 + [("true_indel", None)] * 20 + [("artifact_indel", None)] * 10)
positions = []
for cls, _ in site_classes:
    while True:
        c = rng.choice(["chr1", "chr2"])
        lo = 5001 if c == "chr1" else 1
        p = rng.randint(lo, len(chrom[c]) - 10)
        if (c, p) not in used and all((c, p + d) not in used for d in range(-3, 4)):
            used.add((c, p))
            positions.append((c, p, cls))
            break
positions.sort(key=lambda x: (x[0], x[1]))
for idx, (c, p, cls) in enumerate(positions):
    r = ref(c, p)
    if cls in ("true_indel", "artifact_indel"):
        if rng.random() < 0.5:
            r2 = ref(c, p, 2)
            REF, ALT = r2, r2[0]
        else:
            REF, ALT = r, r + rng.choice("ACGT")
        transition = None
    else:
        transition = (rng.random() < 2 / 3) if cls != "artifact_snp" else (rng.random() < 1 / 3)
        REF, ALT = r, pick_alt(r, transition)
    if cls == "true_homalt":
        paf = 0.9
    elif cls in ("true_snp", "true_indel"):
        paf = rng.choice([0.02, 0.05, 0.1, 0.2, 0.3, 0.45])
    else:
        paf = 0.0
    fields = []
    gts_this = []
    n_het = n_homalt = 0
    alt_total = 0
    for si, s in enumerate(SAMPLES):
        dp = max(0, int(rng.gauss(32, 7)))
        if s == "SYN_S6" and rng.random() < 0.25:
            dp = rng.randint(0, 3)
        g_true = sum(1 for _ in range(2) if rng.random() < paf)
        if cls == "true_homalt":
            g_true = 2 if rng.random() < 0.8 else 0
        if cls == "artifact_snp" or cls == "artifact_indel":
            g_true = 0
            q = 0.18 if rng.random() < 0.3 else 0.01
        elif cls == "excess_het":
            q = 0.5
        else:
            q = {0: 0.01, 1: 0.5, 2: 0.99}[g_true]
        if s == "SYN_S7":
            q = q * 0.85 + 0.15 * max(paf, 0.05)
        rn, an = sample_reads(dp, q)
        if dp < 4:
            fields.append(f"./.:{rn},{an}:{dp}:.:.")
            gts_this.append(-1)
            continue
        g, pl, gq = geno_call(rn, an)
        gt = ["0/0", "0/1", "1/1"][g]
        gts_this.append(g)
        n_het += g == 1
        n_homalt += g == 2
        alt_total += an if g > 0 else 0
        fields.append(f"{gt}:{rn},{an}:{dp}:{gq}:{','.join(map(str, pl))}")
    if n_het + n_homalt == 0:
        # force at least one carrier so the record is a variant
        fields[0] = "0/1:12,11:23:99:180,0,210"
        n_het, alt_total = 1, 11
    qual = round(min(4000.0, 10.0 * alt_total + rng.uniform(5, 30)), 2)
    altdp = max(1, alt_total)
    if cls in ("artifact_snp", "artifact_indel"):
        qd = round(rng.uniform(0.4, 1.9), 2) if rng.random() < 0.6 else round(rng.uniform(2.5, 6), 2)
        fs = round(rng.uniform(62, 120), 3) if rng.random() < 0.4 else round(rng.uniform(0, 20), 3)
        mq = round(rng.uniform(25, 39), 2) if rng.random() < 0.3 else 60.0
        rprs = round(rng.uniform(-25, -9), 3) if rng.random() < 0.4 else round(rng.uniform(-2, 1), 3)
        sor = round(rng.uniform(3.5, 12), 3) if rng.random() < 0.4 else round(rng.uniform(0.5, 2), 3)
        mqrs = round(rng.uniform(-14, -13), 3) if rng.random() < 0.2 else round(rng.uniform(-1, 1), 3)
        qual = round(min(qual, rng.uniform(20, 80)), 2)
    else:
        qd = round(max(2.2, rng.gauss(18, 6)), 2)
        fs = round(abs(rng.gauss(2, 3)), 3) if cls != "true_indel" else round(rng.uniform(0, 150), 3)
        mq = 60.0 if cls != "excess_het" else 44.0
        rprs = round(rng.gauss(0, 0.8), 3)
        sor = round(rng.uniform(0.3, 1.6), 3) if cls != "true_indel" else round(rng.uniform(0.5, 6), 3)
        mqrs = round(rng.gauss(0, 0.8), 3)
    info = [f"DP={sum(int(f.split(':')[2]) for f in fields)}", f"QD={qd}", f"FS={fs}", f"MQ={mq}", f"SOR={sor}"]
    if n_het > 0:
        info += [f"MQRankSum={mqrs}", f"ReadPosRankSum={rprs}"]
    exhet = round(rng.uniform(60, 200), 3) if cls == "excess_het" else round(rng.uniform(0, 5), 3)
    info.append(f"ExcessHet={exhet}")
    known = cls in ("true_snp", "true_homalt", "true_indel", "excess_het") and paf >= 0.05
    vid = f"rs9{idx:08d}" if known else "."
    cohort_lines.append(f"{c}\t{p}\t{vid}\t{REF}\t{ALT}\t{qual}\t.\t{';'.join(info)}\tGT:AD:DP:GQ:PL\t" + "\t".join(fields))

# SYN_S8 is written as an independent draw above; re-derive it as a duplicate of SYN_S3 genotypes
# with fresh read sampling so identity QC has something to find.
fixed = []
for line in cohort_lines:
    cols = line.split("\t")
    s3 = cols[9 + 2].split(":")
    gt = s3[0]
    if gt == "./.":
        cols[9 + 7] = cols[9 + 2]
    else:
        g = {"0/0": 0, "0/1": 1, "1/1": 2}[gt]
        dp = max(8, int(rng.gauss(32, 7)))
        rn, an = sample_reads(dp, {0: 0.01, 1: 0.5, 2: 0.99}[g])
        g2, pl, gq = geno_call(rn, an)
        cols[9 + 7] = f"{['0/0', '0/1', '1/1'][g2]}:{rn},{an}:{dp}:{gq}:{','.join(map(str, pl))}"
    fixed.append("\t".join(cols))
cohort_lines = fixed

hdr_c = ("##fileformat=VCFv4.2\n##source=SYNTHETIC_cohort_GATKlike_raw_joint_callset\n"
         "##reference=ref.fa\n" + CONTIGS
         + '##INFO=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth">\n'
         + '##INFO=<ID=QD,Number=1,Type=Float,Description="Variant confidence/quality by depth">\n'
         + '##INFO=<ID=FS,Number=1,Type=Float,Description="Phred-scaled p-value Fisher strand bias">\n'
         + '##INFO=<ID=MQ,Number=1,Type=Float,Description="RMS mapping quality">\n'
         + '##INFO=<ID=SOR,Number=1,Type=Float,Description="Symmetric odds ratio strand bias">\n'
         + '##INFO=<ID=MQRankSum,Number=1,Type=Float,Description="Alt vs ref read mapping qualities">\n'
         + '##INFO=<ID=ReadPosRankSum,Number=1,Type=Float,Description="Alt vs ref read position bias">\n'
         + '##INFO=<ID=ExcessHet,Number=1,Type=Float,Description="Phred-scaled p-value for exact test of excess heterozygosity">\n'
         + FMT_HDR + "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t" + "\t".join(SAMPLES) + "\n")
w("cohort.vcf", hdr_c + "\n".join(cohort_lines) + "\n")
with open(os.path.join(OUT, "cohort_truth_classes.tsv"), "w", newline="\n") as fh:
    fh.write("chrom\tpos\tclass\n")
    for c, p, cls in positions:
        fh.write(f"{c}\t{p}\t{cls}\n")
w("cohort.ped", "".join(f"FAM{i}\t{s}\t0\t0\t{1 + (i % 2)}\t-9\n" for i, s in enumerate(SAMPLES, 1)))

# ---- synthetic gVCF ------------------------------------------------------------------------------
g_hdr = ("##fileformat=VCFv4.2\n##source=SYNTHETIC_gVCF_HaplotypeCaller_ERC_GVCF_like\n" + CONTIGS
         + '##ALT=<ID=NON_REF,Description="Represents any possible alternative allele not already represented">\n'
         + '##INFO=<ID=END,Number=1,Type=Integer,Description="End of reference block">\n'
         + '##FORMAT=<ID=MIN_DP,Number=1,Type=Integer,Description="Minimum DP in block">\n' + FMT_HDR
         + "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYN_S1\n")
g_body = (
    f"chr1\t1\t.\t{ref('chr1', 1)}\t<NON_REF>\t.\t.\tEND=1025\tGT:DP:GQ:MIN_DP:PL\t0/0:30:99:22:0,66,990\n"
    f"chr1\t{POS_MISSENSE}\t.\tG\tC,<NON_REF>\t512.6\t.\t.\tGT:AD:DP:GQ:PL\t0/1:16,15,0:31:99:520,0,560,570,610,1180\n"
    f"chr1\t{POS_MISSENSE + 1}\t.\t{ref('chr1', POS_MISSENSE + 1)}\t<NON_REF>\t.\t.\tEND=1200\tGT:DP:GQ:MIN_DP:PL\t0/0:28:60:12:0,36,540\n"
    f"chr1\t1201\t.\t{ref('chr1', 1201)}\t<NON_REF>\t.\t.\tEND=1230\tGT:DP:GQ:MIN_DP:PL\t0/0:3:0:1:0,0,0\n"
)
w("sample.g.vcf", g_hdr + g_body)

# ---- synthetic VEP-annotated trio (CSQ + gnomAD v4 field names) ---------------------------------
CSQ_FMT = "Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|HGVSc|HGVSp|MANE_SELECT|CANONICAL"


def csq(alt, blocks):
    return ",".join("|".join([alt] + b) for b in blocks)


def blk(cons, imp, sym, feat, mane):
    return [cons, imp, sym, f"ENSGSYN_{sym}", "Transcript", feat, "protein_coding", "", "", "",
            mane, "YES" if mane else ""]


trio = [
    # chrom,pos,ref,alt,qual,filter,info_extra,csq_blocks,(gt,ad,dp,gq) x3 [PROBAND,MOTHER,FATHER], note
    ("chr1", 10100, "C", "T", 480, "PASS", "AF_grpmax=0.00001;fafmax_faf95_max=0.000004",
     [blk("missense_variant", "MODERATE", "SYNDN1", "ENSTSYN1", "NM_SYN1.1")],
     [("0/1", "14,15", 29, 99), ("0/0", "30,0", 30, 90), ("0/0", "28,0", 28, 84)], "de novo, good parental depth"),
    ("chr1", 10500, "G", "A", 300, "PASS", "AF_grpmax=0.00002;fafmax_faf95_max=0.00001",
     [blk("stop_gained", "HIGH", "SYNDN2", "ENSTSYN2", "NM_SYN2.1")],
     [("0/1", "10,11", 21, 99), ("0/0", "5,0", 5, 15), ("0/0", "6,0", 6, 18)], "de novo candidate but parents DP<10"),
    ("chr1", 11000, "A", "G", 350, "PASS", "AF_grpmax=0.0002;fafmax_faf95_max=0.00008",
     [blk("missense_variant", "MODERATE", "SYNCH1", "ENSTSYN3", "NM_SYN3.1")],
     [("0/1", "12,13", 25, 99), ("0/1", "13,12", 25, 99), ("0/0", "26,0", 26, 78)], "comp-het part 1 (maternal)"),
    ("chr1", 11400, "T", "C", 360, "PASS", "AF_grpmax=0.00003;fafmax_faf95_max=0.00002",
     [blk("missense_variant", "MODERATE", "SYNCH1", "ENSTSYN3", "NM_SYN3.1")],
     [("0/1", "11,14", 25, 99), ("0/0", "25,0", 25, 75), ("0/1", "12,12", 24, 99)], "comp-het part 2 (paternal)"),
    ("chr1", 12000, "G", "T", 330, "PASS", "AF_grpmax=0.00005;fafmax_faf95_max=0.00003",
     [blk("missense_variant", "MODERATE", "SYNCIS1", "ENSTSYN4", "NM_SYN4.1")],
     [("0/1", "12,12", 24, 99), ("0/1", "12,11", 23, 99), ("0/0", "24,0", 24, 72)], "two maternal hets in same gene (cis)"),
    ("chr1", 12300, "C", "A", 340, "PASS", "AF_grpmax=0.00004;fafmax_faf95_max=0.00002",
     [blk("missense_variant", "MODERATE", "SYNCIS1", "ENSTSYN4", "NM_SYN4.1")],
     [("0/1", "13,12", 25, 99), ("0/1", "12,13", 25, 99), ("0/0", "25,0", 25, 75)], "second maternal het (cis)"),
    ("chr1", 13000, "A", "T", 900, "PASS", "AF_grpmax=0.0009;fafmax_faf95_max=0.0006",
     [blk("frameshift_variant", "HIGH", "SYNAR1", "ENSTSYN5", "NM_SYN5.1")],
     [("1/1", "0,30", 30, 90), ("0/1", "15,14", 29, 99), ("0/1", "14,15", 29, 99)], "AR homozygous candidate"),
    ("chr2", 2000, "G", "A", 410, "PASS", "AF_grpmax=0.00001;fafmax_faf95_max=0.000005;CLNSIG=Pathogenic",
     [blk("stop_gained", "HIGH", "ATM", "ENSTSYN6", "NM_SYN6.1")],
     [("0/1", "12,12", 24, 99), ("0/1", "12,13", 25, 99), ("0/0", "25,0", 25, 75)], "ATM: in skill SF list but NOT in ACMG SF v3.2"),
    ("chr2", 3000, "C", "T", 420, "PASS", "AF_grpmax=0.00001;fafmax_faf95_max=0.000006;CLNSIG=Pathogenic",
     [blk("stop_gained", "HIGH", "DSP", "ENSTSYN7", "NM_SYN7.1")],
     [("0/1", "13,12", 25, 99), ("0/0", "25,0", 25, 75), ("0/1", "12,12", 24, 99)], "DSP: in ACMG SF v3.2 but MISSING from skill list"),
    ("chr2", 4000, "T", "G", 390, "PASS", "AF_grpmax=0.00002;fafmax_faf95_max=0.00001",
     [blk("intron_variant", "MODIFIER", "SYNMT1", "ENSTSYN8a", ""),
      blk("stop_gained", "HIGH", "SYNMT1", "ENSTSYN8b", "NM_SYN8.1")],
     [("0/1", "12,12", 24, 99), ("0/0", "24,0", 24, 72), ("0/0", "25,0", 25, 75)], "MANE block is stop_gained; first block intronic"),
    ("chr2", 5000, "A", "C", 520, "PASS", "AF_grpmax=0.00001;fafmax_faf95_max=0.000005",
     [blk("missense_variant", "MODERATE", "SYNGQ1", "ENSTSYN9", "NM_SYN9.1")],
     [("0/1", "3,2", 12, 8), ("0/0", "22,0", 22, 66), ("0/0", "23,0", 23, 69)], "high QUAL but proband GQ=8"),
    ("chr2", 6000, "G", "C", 610, "PASS", "fafmax_faf95_max=0.05",
     [blk("missense_variant", "MODERATE", "SYNCOM1", "ENSTSYN10", "NM_SYN10.1")],
     [("0/1", "12,12", 24, 99), ("0/0", "24,0", 24, 72), ("0/0", "24,0", 24, 72)], "common (FAF 5%) but only v4 fafmax field present"),
    ("chr2", 7000, "C", "G", 60, "LowQual", "AF_grpmax=0.00001;fafmax_faf95_max=0.000005",
     [blk("missense_variant", "MODERATE", "SYNLQ1", "ENSTSYN11", "NM_SYN11.1")],
     [("0/1", "12,12", 24, 99), ("0/0", "24,0", 24, 72), ("0/0", "24,0", 24, 72)], "FILTER=LowQual"),
    ("chr2", 8000, "T", "A", 500, "PASS", "AF_grpmax=0.03;fafmax_faf95_max=0.025",
     [blk("synonymous_variant", "LOW", "SYNSYN1", "ENSTSYN12", "NM_SYN12.1")],
     [("0/1", "12,12", 24, 99), ("0/1", "12,12", 24, 99), ("0/0", "24,0", 24, 72)], "common synonymous"),
]
t_hdr = ("##fileformat=VCFv4.2\n##source=SYNTHETIC_trio_VEPlike_gnomADv4_names\n"
         "##contig=<ID=chr1,length=20000>\n##contig=<ID=chr2,length=15000>\n"
         '##FILTER=<ID=LowQual,Description="Low quality">\n'
         f'##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence annotations from Ensembl VEP. Format: {CSQ_FMT}">\n'
         '##INFO=<ID=AF_grpmax,Number=A,Type=Float,Description="gnomAD v4 grpmax AF">\n'
         '##INFO=<ID=fafmax_faf95_max,Number=A,Type=Float,Description="gnomAD v4 max FAF95">\n'
         '##INFO=<ID=CLNSIG,Number=.,Type=String,Description="ClinVar significance">\n'
         + FMT_HDR + "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPROBAND\tMOTHER\tFATHER\n")
t_body = ""
notes = "chrom\tpos\tnote\n"
for c, p, r, a, q, f, inf, blocks, gts, note in trio:
    samp = "\t".join(f"{g}:{ad}:{dp}:{gq}" for g, ad, dp, gq in gts)
    t_body += f"{c}\t{p}\t.\t{r}\t{a}\t{q}\t{f}\t{inf};CSQ={csq(a, blocks)}\tGT:AD:DP:GQ\t{samp}\n"
    notes += f"{c}\t{p}\t{note}\n"
w("trio_annot.vcf", t_hdr + t_body)
w("trio_truth_notes.tsv", notes)

# ---- VEP-like annotated single-sample VCF for CSQ parsing ----------------------------------------
v_hdr = ("##fileformat=VCFv4.2\n##source=SYNTHETIC_VEP110_like\n" + CONTIGS
         + f'##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence annotations from Ensembl VEP. Format: {CSQ_FMT}">\n'
         + FMT_HDR + "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYN_S1\n")
v_body = (
    f"chr1\t{POS_STOP}\t.\tC\tT\t200\tPASS\tCSQ={csq('T', [blk('intron_variant','MODIFIER','SYNG1','ENSTSYN_alt','') , blk('stop_gained','HIGH','SYNG1','SYNT1','NM_SYNG1.1')])}\tGT\t0/1\n"
    f"chr1\t{POS_SYN}\t.\tT\tC\t200\tPASS\tCSQ={csq('C', [blk('synonymous_variant','LOW','SYNG1','SYNT1','NM_SYNG1.1')])}\tGT\t0/1\n"
    f"chr1\t{POS_MISSENSE}\t.\tG\tC\t200\tPASS\tCSQ={csq('C', [blk('splice_region_variant&intron_variant','LOW','SYNG1','ENSTSYN_alt',''), blk('missense_variant','MODERATE','SYNG1','SYNT1','NM_SYNG1.1')])}\tGT\t0/1\n"
)
w("vep_annotated.vcf", v_hdr + v_body)
print("wrote synthetic data to", OUT)
print("POS_MISSENSE", POS_MISSENSE, "POS_MNP", POS_MNP, "POS_SYN", POS_SYN, "POS_STOP", POS_STOP,
      "POS_STOP_LAST", POS_STOP_LAST, "POS_FS", POS_FS, "cohort sites", len(cohort_lines))
