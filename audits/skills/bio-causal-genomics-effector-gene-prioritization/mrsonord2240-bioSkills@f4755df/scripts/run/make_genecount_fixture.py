"""
Independent (auditor-built) fixture generator for testing the MAGMA gene-count
guard in examples/magma_genebased.sh at gene counts other than the fixer's own
3-gene and the pre-fix audit's 5-gene tests.

Builds N equal-width synthetic gene bins across a real 1000G EUR chr1 window
(same methodology as the Skill's own examples/make_toy_fixture.py: real SNP
identities/positions from the real g1000_eur.bim, arbitrary bin boundaries
since no real NCBI37.3 gene.loc reference is staged in this environment).

Usage: python make_genecount_fixture.py <n_genes> <start_bp> <end_bp> <out_dir>
"""
import sys
import numpy as np
import pandas as pd

n_genes = int(sys.argv[1])
start_bp = int(sys.argv[2])
end_bp = int(sys.argv[3])
out_dir = sys.argv[4]

BIM_PATH = r"F:\OpenScience\audit-envs\mendelian-randomization-analyst\tools\magma\g1000_eur\g1000_eur.bim"

rng = np.random.default_rng(1234 + n_genes)

bim = pd.read_csv(BIM_PATH, sep=r"\s+", header=None,
                   names=["CHR", "SNP", "CM", "BP", "A1", "A2"])
bim = bim[(bim.CHR == 1) & (bim.BP >= start_bp) & (bim.BP <= end_bp)].reset_index(drop=True)
print(f"Loaded {len(bim)} real reference SNPs in chr1:{start_bp}-{end_bp}")

edges = np.linspace(start_bp, end_bp, n_genes + 1).astype(int)
genes = pd.DataFrame({
    "GENE": [f"SYNGENE{i+1:04d}" for i in range(n_genes)],
    "CHR": 1,
    "START": edges[:-1],
    "STOP": edges[1:] - 1,
})
genes["STRAND"] = "+"
genes.to_csv(f"{out_dir}/gene_loc.txt", sep="\t", header=False, index=False,
             columns=["GENE", "CHR", "START", "STOP", "STRAND", "GENE"])
print(f"Wrote gene_loc.txt: {n_genes} synthetic gene bins")

# Random p-values, no planted signal needed -- this test is about the gene-count
# guard and MAGMA's own degrees-of-freedom behavior, not effector-gene recovery.
p = rng.uniform(1e-6, 1.0, size=len(bim))
sumstats = pd.DataFrame({
    "SNP": bim.SNP, "CHR": bim.CHR, "BP": bim.BP,
    "A1": bim.A1, "A2": bim.A2, "P": p, "N": 100000,
})
sumstats.to_csv(f"{out_dir}/gwas_sumstats.tsv", sep="\t", index=False)
sumstats[["SNP", "CHR", "BP"]].to_csv(f"{out_dir}/snp_loc.txt", sep="\t", header=False, index=False)
print(f"Wrote gwas_sumstats.tsv / snp_loc.txt: {len(bim)} SNPs")

# Gene-set file for Step 3 testing: split genes into two arbitrary sets (odd/even
# index) purely to give MAGMA's --set-annot competitive regression something to
# test -- not a biologically meaningful pathway.
odd = [g for i, g in enumerate(genes.GENE) if i % 2 == 0]
even = [g for i, g in enumerate(genes.GENE) if i % 2 == 1]
with open(f"{out_dir}/geneset.gmt", "w") as f:
    f.write("SET_ODD\t" + "\t".join(odd) + "\n")
    f.write("SET_EVEN\t" + "\t".join(even) + "\n")
print(f"Wrote geneset.gmt: SET_ODD ({len(odd)} genes), SET_EVEN ({len(even)} genes)")
