#!/usr/bin/env python3
"""SYNTHETIC rare-variant association dataset for the bio-population-genetics-rare-variant-association audit
(2026-09-15). No real individuals. Seed 20260915.

N = 2000 unrelated samples; binary trait with ~10% cases (imbalanced), covariates age, sex, PC1, PC2.
Three chromosomes, each with 400 common "array" SNPs (for the regenie step-1 null) and 10 genes of rare
variants (MAF 0.0005-0.01) annotated LoF / missense / synonymous. Planted truth:
  G01 (chr1)  BURDEN   : every LoF and missense variant raises risk (log-OR +1.2)
  G11 (chr2)  MIXED    : half the missense variants raise risk (+1.4), half lower it (-1.4); LoF neutral
  G21 (chr3)  LOF_ONLY : only LoF variants raise risk (+1.6); missense are neutral passengers
  all other genes      : null
Outputs (in the working directory):
  array.vcf, wes.vcf           genotypes (VCF 4.2, GT only)
  pheno.txt, covar.txt         regenie format (FID IID ...), Y coded 0/1
  annot.txt, sets.txt, masks.txt   regenie --anno-file / --set-list / --mask-def
  gene_<G>.tsv                 per-gene 0/1/2 dosage matrix (rows = samples) for the SKAT R package
  covar_skat.tsv               IID Y age sex PC1 PC2
  truth.tsv                    gene, class, n_variants, n_LoF, n_missense, cumulative carrier counts
"""
import math
import random

rng = random.Random(20260915)
N = 2000
SAMPLES = [f"SYN{i:04d}" for i in range(1, N + 1)]
BASES = "ACGT"


def draw_gt(maf):
    return sum(1 for _ in range(2) if rng.random() < maf)


age = [rng.gauss(55, 10) for _ in SAMPLES]
sex = [rng.randint(0, 1) for _ in SAMPLES]
pc1 = [rng.gauss(0, 1) for _ in SAMPLES]
pc2 = [rng.gauss(0, 1) for _ in SAMPLES]

array_recs = []   # (chrom, pos, id, ref, alt, gts)
wes_recs = []     # (chrom, pos, id, ref, alt, gts, gene, anno, beta)
genes = {}
for ci, chrom in enumerate(["1", "2", "3"]):
    for k in range(400):
        pos = 100000 + k * 5000
        ref = rng.choice(BASES); alt = rng.choice([b for b in BASES if b != ref])
        maf = rng.uniform(0.05, 0.5)
        array_recs.append((chrom, pos, f"{chrom}:{pos}:{ref}:{alt}", ref, alt, [draw_gt(maf) for _ in SAMPLES]))
    for g in range(10):
        gname = f"G{ci}{g + 1}" if not (ci == 0 and g == 9) else "G10"
        gname = f"G{ci * 10 + g + 1:02d}"
        start = 5_000_000 + g * 200_000
        nvar = rng.randint(10, 22)
        cls = {"G01": "BURDEN", "G11": "MIXED", "G21": "LOF_ONLY"}.get(gname, "NULL")
        genes[gname] = {"chrom": chrom, "start": start, "vars": [], "class": cls}
        for v in range(nvar):
            pos = start + 30 * v + rng.randint(0, 20)
            ref = rng.choice(BASES); alt = rng.choice([b for b in BASES if b != ref])
            u = rng.random()
            anno = "LoF" if u < 0.25 else ("missense" if u < 0.75 else "synonymous")
            maf = math.exp(rng.uniform(math.log(0.0005), math.log(0.01)))
            beta = 0.0
            if cls == "BURDEN" and anno in ("LoF", "missense"):
                beta = 1.2
            elif cls == "MIXED" and anno == "missense":
                beta = 1.4 if len([x for x in genes[gname]["vars"] if x[7] == "missense"]) % 2 == 0 else -1.4
            elif cls == "LOF_ONLY" and anno == "LoF":
                beta = 1.6
            vid = f"{chrom}:{pos}:{ref}:{alt}"
            rec = (chrom, pos, vid, ref, alt, [draw_gt(maf) for _ in SAMPLES], gname, anno, beta)
            genes[gname]["vars"].append(rec)
            wes_recs.append(rec)

