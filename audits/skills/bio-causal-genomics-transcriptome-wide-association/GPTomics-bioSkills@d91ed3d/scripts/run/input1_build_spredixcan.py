# Input 1 (canonical S-PrediXcan) builder.
# Reuses the SAME two planted SNPs/genes as Input 2's FUSION run (GENE1 = true signal at
# rs637471, GWAS Z=6.5; GENE2 = null at rs2786797) so S-PrediXcan's output can be checked
# directly against FUSION's already ground-truth-verified TWAS.Z = 6.500 / -0.557.
# Both tools implement a single-SNP top1-equivalent weighted-sum-of-Z model here, so an
# identical weight=1 single-SNP model should reproduce the same TWAS Z algebraically
# (modulo any variance/frequency correction S-PrediXcan applies from the covariance file).
import sqlite3, os

base = "F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association"
outdir = os.path.join(base, "data", "spredixcan")
os.makedirs(outdir, exist_ok=True)

# From data/fusion/wgt/GENE*.wgt.RDat and weights.pos (already built for Input 2):
# GENE1: rs637471, A1/A2 from bim row 500; GENE2: rs2786797, A1/A2 from bim row 7500.
# Read alleles straight from the LD reference .bim (same real genotype panel).
bim_path = os.path.join(base, "data", "fusion", "ld", "EUR.1.bim")
alleles = {}
with open(bim_path) as f:
    for line in f:
        chrom, snp, cm, pos, a1, a2 = line.split()
        if snp in ("rs637471", "rs2786797"):
            alleles[snp] = (a1, a2)
print("Alleles:", alleles)

db_path = os.path.join(outdir, "synthetic_model.db")
if os.path.exists(db_path):
    os.remove(db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("CREATE TABLE weights (rsid TEXT, gene TEXT, weight REAL, ref_allele TEXT, eff_allele TEXT)")
cur.execute("""CREATE TABLE extra (gene TEXT, genename TEXT, "n.snps.in.model" INTEGER,
               "pred.perf.R2" REAL, "pred.perf.pval" REAL, "pred.perf.qval" REAL)""")

a1_g1, a2_g1 = alleles["rs637471"]
a1_g2, a2_g2 = alleles["rs2786797"]
# eff_allele = A1 (matches GWAS file A1 below), ref_allele = A2. weight=1 (top1-equivalent).
cur.execute("INSERT INTO weights VALUES (?,?,?,?,?)", ("rs637471", "GENE1", 1.0, a2_g1, a1_g1))
cur.execute("INSERT INTO weights VALUES (?,?,?,?,?)", ("rs2786797", "GENE2", 1.0, a2_g2, a1_g2))
cur.execute("INSERT INTO extra VALUES (?,?,?,?,?,?)", ("GENE1", "GENE1", 1, 0.18, 1e-6, 1e-5))
cur.execute("INSERT INTO extra VALUES (?,?,?,?,?,?)", ("GENE2", "GENE2", 1, 0.09, 1e-3, 5e-3))
conn.commit()
conn.close()
print("Wrote", db_path)

# Covariance file: whitespace-delimited GENE RSID1 RSID2 VALUE. For a single-SNP model,
# the "covariance" is just the SNP's own variance -- use 1.0 (standardized genotype),
# consistent with GWAS Z/BETA/SE already expressed on a standardized scale in Input 2.
cov_path = os.path.join(outdir, "synthetic.cov.txt")
with open(cov_path, "w") as f:
    f.write("GENE RSID1 RSID2 VALUE\n")
    f.write("GENE1 rs637471 rs637471 1.0\n")
    f.write("GENE2 rs2786797 rs2786797 1.0\n")
print("Wrote", cov_path)

# GWAS file: reuse Input 2's gwas.sumstats (SNP A1 A2 Z BETA SE N) but add a P column,
# since the Skill's documented S-PrediXcan invocation passes --pvalue_column P.
import scipy.stats as st
src = os.path.join(base, "data", "fusion", "gwas.sumstats")
dst = os.path.join(outdir, "gwas.sumstats.p.txt")
with open(src) as fin, open(dst, "w") as fout:
    header = fin.readline().split()
    header.append("P")
    fout.write("\t".join(header) + "\n")
    for line in fin:
        parts = line.split()
        z = float(parts[3])
        p = 2 * st.norm.sf(abs(z))
        fout.write("\t".join(parts) + f"\t{p:.6g}\n")
print("Wrote", dst)
