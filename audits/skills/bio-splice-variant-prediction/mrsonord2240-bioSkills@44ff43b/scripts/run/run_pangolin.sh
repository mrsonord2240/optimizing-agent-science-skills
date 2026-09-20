#!/bin/bash
# Pangolin as the Skill directs: pangolin input.vcf genome.fa gencode.db out -d 500 -m True -s 0.2  (+ default-ish variants). chrX GRCh37 Ensembl DB.
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1
R=/mnt/openscience/audits/bio-splice-variant-prediction/run
AS=/mnt/openscience/audit-envs/alternative-splicing
FA=$AS/public-data/derived/X.fa
DB=$AS/public-data/derived/chrX_GRCh37_ensembl.gffutils.db
cd $R
$AS/tools/bin/pangolin data/panel_grch37.vcf $FA $DB out/pang_skill_d500_m1_s02 -d 500 -m True -s 0.2 > out/pang_skill_d500_m1_s02.log 2>&1; echo "skill cmd rc=$?"
$AS/tools/bin/pangolin data/panel_grch37.vcf $FA $DB out/pang_d50_mF -d 50 -m False > out/pang_d50_mF.log 2>&1; echo "d50 mask False rc=$?"
$AS/tools/bin/pangolin data/panel_grch37.vcf $FA $DB out/pang_d50_mT -d 50 -m True > out/pang_d50_mT.log 2>&1; echo "d50 mask True rc=$?"
ls out | grep pang