# liability
lin = []
for i in range(N):
    eta = -2.6 + 0.02 * (age[i] - 55) + 0.2 * sex[i] + 0.15 * pc1[i]
    for rec in wes_recs:
        if rec[8] != 0.0 and rec[5][i] > 0:
            eta += rec[8] * rec[5][i]
    lin.append(eta)
Y = [1 if rng.random() < 1 / (1 + math.exp(-e)) else 0 for e in lin]


def write_vcf(path, recs):
    with open(path, "w", newline="\n") as fh:
        fh.write("##fileformat=VCFv4.2\n##source=SYNTHETIC_rare_variant_audit_seed20260915\n")
        for c in ("1", "2", "3"):
            fh.write(f"##contig=<ID={c},length=10000000>\n")
        fh.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        fh.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t" + "\t".join(SAMPLES) + "\n")
        for r in sorted(recs, key=lambda x: (x[0], x[1])):
            gts = "\t".join(("0/0", "0/1", "1/1")[g] for g in r[5])
            fh.write(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t.\tPASS\t.\tGT\t{gts}\n")


write_vcf("array.vcf", array_recs)
write_vcf("wes.vcf", wes_recs)
with open("pheno.txt", "w", newline="\n") as fh:
    fh.write("FID IID Y\n")
    for s, y in zip(SAMPLES, Y):
        fh.write(f"{s} {s} {y}\n")
with open("covar.txt", "w", newline="\n") as fh:
    fh.write("FID IID age sex PC1 PC2\n")
    for i, s in enumerate(SAMPLES):
        fh.write(f"{s} {s} {age[i]:.2f} {sex[i]} {pc1[i]:.4f} {pc2[i]:.4f}\n")
with open("covar_skat.tsv", "w", newline="\n") as fh:
    fh.write("IID\tY\tage\tsex\tPC1\tPC2\n")
    for i, s in enumerate(SAMPLES):
        fh.write(f"{s}\t{Y[i]}\t{age[i]:.2f}\t{sex[i]}\t{pc1[i]:.4f}\t{pc2[i]:.4f}\n")
with open("annot.txt", "w", newline="\n") as fa, open("sets.txt", "w", newline="\n") as fs, \
        open("truth.tsv", "w", newline="\n") as ft:
    ft.write("gene\tclass\tn_var\tn_LoF\tn_missense\tcarriers_LoF\tcarriers_LoF_missense\n")
    for gname, g in genes.items():
        vs = sorted(g["vars"], key=lambda x: x[1])
        for r in vs:
            fa.write(f"{r[2]} {gname} {r[7]}\n")
        fs.write(f"{gname} {g['chrom']} {vs[0][1]} {','.join(r[2] for r in vs)}\n")
        car_l = sum(1 for i in range(N) if any(r[5][i] > 0 for r in vs if r[7] == "LoF"))
        car_lm = sum(1 for i in range(N) if any(r[5][i] > 0 for r in vs if r[7] in ("LoF", "missense")))
        ft.write(f"{gname}\t{g['class']}\t{len(vs)}\t{sum(r[7] == 'LoF' for r in vs)}\t"
                 f"{sum(r[7] == 'missense' for r in vs)}\t{car_l}\t{car_lm}\n")
        with open(f"gene_{gname}.tsv", "w", newline="\n") as fg:
            fg.write("\t".join(f"{r[2]}|{r[7]}" for r in vs) + "\n")
            for i in range(N):
                fg.write("\t".join(str(r[5][i]) for r in vs) + "\n")
with open("masks.txt", "w", newline="\n") as fh:
    fh.write("Mask_LoF LoF\nMask_LoF_mis LoF,missense\n")
print(f"cases {sum(Y)} / {N}; genes {len(genes)}; rare variants {len(wes_recs)}; array SNPs {len(array_recs)}")
