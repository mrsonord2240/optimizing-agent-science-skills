#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
smr="F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/smr/smr-1.3.1-win-x86_64/smr-1.3.1-win.exe"
plink="F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/plink2/plink2.exe"
cd "$here/input5_smr/smr_test"
"$plink" --pedmap ./ref --make-bed --out ./ref_bed
"$smr" --eqtl-flist ./eqtl_shared.flist --make-besd --out ./eqtl_shared_besd
"$smr" --eqtl-flist ./eqtl_linkage.flist --make-besd --out ./eqtl_linkage_besd
"$smr" --bfile ./ref_bed --gwas-summary ./gwas.ma --beqtl-summary ./eqtl_shared_besd --out ./result_shared --peqtl-smr 5e-8 --heidi-mtd 1
"$smr" --bfile ./ref_bed --gwas-summary ./gwas.ma --beqtl-summary ./eqtl_linkage_besd --out ./result_linkage --peqtl-smr 5e-8 --heidi-mtd 1
awk 'NR==1 || NR==2 {print}' result_shared.smr
awk 'NR==1 || NR==2 {print}' result_linkage.smr
