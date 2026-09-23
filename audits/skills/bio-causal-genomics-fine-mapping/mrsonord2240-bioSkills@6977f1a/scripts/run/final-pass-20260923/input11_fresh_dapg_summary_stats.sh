#!/usr/bin/env bash
# Final-pass: verify a DAP-G worked example built from the same synthetic
# FINEMAP locus (locus.z / locus.ld from run_finemap_test.sh), since DAP-G's
# -d_z/-d_ld summary-stat mode takes the same shape of input as FINEMAP/susie_rss.
set -euo pipefail
DAPG=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools/finemapping/dap/dap_src/dap-g
cd /mnt/openscience/audits/bio-causal-genomics-fine-mapping/run/final-pass-20260923/finemap_cli_run

# --- Reformat the existing locus.z / locus.ld (FINEMAP format) into DAP-G's
#     -d_z (snp_id z) / -d_ld (headerless square matrix) format ---
awk 'NR>1{z=$7/$8; print $1, z}' locus.z > dapg.zval.dat
tail -n +1 locus.ld > dapg.LD.dat   # already headerless, space-separated

wc -l dapg.zval.dat dapg.LD.dat

set +e
"$DAPG" -d_z dapg.zval.dat -d_ld dapg.LD.dat -t 4 > dapg_out.txt 2>&1
RC=$?
set -e
echo "dap-g exit code: $RC (expected 1 despite usable output)"

echo "=== Independent association signal clusters ==="
grep -A 20 "Independent association signal clusters" dapg_out.txt

CAUSAL_SNP=$(awk 'NR==150{print $2}' panel.bim)
echo "=== Planted causal SNP: $CAUSAL_SNP -- its PIP line ==="
grep -w "$CAUSAL_SNP" dapg_out.txt || echo "not found in output"
