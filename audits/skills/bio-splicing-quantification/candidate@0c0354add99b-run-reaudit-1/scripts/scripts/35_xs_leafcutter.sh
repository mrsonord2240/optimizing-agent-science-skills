#!/bin/bash
# SQ-04: regtools/leafcutter route per the Skill text, untagged vs XS-tagged BAMs, incl. the Skill's own strand-check command.
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing; D=$AS/public-data; R=$D/rnasplice
O=/mnt/openscience/audits/bio-splicing-quantification/run-reaudit-1/out; CB=/home/sci/micromamba/envs/as-core/bin
LC=$AS/tools/bin/leafcutter_cluster_regtools.py
mkdir -p $O/lc_noxs $O/lc_xs
for s in ERR188383 ERR188428 ERR188454 ERR204916; do
  $CB/regtools junctions extract -a 8 -m 50 -s XS $R/bam/$s.Aligned.out.bam -o $O/lc_noxs/$s.junc 2> $O/lc_noxs/$s.err
  $CB/regtools junctions extract -a 8 -m 50 -s XS $D/derived/xs_bams/$s.xs.bam -o $O/lc_xs/$s.junc 2> $O/lc_xs/$s.err
done
for v in lc_noxs lc_xs; do
  cd $O/$v
  echo "== $v: Skill's strand check (tail -n +2 s.junc | cut -f6 | sort | uniq -c)"
  for f in ERR188383.junc ERR188454.junc; do echo "$f: $(tail -n +2 $f | cut -f6 | sort | uniq -c | tr '\n' ' ')"; done
  ls *.junc > juncfiles.txt
  bash $LC -j juncfiles.txt -o leafcutter -m 50 -l 500000 > cluster50.log 2>&1; echo "$v -m 50 rc=$? clusters=$(($(zcat leafcutter_perind.counts.gz 2>/dev/null | wc -l)-1))"
  bash $LC -j juncfiles.txt -o m5 -m 5 -l 500000 > cluster5.log 2>&1; echo "$v -m 5 rc=$? clusters=$(($(zcat m5_perind.counts.gz 2>/dev/null | wc -l)-1))"
done
