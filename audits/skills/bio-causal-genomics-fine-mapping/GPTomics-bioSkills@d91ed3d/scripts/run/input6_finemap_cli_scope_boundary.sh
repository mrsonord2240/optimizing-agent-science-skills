#!/usr/bin/env bash
# Input 6 (Scope Boundary) -- "Independently confirm my susie_rss credible set at this locus
# with FINEMAP's shotgun stochastic search (--sss), then reconcile any disagreement."
#
# NOT EXECUTED. FINEMAP is a Linux/macOS-only binary distributed from christianbenner.com with
# no Windows build (confirmed: no `finemap` binary anywhere on this machine or in the audit env's
# tools/ directory, which does hold plink2, magma, and smr Windows builds -- FINEMAP is absent
# because none exists for this platform). SuSiEx, PAINTOR, and DAP-G are the same story (C/C++
# CLI tools built from source on POSIX; not present here either). This is exactly the platform
# gap the audit brief anticipates ("Command-line tools that have no Windows build ... will
# usually not run here").
#
# What was verified instead (2026-09-17, WebSearch against public FINEMAP documentation --
# hongchengyao.github.io/fine-mapping_document/FINEMAP/, christianbenner.com):
#   - `--sss` (shotgun stochastic search), `--n-causal-snps`, `--prob-tol`, `--n-iterations`,
#     `--n-convergence` are all real, current FINEMAP 1.4.x flags with the meanings SKILL.md
#     ascribes to them.
#   - The master file column order (z;ld;snp;config;cred;log;n_samples) matches FINEMAP's
#     documented master-file spec.
#   - FINEMAP's `--sss` mode is genuinely a stochastic search (no --seed flag is documented by
#     FINEMAP itself) -- SKILL.md does not flag this as a determinism caveat anywhere, even
#     though it flags determinism carefully everywhere else (susie_rss seeding, IBSS convergence).
#
# The command below is exactly what an agent following SKILL.md + examples/finemap_pipeline.sh
# would construct for the user's stated locus. It is syntactically valid against the real CLI
# but is NOT run here (no binary on this machine).

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
