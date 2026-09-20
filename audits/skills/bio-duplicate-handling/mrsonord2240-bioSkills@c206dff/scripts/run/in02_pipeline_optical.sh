#!/bin/bash
# Input 2 (variant A): SKILL.md "Pipeline Version (Optimized)" verbatim from a clean dir, + optical-distance claims
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in02; mkdir in02; cd in02
echo "### 2a. pipeline verbatim, tmpdir does NOT exist beforehand"
cp $D/planted_dups.bam input.bam
samtools collate -O -u input.bam tmpdir/collate | \
    samtools fixmate -m -u - - | \
    samtools sort -u -@ 4 -T tmpdir/sort - | \
    samtools markdup -@ 4 -d 2500 --use-read-groups \
        -f markdup_stats.txt - marked.bam
echo "pipeline exit codes: ${PIPESTATUS[*]}"
ls -la marked.bam markdup_stats.txt 2>&1 | head
echo "### 2b. same, after mkdir tmpdir"
mkdir tmpdir
samtools collate -O -u input.bam tmpdir/collate | \
    samtools fixmate -m -u - - | \
    samtools sort -u -@ 4 -T tmpdir/sort - | \
    samtools markdup -@ 4 -d 2500 --use-read-groups \
        -f markdup_stats.txt - marked.bam
echo "pipeline exit codes: ${PIPESTATUS[*]}"
samtools index marked.bam
echo "[check] dup flag reads: $(samtools view -c -f 1024 marked.bam) (truth 100)"; cat markdup_stats.txt
echo "[check] SKILL.md dt-tag counting one-liner:"
samtools view -f 1024 marked.bam | grep -o 'dt:Z:[A-Z][A-Z]' | sort | uniq -c
echo "[check] reads carrying dt tag: $(samtools view marked.bam | grep -c 'dt:Z')"
echo "### 2c. -r removal count with -d/--use-read-groups"
samtools markdup -r -d 2500 --use-read-groups coordsort.bam x.bam 2>&1 | head -2
echo "### 2d. optical: synthetic Illumina-name BAM (truth: 4 dup pairs; optical pairs -d0:0, -d100:1, -d2500:2)"
cp $D/synth_optical.bam so.bam
samtools fixmate -m so.bam so_fm.bam 2>&1 | head -2   # coordinate sorted input: fixmate needs name groups
samtools sort -n -o so_ns.bam so.bam; samtools fixmate -m so_ns.bam so_fm.bam; samtools sort -o so_cs.bam so_fm.bam
for d in 0 100 2500; do
  if [ $d = 0 ]; then samtools markdup -s so_cs.bam o$d.bam 2> s$d.txt; else samtools markdup -d $d -s so_cs.bam o$d.bam 2> s$d.txt; fi
  echo "-- -d $d : dup reads $(samtools view -c -f 1024 o$d.bam); $(grep -E 'DUPLICATE PAIR:|DUPLICATE PAIR OPTICAL' s$d.txt | tr '\n' ' ')  dt tags: $(samtools view o$d.bam | grep -o 'dt:Z:[A-Z]*' | sort | uniq -c | tr '\n' ' ')"
done
echo "-- -t (no -d) tags:"; samtools markdup -t so_cs.bam ot.bam; samtools view -f 1024 ot.bam | head -1 | grep -o 'do:Z:[^ 	]*\|dt:Z:[A-Z]*'
for d in 100 2500; do
  picard MarkDuplicates I=so.bam O=pic$d.bam M=pic$d.txt OPTICAL_DUPLICATE_PIXEL_DISTANCE=$d ASSUME_SORT_ORDER=coordinate >/dev/null 2>&1
  echo "-- picard OPT=$d: $(grep -A1 '^LIBRARY' pic$d.txt | tail -1 | cut -f7,8)  (cols: READ_PAIR_DUPLICATES READ_PAIR_OPTICAL_DUPLICATES)"
done
echo "### 2e. -d on the real human BAM whose read names are not Illumina-format (testN:1)"
samtools markdup -d 2500 -s coordsort_dummy.bam /dev/null 2>&1 | head -1
samtools sort -n -o h_ns.bam $D/test.paired_end.sorted.bam; samtools fixmate -m h_ns.bam h_fm.bam; samtools sort -o h_cs.bam h_fm.bam
samtools markdup -d 2500 -s h_cs.bam h_d.bam 2>&1 | grep -E 'warn|error|DUPLICATE PAIR|OPTICAL' | head
echo "[check] human BAM flagged with -d 2500: $(samtools view -c -f 1024 h_d.bam) (no -d: 1656)"
