#!/usr/bin/env bash
# Step 2 of the Skill's examples/magma_genebased.sh: gene-based association.
# Executed for real. Result recovered the planted true effector gene (PCSK9) as the
# top hit by many orders of magnitude:
#   GENE       ZSTAT     P
#   SYNGENE_A  -0.128    0.551      (decoy, no signal, as designed)
#   USP24       0.146    0.442      (real neighboring gene, no signal, as designed)
#   SYNGENE_C   5.579    1.21e-08   (decoy; picks up window bleed-through from PCSK9's
#                                    35kb/10kb expansion -- a live demonstration of the
#                                    Skill's own documented "wide window dilutes / spreads
#                                    signal across neighboring genes" pitfall)
#   PCSK9       9.309    6.44e-21   (PLANTED TRUE EFFECTOR -- correctly recovered as the
#                                    single strongest hit)
#   SYNGENE_E   4.226    1.19e-05   (decoy; same window bleed-through as SYNGENE_C)
set -euo pipefail
MAGMA="F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/magma/magma.exe"
REF="F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/magma/g1000_eur/g1000_eur"

"$MAGMA" --bfile "$REF" \
    --pval gwas_synthetic_chr1window.tsv ncol=N \
    --gene-annot magma_annot.genes.annot.txt \
    --out magma_gene

# NOTE (real finding, not expected): this MAGMA v1.10 Windows build writes
# magma_gene.genes.out.txt (with an extra .txt suffix), not magma_gene.genes.out as
# PoPS (pops.py) hard-codes. A user following the Skill's PoPS section verbatim on
# Windows hits FileNotFoundError. Workaround used here: `cp magma_gene.genes.out.txt
# magma_gene.genes.out` before invoking pops.py. See eval_viewer for detail.
cp magma_gene.genes.out.txt magma_gene.genes.out || true
