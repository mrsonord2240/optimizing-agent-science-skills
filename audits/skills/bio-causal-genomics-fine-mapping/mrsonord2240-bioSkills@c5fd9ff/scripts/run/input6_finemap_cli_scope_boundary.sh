#!/usr/bin/env bash
# REGRESSION of pre-fix audit Input 6 (Scope Boundary) -- "Independently confirm my susie_rss
# credible set at this locus with FINEMAP's shotgun stochastic search (--sss), then reconcile any
# disagreement."
#
# NOT EXECUTED, same as pre-fix. Re-confirmed 2026-09-17 against this fixed Skill's audit env: no
# `finemap`, `SuSiEx`, `PAINTOR`, or `dap-g` binary exists anywhere on PATH or under
# audit-envs/mendelian-randomization-analyst/tools/ (which does hold Windows plink2/magma/smr
# builds, and now also a full PolyFun Python clone -- see input8). `which finemap`, `which
# SuSiEx`, `which PAINTOR`, `which dap-g` all report "not found"; a filesystem search for
# *finemap* under tools/ only turns up PolyFun's own finemapper.py (a different, Python-based
# fine-mapper bundled with PolyFun, not the FINEMAP C++ CLI this input targets).
#
# THE FIX BEING REGRESSION-TESTED HERE: the pre-fix audit's P1 finding was "no platform caveat
# that FINEMAP/SuSiEx/PAINTOR/DAP-G are POSIX-only". SKILL.md now carries (confirmed by direct
# read, 2026-09-17, line 31, immediately after the tool-invocation list and before the
# Algorithmic Taxonomy table):
#   "Platform note: FINEMAP, SuSiEx, PAINTOR, and DAP-G are POSIX (Linux/macOS) command-line
#   binaries with no native Windows build. On Windows, run them under WSL, or use `susie_rss` /
#   SuSiE-inf as the equivalent inference path."
# This directly fixes the P1: an agent on Windows now learns the platform limitation from
# SKILL.md itself, at first mention, rather than discovering it only after a failed install.
#
# CLI flags and master-file format are unchanged from the pre-fix audit and were already verified
# correct against real FINEMAP 1.4.x documentation (hongchengyao.github.io/fine-mapping_document/
# FINEMAP/, christianbenner.com) -- not re-verified here since SKILL.md's FINEMAP CLI Pattern
# section text is byte-identical to the pre-fix version (the fix touched only the Coloc.susie
# Integration and the new Platform note, not this section).

set -euo pipefail

GWAS_FILE="locus_gwas.txt"     # SNP CHR POS A1 A2 MAF BETA SE, from the user's harmonized sumstats
REF_PANEL="1000G_EUR"
CHR=6
START=30000000
END=31000000
N_SAMPLES=300000
N_CAUSAL=5

awk -v chr="$CHR" -v start="$START" -v end="$END" \
  '$2 == chr && $3 >= start && $3 <= end' "$GWAS_FILE" > locus_gwas_window.txt
awk '{print $1}' locus_gwas_window.txt > locus_snps.txt

plink --bfile "$REF_PANEL" --chr "$CHR" --from-bp "$START" --to-bp "$END" \
  --extract locus_snps.txt --r square --out locus_ld
mv locus_ld.ld locus.ld

echo "rsid chromosome position allele1 allele2 maf beta se" > locus.z
awk -v OFS=" " '{print $1, $2, $3, $4, $5, $6, $7, $8}' locus_gwas_window.txt >> locus.z

cat > master.txt << EOF
z;ld;snp;config;cred;log;n_samples
locus.z;locus.ld;locus.snp;locus.config;locus.cred;locus.log;${N_SAMPLES}
EOF

finemap --sss --in-files master.txt --n-causal-snps "$N_CAUSAL" --prob-tol 0.001

echo "=== Reconcile against susie_rss per SKILL.md's Reconciliation table ==="
echo "If FINEMAP's .cred disagrees with the susie_rss fit already run (see input1/input3/input5"
echo "of this audit): check susie purity (< 0.5 => spurious), raise FINEMAP --n-iterations, and"
echo "report the INTERSECTION of high-PIP variants from both methods as the primary candidates,"
echo "per SKILL.md 'Reconciliation: When Methods Disagree'."
