#!/usr/bin/env bash
# Fresh Phase 2 execution of the current branch's shipped GCTA-GREML example.
# A deterministic synthetic quantitative phenotype is paired with the public 957-person test panel.
# Usage: bash run_gcta_example.sh
set -euo pipefail

RUN=/mnt/openscience/audits/bio-causal-genomics-heritability-partitioning/run/finalpass_20260923
OUT="$RUN/out/input10_gcta"
SKILL=/mnt/openscience/wt/causal-genomics-heritability-partitioning/causal-genomics/heritability-partitioning
PANEL=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools/src/plink2R/data
mkdir -p "$OUT"

awk '{printf "%s %s %.6f\n", $1, $2, ((NR % 17) - 8) / 4.0}' "$PANEL.fam" > "$OUT/synthetic_quantitative.phen"
test "$(wc -l < "$OUT/synthetic_quantitative.phen")" -eq 957
cp "$SKILL/examples/gcta_greml.sh" "$RUN/input10_gcta_greml.sh"
export PATH="/home/sci/micromamba/envs/cg-hp-gcta/bin:$PATH"
bash "$RUN/input10_gcta_greml.sh" "$PANEL" "$OUT/synthetic_quantitative.phen" "$OUT/gcta"
grep -E '^V\(G\)/Vp|^V\(e\)/Vp|^n:' "$OUT/gcta_h2.hsq"
echo 'FRESH_GCTA_EXAMPLE_COMPLETE'
