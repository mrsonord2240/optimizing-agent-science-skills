#!/bin/bash
# INPUT 3 (Edge; regression of pre-fix input 3 + NEW edge BAMs): planted flag categories; qc_report.py and block 027 vs flagstat -O tsv, hand counts, and counts planted by construction
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work
S=$R/data/synth.bam; D=/mnt/openscience/audit-envs/alignment-files/public-data
echo "=== planted truth (synth.bam)"; head -c 500 $R/data/synth.truth.json; echo
echo "=== check_counts.py: tools vs hand counts + the Skill's cross-check identity (Skill now says pass+fail)"; python $R/check_counts.py $S 2>&1 | grep -E '^(PASS|FAIL|SKILL|SUMMARY)'
echo "=== qc_report.py + block 027 vs flagstat -O tsv (QC-passed col, %) and hand counts, on 18 BAMs: synth, real human, real 1000G, ARTIC, RNA, planted dups, SE, empty, 9 NEW edge BAMs"
python $R/t3_qc_vs_flagstat.py $S $D/human/test.paired_end.sorted.bam $D/1000g/HG00349.chr20_1400000-1500000.bam $D/sarscov2/sars-cov-2_v5.3.2.nanopore.bam $D/human/test.rna.paired_end.sorted.bam $D/derived/planted_dups.bam $D/sarscov2/test.single_end.sorted.bam $R/data/se.bam $R/data/empty.bam $R/data/edge/*.bam
echo "=== NEW edge BAMs vs counts planted by construction (expected.json)"; python $R/t3_expected.py
echo "=== MAPQ>=30 fraction idiom on synth (truth 485 of 505 primary mapped)"; samtools view -c -F 2308 -q 30 $S; samtools view -c -F 2308 $S
echo "=== stats SN fields the Skill lists (synth)"; samtools stats $S | grep '^SN' | cut -f2-3 | grep -E 'raw total|reads mapped|properly|insert size|inward|outward|other orient|bases mapped|error rate|average length|percentage'
