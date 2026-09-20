#!/bin/bash
# Input 1 (canonical, regression of pre-fix inputs 1 and 4): the SKILL.md "Duplicate Marking Workflow" block (extracted verbatim),
# -r, -s/-f stats, percentage block, flagstat, the pysam blocks (extracted verbatim) -- on planted_dups.bam (truth 100 reads = 50 pairs)
# and the real human PE BAM (cross-checked against Picard + sambamba + samblaster).
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in01; mkdir in01; cd in01
samtools --version | head -1
for S in planted_dups test.paired_end.sorted; do
  echo "=========== $S"
  rm -rf s; mkdir s; cd s
  cp $D/$S.bam input.bam
  blk "## Duplicate Marking Workflow" 1 > steps.sh; echo "[extracted block: $(wc -l < steps.sh) lines]"
  bash -e steps.sh; echo "[steps exit=$?]"
  echo "[check] input records $(samtools view -c input.bam) marked records $(samtools view -c marked.bam); flagged (0x400) $(flagged marked.bam); index: $(ls marked.bam.bai)"
  samtools flagstat marked.bam | grep -i dup
  # SKILL.md "Percentage Duplicates" block (verbatim)
  blk "### Percentage Duplicates" 1 > pct.sh; echo "[pct block output]"; bash pct.sh
  echo "[check] independent: primary flagged / primary (samtools stats-free): $(samtools view -c -f 1024 -F 2304 marked.bam) / $(samtools view -c -F 2304 marked.bam)"
  # -s / -f / -r blocks verbatim
  blk "### Output Statistics" 1 | sed 's#input.bam#coordsort.bam#; s#marked.bam#m_s.bam#' > s.sh; bash s.sh; cat markdup_stats.txt | grep -E 'DUPLICATE (PAIR|SINGLE)$|DUPLICATE TOTAL|EXAMINED'
  blk "### Remove Duplicates" 1 | sed 's#input.bam#coordsort.bam#' > r.sh; bash r.sh; echo "[check] -r records: $(samtools view -c deduped.bam) (= total - flagged = $(( $(samtools view -c marked.bam) - $(flagged marked.bam) )))"
  echo "[check] -c count blocks: $(samtools view -c -f 1024 marked.bam) dup / $(samtools view -c -F 1024 marked.bam) nondup"
  # independent tools
  picard MarkDuplicates I=input.bam O=picard.bam M=picard.metrics ASSUME_SORT_ORDER=coordinate >/dev/null 2>&1
  echo "[picard] $(grep -A1 '^LIBRARY' picard.metrics | tail -1 | cut -f 6-9) ; flagged reads $(flagged picard.bam)"
  sambamba markdup -t 2 input.bam samba.bam >/dev/null 2>&1; echo "[sambamba] flagged $(flagged samba.bam)"
  samtools collate -O -u input.bam col | samtools view -h | samblaster -M 2>/dev/null | samtools view -b -o sblast.bam -; echo "[samblaster] flagged $(flagged sblast.bam)"
  samtools view -f 1024 marked.bam | cut -f1,2 | sort > a.txt; samtools view -f 1024 picard.bam | cut -f1,2 | sort > b.txt
  echo "[check] samtools vs Picard flagged (name,flag) set diff lines: $(comm -3 a.txt b.txt | wc -l)"
  # pysam blocks verbatim
  blk "### Full Pipeline" 1 > ps_full.py
  blk "### Check Duplicate Flag" 1 > ps_rate.py
  blk "### Filter Out Duplicates" 1 > ps_filter.py
  mkdir p; cp input.bam p/; cd p
  python ../ps_full.py && echo "[pysam full pipeline] flagged $(flagged marked.bam) index $(ls marked.bam.bai)"
  python ../ps_rate.py
  python ../ps_filter.py && echo "[pysam filter] nodup.bam records $(samtools view -c nodup.bam) ; samtools -F 1024: $(samtools view -c -F 1024 marked.bam)"
  cd ../..
done
echo "=========== pysam error surfaces as exception (markdup without ms tag)"
python - <<'PY'
import pysam
try:
    pysam.markdup('/mnt/openscience/audits/bio-duplicate-handling/run/data/test.paired_end.sorted.bam', '/tmp/x.bam')
except Exception as e:
    print(type(e).__name__, str(e)[:120])
PY
