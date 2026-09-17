"""
Synthetic GWAS summary statistics for a MAGMA gene-based test.
Region: chr1:54,900,000-55,700,000 (hg19/GRCh37), matching MAGMA's g1000_eur reference build.
This region genuinely spans the real PCSK9 locus (chr1:55,505,221-55,530,525, hg19), a canonical
LDL-cholesterol GWAS effector gene. SNP identities and positions are REAL (drawn from the actual
1000 Genomes EUR reference .bim shipped with MAGMA); the GWAS p-values are SYNTHETIC, with a planted
signal concentrated in and around PCSK9 so the "true" effector gene is known in advance.
All other gene bins in this window are decoys with null (uniform) p-values.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

bim = pd.read_csv(
    "chr1_window.bim", sep=r"\s+", header=None,
    names=["CHR", "SNP", "CM", "BP", "A1", "A2"]
)
print(f"Loaded {len(bim)} real reference SNPs in chr1:54.9-55.7Mb window")

# Synthetic gene bins (approximate; PCSK9 coordinates are the real hg19 locus)
genes = pd.DataFrame([
    {"GENE": "SYNGENE_A", "CHR": 1, "START": 54900000, "STOP": 55100000},
    {"GENE": "USP24",     "CHR": 1, "START": 55158183, "STOP": 55349999},  # real neighboring gene
    {"GENE": "SYNGENE_C", "CHR": 1, "START": 55350000, "STOP": 55505000},
    {"GENE": "PCSK9",     "CHR": 1, "START": 55505221, "STOP": 55530525},  # planted true effector (real coords)
    {"GENE": "SYNGENE_E", "CHR": 1, "START": 55530526, "STOP": 55700000},
])
genes["STRAND"] = "+"
genes.to_csv(
    "gene_loc_chr1_window.txt", sep="\t", header=False, index=False,
    columns=["GENE", "CHR", "START", "STOP", "STRAND", "GENE"]
)
print("Wrote gene_loc_chr1_window.txt (5 gene bins, MAGMA --gene-loc format)")

# Planted signal window: PCSK9 body +/- 35kb upstream / 10kb downstream (FUMA MAGMA window convention)
sig_lo, sig_hi = 55505221 - 35000, 55530525 + 10000
in_signal = (bim.BP >= sig_lo) & (bim.BP <= sig_hi)
print(f"SNPs inside planted PCSK9 signal window ({sig_lo}-{sig_hi}): {in_signal.sum()}")

n = len(bim)
p = np.empty(n)
# Null background: uniform p-values
p[~in_signal.values] = rng.uniform(1e-4, 1.0, size=(~in_signal).sum())
# Planted signal: small p-values (chi-sq(1) tail from a real-ish effect size draw)
z_signal = rng.normal(loc=6.5, scale=1.2, size=in_signal.sum())  # strong mean Z ~ 6.5
from scipy.stats import norm
p_signal = 2 * norm.sf(np.abs(z_signal))
p[in_signal.values] = np.clip(p_signal, 1e-300, 1.0)

sumstats = pd.DataFrame({
    "SNP": bim.SNP, "CHR": bim.CHR, "BP": bim.BP,
    "A1": bim.A1, "A2": bim.A2, "P": p, "N": 100000,
})
sumstats.to_csv("gwas_synthetic_chr1window.tsv", sep="\t", index=False)
print("Wrote gwas_synthetic_chr1window.tsv:", sumstats.shape)
print("Min p overall:", sumstats.P.min(), "at SNP", sumstats.loc[sumstats.P.idxmin(), "SNP"],
      "BP", sumstats.loc[sumstats.P.idxmin(), "BP"])

# SNP-loc file for MAGMA --annotate (SNP CHR BP, no header)
sumstats[["SNP", "CHR", "BP"]].to_csv("gwas_synthetic.snploc", sep="\t", header=False, index=False)
print("Wrote gwas_synthetic.snploc")
