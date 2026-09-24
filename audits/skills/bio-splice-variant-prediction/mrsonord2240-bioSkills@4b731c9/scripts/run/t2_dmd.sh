#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
FA=/mnt/openscience/as-spvp-scratch/g38/hg38_chr17_chrX.upper.fa
for db in canon all; do for m in False True; do
 micromamba run -n as-pangolin pangolin data/dmd_sites.vcf $FA out/db_$db/gencode.v45.annotation.db out/dmd_${db}_m$m -d 50 -m $m > out/dmd_${db}_m$m.log 2>&1
 echo "dmd db=$db mask=$m rc=$? tagged=$(grep -c 'Pangolin=' out/dmd_${db}_m$m.vcf)"
done; done
