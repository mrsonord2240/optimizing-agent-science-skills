#!/bin/bash
# Input 1 (canonical): SKILL.md "Duplicate Marking Workflow" step-by-step, verbatim commands, on
# (a) planted_dups.bam (truth: 50 pairs = 100 reads) and (b) the real human PE BAM (natural dups; cross-tool truth)
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in01; mkdir in01; cd in01
samtools --version | head -1; picard MarkDuplicates --version 2>&1 | tail -1
for S in planted_dups test.paired_end.sorted; do
  echo "=========== $S"
  cp $D/$S.bam input.bam
  # ---- SKILL.md steps 1-5 verbatim
  samtools sort -n -o namesort.bam input.bam
  samtools fixmate -m namesort.bam fixmate.bam
  samtools sort -o coordsort.bam fixmate.bam
  samtools markdup coordsort.bam marked.bam
  samtools index marked.bam
  echo "[check] input records: $(samtools view -c input.bam)  marked records: $(samtools view -c marked.bam)"
  echo "[check] dup flag (0x400) reads: $(samtools view -c -f 1024 marked.bam)"
  echo "[check] pct (SKILL.md formula):"; total=$(samtools view -c marked.bam); dups=$(samtools view -c -f 1024 marked.bam); echo "scale=2; $dups * 100 / $total" | bc
  echo "[check] flagstat dup lines:"; samtools flagstat marked.bam | grep -i dup
  echo "[check] markdup -s stats (SKILL.md 'Output Statistics'):"
  samtools markdup -s coordsort.bam marked_s.bam 2> stats_s.txt; cat stats_s.txt
  echo "[check] -r removal:"
  samtools markdup -r coordsort.bam deduped.bam; echo "records after -r: $(samtools view -c deduped.bam)"
  echo "[check] nodup view -F 1024 count: $(samtools view -c -F 1024 marked.bam)"
  # ---- independent tools
  picard MarkDuplicates I=input.bam O=picard.bam M=picard.metrics ASSUME_SORT_ORDER=coordinate 2>/dev/null >/dev/null
  echo "[picard] metrics:"; grep -A2 '^LIBRARY' picard.metrics | cut -f1-9
  echo "[picard] flagged reads: $(samtools view -c -f 1024 picard.bam)"
  sambamba markdup -t 2 input.bam samba.bam 2>/dev/null >/dev/null; echo "[sambamba] flagged reads: $(samtools view -c -f 1024 samba.bam)"
  samtools collate -O -u input.bam col | samtools view -h | samblaster -M 2>samblaster.log | samtools view -b -o sblast.bam -; echo "[samblaster] flagged reads: $(samtools view -c -f 1024 sblast.bam)"; tail -3 samblaster.log
  # same set of reads? compare flagged read names between samtools and picard
  samtools view -f 1024 marked.bam | cut -f1,2 | sort > st_names.txt; samtools view -f 1024 picard.bam | cut -f1,2 | sort > pic_names.txt
  echo "[check] samtools vs picard flagged read (name,flag) set differences: $(comm -3 st_names.txt pic_names.txt | wc -l)"
  rm -f namesort.bam fixmate.bam
done
