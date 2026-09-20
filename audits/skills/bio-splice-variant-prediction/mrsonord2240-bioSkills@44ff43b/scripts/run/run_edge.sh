#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1
AS=/mnt/openscience/audit-envs/alternative-splicing
FA=$AS/public-data/derived/X.fa; DB=$AS/public-data/derived/chrX_GRCh37_ensembl.gffutils.db
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
$AS/tools/bin/asenv as-spliceai python build_edge.py
for v in edge_grch37 edge_chr_prefixed; do
  echo "=== SpliceAI $v"; $AS/tools/bin/spliceai -I data/$v.vcf -O out/sai_$v.vcf -R $FA -A grch37 -D 50 -M 0 > out/sai_$v.log 2>&1; echo "rc=$?"
  grep -a -v "step\|pkg_resources\|get_distribution" out/sai_$v.log | tail -5 | cut -c1-300
  echo "-- output records"; grep -v '^##' out/sai_$v.vcf | cut -f2-5,8 | cut -c1-200
done
for v in edge_symbolic_DEL edge_star_allele; do
  echo "=== SpliceAI $v"; $AS/tools/bin/spliceai -I data/$v.vcf -O out/sai_$v.vcf -R $FA -A grch37 -D 50 -M 0 > out/sai_$v.log 2>&1; echo "rc=$?"
  grep -a -v "step\|pkg_resources\|get_distribution\|absl" out/sai_$v.log | tail -3 | cut -c1-200; echo "-- output records"; grep -v '^##' out/sai_$v.vcf | cut -f2-5,8 | cut -c1-200
done
echo "=== Pangolin edge"; $AS/tools/bin/pangolin data/edge_grch37.vcf $FA $DB out/pang_edge -d 50 -m True 2>&1 | grep -av pkg_resources | cut -c1-250
grep -v '^##' out/pang_edge.vcf | cut -f2-5,8 | cut -c1-200
echo "=== Pangolin chr-prefixed"; $AS/tools/bin/pangolin data/edge_chr_prefixed.vcf $FA $DB out/pang_edge_chr -d 50 -m True 2>&1 | grep -av pkg_resources | cut -c1-250
grep -v '^##' out/pang_edge_chr.vcf | cut -f2-5,8 | cut -c1-200
