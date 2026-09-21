#!/bin/bash
# Input 2: Pangolin exactly as SKILL.md "Pangolin" section. Env as-pangolin (Pangolin 1.0.2, torch 2.13 CPU). GRCh38, GENCODE v45.
export PYTHONDONTWRITEBYTECODE=1
R=/mnt/openscience/audits/bio-splice-variant-prediction/run
G=/mnt/openscience/as-spvp-scratch/g38
FA=$G/hg38_chr17_chrX.upper.fa
cd $R; mkdir -p out/db_canon out/db_all
run() { micromamba run -n as-pangolin "$@"; }
# --- annotation DBs with the Skill's command (create_db.py), on a copy of the chr17+chrX GENCODE v45 GTF
cp $G/gencode.v45.chr17_X.gtf out/db_canon/gencode.v45.annotation.gtf
cp $G/gencode.v45.chr17_X.gtf out/db_all/gencode.v45.annotation.gtf
( cd out/db_canon && /usr/bin/time -f "create_db canonical %es" micromamba run -n as-pangolin create_db.py gencode.v45.annotation.gtf 2>&1 | tail -3; ls -la )
( cd out/db_all && /usr/bin/time -f "create_db --filter None %es" micromamba run -n as-pangolin create_db.py gencode.v45.annotation.gtf --filter None 2>&1 | tail -3; ls -la )
# --- Skill commands
V=data/panel_grch38_auditor.vcf
for db in canon all; do
  for m in False True; do
    run pangolin $V $FA out/db_$db/gencode.v45.annotation.db out/pang38_${db}_m$m -d 50 -m $m > out/pang38_${db}_m$m.log 2>&1
    echo "db=$db mask=$m rc=$? out_records=$(grep -vc '^#' out/pang38_${db}_m$m.vcf) tagged=$(grep -c 'Pangolin=' out/pang38_${db}_m$m.vcf)"
  done
done
# the D500 -s 0.2 line from SKILL.md (mask False)
run pangolin $V $FA out/db_canon/gencode.v45.annotation.db out/pang38_canon_d500_s02 -d 500 -m False -s 0.2 > out/pang38_canon_d500_s02.log 2>&1; echo "d500 s0.2 rc=$? tagged=$(grep -c 'Pangolin=' out/pang38_canon_d500_s02.vcf)"
# the SKILL.md warning: gffutils.create_db on GFF3 -> Duplicate ID CDS
