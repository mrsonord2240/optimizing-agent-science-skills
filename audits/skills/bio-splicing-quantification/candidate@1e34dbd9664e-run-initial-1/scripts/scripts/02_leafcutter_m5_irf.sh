#!/bin/bash
# Follow-up: leafcutter at -m 5 on XS vs non-XS junction files; IRFinder correct syntax on single-end FASTQ.
AS=/mnt/openscience/audit-envs/alternative-splicing; R=$AS/public-data/rnasplice
O=/mnt/openscience/audits/bio-splicing-quantification/run-initial-1/out
for v in lc_noxs lc_xs; do (cd $O/$v; bash $AS/tools/bin/leafcutter_cluster_regtools.py -j juncfiles.txt -o m5 -m 5 -l 500000 > m5.log 2>&1
  echo "$v -m 5 rc=$? clusters=$(($(zcat m5_perind.counts.gz 2>/dev/null | wc -l)-1))"); done
REF=$AS/logs/smoke_irfinder/ref
echo "-- IRFinder -m FastQ, single-end (Skill's sample.fastq shape)"
( time timeout 1200 bash $AS/tools/bin/IRFinder -m FastQ -r $REF -t 8 -d $O/irf/se $R/fastq/ERR188383_chrX_1.fastq.gz > $O/irf/se.log 2>&1 ); echo "rc=$?"
tail -3 $O/irf/se.log | cut -c1-200; ls $O/irf/se; echo "rows: $(($(wc -l < $O/irf/se/IRFinder-IR-nondir.txt)-1))"
