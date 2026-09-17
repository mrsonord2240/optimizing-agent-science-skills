"""
Minimal synthetic PoPS inputs to exercise pops.py's real ridge-regression code path
end-to-end (not just inspected). Uses the real magma_gene.genes.raw produced by MAGMA
in this same audit run as the --magma_prefix input (real MAGMA output format, real gene
Z-scores/correlations for our 5-gene synthetic locus). The feature matrix itself is
synthetic (toy 3-feature matrix) -- PoPS normally needs the ~50k-feature FinucaneLab
matrix (multi-GB download, out of scope for this audit); this only tests that pops.py's
parsing + ridge-regression fitting machinery runs without error on a well-formed input
of the documented shape.
"""
import numpy as np

genes = ["SYNGENE_A", "USP24", "SYNGENE_C", "PCSK9", "SYNGENE_E"]

# Gene annotation: ENSGID, CHR, TSS (toy IDs reused from the MAGMA run so genes.raw matches)
with open("pops_gene_annot.txt", "w") as f:
    f.write("ENSGID\tCHR\tTSS\n")
    tss = {"SYNGENE_A": 54900000, "USP24": 55158183, "SYNGENE_C": 55350000,
           "PCSK9": 55505221, "SYNGENE_E": 55530526}
    for g in genes:
        f.write(f"{g}\t1\t{tss[g]}\n")

# Toy feature matrix: 3 synthetic pathway-membership-like features.
# Feature 3 ("lipid_pathway") is given a strong synthetic signal for PCSK9 to check
# that PoPS's ridge fit assigns it a non-trivial coefficient.
rng = np.random.default_rng(7)
mat = rng.normal(0, 1, size=(5, 3))
mat[genes.index("PCSK9"), 2] = 4.0  # lipid_pathway feature spikes for the true effector

np.savetxt("pops_feat.rows.txt", np.array(genes), fmt="%s")
np.savetxt("pops_feat.cols.0.txt", np.array(["feature_ppi", "feature_coexpr", "lipid_pathway"]), fmt="%s")
np.save("pops_feat.mat.0.npy", mat)

with open("pops_control_features.txt", "w") as f:
    f.write("feature_ppi\n")

print("Wrote pops_gene_annot.txt, pops_feat.{rows,cols.0,mat.0}, pops_control_features.txt")
