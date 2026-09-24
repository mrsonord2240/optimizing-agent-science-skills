#!/bin/bash
# NEW input: Pangolin per the SKILL.md commands on the CFTR/BRCA1 panel: create_db.py on the chr7+chr17 GENCODE v45 GTF (canonical default), -m False and -m True.
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
S=/mnt/openscience/as-spvp-reaudit-scratch; FA=$S/hg38_chr7_chr17.upper.fa
mkdir -p out/db_new && cp $S/gencode.v45.chr7_17.gtf out/db_new/gencode.v45.annotation.gtf
( cd out/db_new && /usr/bin/time -f "create_db canonical %es" micromamba run -n as-pangolin create_db.py gencode.v45.annotation.gtf 2>&1 | tail -2 )
for m in False True; do
  micromamba run -n as-pangolin pangolin data/panel_new_grch38.vcf $FA out/db_new/gencode.v45.annotation.db out/pang_new_m$m -d 50 -m $m > out/pang_new_m$m.log 2>&1
  echo "pangolin new mask=$m rc=$? tagged=$(grep -c 'Pangolin=' out/pang_new_m$m.vcf)"
done
micromamba run -n as-pangolin pangolin data/panel_new_grch38.vcf $FA out/db_new/gencode.v45.annotation.db out/pang_new_d500 -d 500 -m False -s 0.2 > out/pang_new_d500.log 2>&1; echo "d500 rc=$?"
