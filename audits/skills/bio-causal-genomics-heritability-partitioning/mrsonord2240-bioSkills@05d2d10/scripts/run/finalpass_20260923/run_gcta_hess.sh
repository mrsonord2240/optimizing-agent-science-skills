#!/usr/bin/env bash
# Fresh Phase 2 runs of the current branch's shipped GCTA-GREML and HESS examples.
# Inputs: existing public test panel and the isolated cg-hp-gcta environment.
# Usage: bash run_gcta_hess.sh
set -euo pipefail

RUN=/mnt/openscience/audits/bio-causal-genomics-heritability-partitioning/run/finalpass_20260923
OUT="$RUN/out"
TOOLS=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools
SKILL=/mnt/openscience/wt/causal-genomics-heritability-partitioning/causal-genomics/heritability-partitioning
PANEL="$TOOLS/src/plink2R/data"
mkdir -p "$OUT/input10_gcta" "$OUT/input11_hess"

echo '=== Input 10: current GCTA-GREML example on real genotypes + planted phenotype ==='
python3 "$TOOLS/gcta_make_pheno.py" "$OUT/input10_gcta"
cp "$SKILL/examples/gcta_greml.sh" "$RUN/input10_gcta_greml.sh"
export PATH="/home/sci/micromamba/envs/cg-hp-gcta/bin:$PATH"
bash "$RUN/input10_gcta_greml.sh" "$PANEL" "$OUT/input10_gcta/pheno.phen" "$OUT/input10_gcta/gcta"
grep -E 'V\(G\)/Vp|Sum of|n:' "$OUT/input10_gcta/gcta_h2.hsq"

echo '=== Input 11: current HESS local-h2 example on a real chr1 panel + planted phenotype ==='
python3 "$TOOLS/hess_make_test.py" "$OUT/input11_hess"
awk '$1 == 1' "$PANEL.bim" > "$OUT/input11_hess/chr1.bim"
cp "$SKILL/examples/hess_local_h2.sh" "$RUN/input11_hess_local_h2.sh"
HESS_DIR="$TOOLS/hess" bash "$RUN/input11_hess_local_h2.sh" "$OUT/input11_hess/sumstats.txt" 1 "$OUT/input11_hess/chr1" "$OUT/input11_hess/partition.bed" "$OUT/input11_hess/hess"
test -s "$OUT/input11_hess/hess_chr1.info.gz"
test -s "$OUT/input11_hess/hess_chr1.eig.gz"
test -s "$OUT/input11_hess/hess_chr1.prjsq.gz"
echo 'HESS_STEP1_OUTPUTS_PRESENT'

echo 'FRESH_GCTA_HESS_COMPLETE'
