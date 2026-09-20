#!/bin/bash
# Skill veto T1/T3: 10 consecutive runs each of the shipped script and the main recipes; success count and distinct-output count (deterministic => 1).
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work
B=$AFDATA/human/test.paired_end.sorted.bam; ok=0
for i in $(seq 1 10); do python $R/skill/examples/qc_report.py $B > qr_$i.txt 2>&1 && ok=$((ok+1)); done
echo "qc_report.py: $ok/10 rc=0; distinct outputs: $(md5sum qr_*.txt | cut -d' ' -f1 | sort -u | wc -l)"
for i in $(seq 1 10); do samtools depth -aa $B | awk '{s+=$3;n++; if($3>=10)c10++} END{printf "%.6f %.6f\n", s/n, c10/n*100}'; done | sort -u | wc -l | sed 's/^/depth -aa recipe distinct outputs: /'
for i in $(seq 1 10); do samtools flagstat -O tsv $B | md5sum; done | sort -u | wc -l | sed 's/^/flagstat distinct outputs: /'
for i in $(seq 1 10); do python $R/t4_helper.py $B chr22 40001 0 40001 1951 4617 | md5sum; done | sort -u | wc -l | sed 's/^/region_depth_stats distinct outputs: /'
rm -f qr_*.txt
