import sqlite3, os, shutil

base = "F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association"
d = os.path.join(base, "data", "smultixcan")
models_dir = os.path.join(d, "models")
mx_dir = os.path.join(d, "metaxcan_out")
os.makedirs(models_dir, exist_ok=True)
os.makedirs(mx_dir, exist_ok=True)

def make_db(path, w1, w2):
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE weights (rsid TEXT, gene TEXT, weight REAL, ref_allele TEXT, eff_allele TEXT)")
    cur.execute("""CREATE TABLE extra (gene TEXT, genename TEXT, "n.snps.in.model" INTEGER,
                   "pred.perf.R2" REAL, "pred.perf.pval" REAL, "pred.perf.qval" REAL)""")
    cur.execute("INSERT INTO weights VALUES (?,?,?,?,?)", ("rs637471", "GENE1", w1, "C", "T"))
    cur.execute("INSERT INTO weights VALUES (?,?,?,?,?)", ("rs2786797", "GENE2", w2, "A", "G"))
    cur.execute("INSERT INTO extra VALUES (?,?,?,?,?,?)", ("GENE1", "GENE1", 1, 0.18, 1e-6, 1e-5))
    cur.execute("INSERT INTO extra VALUES (?,?,?,?,?,?)", ("GENE2", "GENE2", 1, 0.09, 1e-3, 5e-3))
    conn.commit()
    conn.close()

# Two "tissues": Tissue1 identical to Input1's model; Tissue2 uses a partially independent
# weight (0.7) to avoid a perfectly-collinear (singular) 2-tissue system, while still being a
# realistic near-duplicate cross-tissue model for the same cis-eQTL SNP -- the actual scenario
# the Skill's own taxonomy table calls out as an S-MultiXcan failure mode ("correlated tissues
# produce ill-conditioned regression").
make_db(os.path.join(models_dir, "Tissue1.db"), 1.0, 1.0)
make_db(os.path.join(models_dir, "Tissue2.db"), 0.7, 0.7)

# snp covariance per tissue-gene (GENE RSID1 RSID2 VALUE) -- reuse variance=1.0 for both SNPs.
cov_path = os.path.join(d, "snp_covariance.txt")
with open(cov_path, "w") as f:
    f.write("GENE RSID1 RSID2 VALUE\n")
    f.write("GENE1 rs637471 rs637471 1.0\n")
    f.write("GENE2 rs2786797 rs2786797 1.0\n")

print("Built models + covariance for S-MultiXcan Input 4.")
