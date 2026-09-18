#!/usr/bin/env bash
# Usage: run_magma_case.sh <case_dir>
set -uo pipefail
MAGMA="/f/OpenScience/audit-envs/mendelian-randomization-analyst/tools/magma/magma.exe"
BFILE="/f/OpenScience/audit-envs/mendelian-randomization-analyst/tools/magma/g1000_eur/g1000_eur"
CASE="$1"
cd "$CASE" || exit 1

"$MAGMA" --annotate window=35,10 \
  --snp-loc snp_loc.txt \
  --gene-loc gene_loc.txt \
  --out annot > annotate.log 2>&1

"$MAGMA" --bfile "$BFILE" \
  --pval gwas_sumstats.tsv ncol=N \
  --gene-annot annot.genes.annot \
  --out gene > genebased.log 2>&1

GENES_OUT="gene.genes.out"
if [ ! -f "$GENES_OUT" ] && [ -f "${GENES_OUT}.txt" ]; then
  cp "${GENES_OUT}.txt" "$GENES_OUT"
fi

N_GENES=$(grep -vc '^#' gene.genes.raw 2>/dev/null || echo "N/A")
echo "CASE=$CASE  genes.raw_count=$N_GENES"

if [ "$N_GENES" != "N/A" ] && [ "$N_GENES" -lt 200 ] 2>/dev/null; then
  echo "GUARD: would SKIP Step 3 (N_GENES=$N_GENES < 200)"
else
  echo "GUARD: would RUN Step 3 (N_GENES=$N_GENES >= 200) -- attempting real gene-set enrichment"
  "$MAGMA" --gene-results gene.genes.raw \
    --set-annot geneset.gmt \
    --out geneset > geneset.log 2>&1
  echo "Step 3 exit code: $?"
  tail -5 geneset.log
fi
