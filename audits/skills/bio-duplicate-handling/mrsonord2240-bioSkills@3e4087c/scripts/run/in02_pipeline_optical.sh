#!/bin/bash
# Input 2 (variant A, regression of pre-fix input 2): the fixer's rewritten "Pipeline Version (Optimized)" block extracted verbatim, run
# from a CLEAN directory. Asserts: valid run exits 0 with truth counts; each failure mode exits NON-ZERO (the pre-fix defect exited 0).
# Then the optical section on a SYNTHETIC Illumina-named BAM (truth: 4 dup pairs; optical pairs 0/1/2 at -d 0/100/2500), checked against Picard.
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in02; mkdir in02; cd in02
blk "### Pipeline Version (Optimized)" 1 > pipe_block.sh
echo "----- extracted pipeline block:"; cat pipe_block.sh; echo "-----"
for S in planted_dups test.paired_end.sorted; do
  echo "== 2a valid run, clean dir, $S"
  rm -rf c; mkdir c; cd c; cp $D/$S.bam input.bam
  bash ../pipe_block.sh > out.txt 2> err.txt; rc=$?
  echo "[exit=$rc] input $(samtools view -c input.bam) marked $(samtools view -c marked.bam) flagged $(flagged marked.bam) index $(ls marked.bam.bai 2>&1)"
  echo "[stats file] $(grep -E 'DUPLICATE TOTAL|EXAMINED' markdup_stats.txt | tr '\n' ' ')  read-group blocks: $(grep -c 'READ GROUP' markdup_stats.txt)"
  grep -v '^\[' err.txt | head -3
  cd ..
done
echo "== 2b block WITHOUT the mkdir line (the pre-fix failure), clean dir: exit must be NON-ZERO"
rm -rf c; mkdir c; cd c; cp $D/planted_dups.bam input.bam
grep -v '^mkdir -p tmpdir' ../pipe_block.sh > nomkdir.sh
bash nomkdir.sh >out.txt 2>err.txt; rc=$?; echo "[exit=$rc] (err: $(grep -m1 -i 'cannot open' err.txt))  marked.bam size: $(stat -c %s marked.bam 2>/dev/null)"
cd ..
echo "== 2c block WITHOUT pipefail: shows why the guard matters (exit code would be 0 with empty output)"
rm -rf c; mkdir c; cd c; cp $D/planted_dups.bam input.bam
grep -v '^set -euo pipefail' ../pipe_block.sh | grep -v '^mkdir' > nopf.sh
bash nopf.sh >out.txt 2>err.txt; echo "[exit=$?] marked.bam size $(stat -c %s marked.bam 2>/dev/null)"
cd ..
echo "== 2d missing input: exit must be non-zero"
rm -rf c; mkdir c; cd c
bash ../pipe_block.sh >out.txt 2>err.txt; echo "[exit=$?] $(grep -m1 -iE 'no such|fail|error' err.txt)"
cd ..
echo "== 2e truncated input BAM: exit non-zero?"
rm -rf c; mkdir c; cd c; head -c 6000 $D/test.paired_end.sorted.bam > input.bam
bash ../pipe_block.sh >out.txt 2>err.txt; echo "[exit=$?] $(grep -m1 -iE 'truncat|EOF|fail|error' err.txt)"
cd ..

echo "== 2f optical section (SKILL.md block verbatim) on SYNTHETIC synth_optical.bam"
python $RUN/00_make_synth.py
prep() { samtools sort -n -o $1.ns.bam $2 && samtools fixmate -m $1.ns.bam $1.fm.bam && samtools sort -o $1.cs.bam $1.fm.bam; }
prep op $D/synth_optical.bam
for d in 0 100 2500; do
  samtools markdup -d $d -s op.cs.bam op_$d.bam 2> op_$d.txt
  echo "  samtools -d $d: flagged $(flagged op_$d.bam) reads; OPTICAL reads: $(grep -E '^(DUPLICATE (PAIR|SINGLE) )?OPTICAL' op_$d.txt | tr '\n' ' ')  dt tags: $(samtools view -f 1024 op_$d.bam | grep -o 'dt:Z:[A-Z][A-Z]' | sort | uniq -c | tr '\n' ' ')"
  picard MarkDuplicates I=$D/synth_optical.bam O=pic_$d.bam M=pic_$d.txt OPTICAL_DUPLICATE_PIXEL_DISTANCE=$d >/dev/null 2>&1
  [ $d -eq 0 ] && continue
  echo "  picard  -d $d: $(grep -A1 '^LIBRARY' pic_$d.txt | tail -1 | cut -f 7-8 | tr '\t' ' ')  (READ_PAIR_DUPLICATES / READ_PAIR_OPTICAL_DUPLICATES columns 7..8)"
done
echo "  header of Picard metrics columns: $(grep '^LIBRARY' pic_100.txt | tr '\t' '\n' | sed -n '7,8p' | tr '\n' ' ')"
cp op.cs.bam marked_in.bam
blk "## Optical Distance Is Platform-Specific" 1 > opt.sh
sed 's#input.bam#marked_in.bam#g' opt.sh > opt2.sh; echo "[SKILL.md optical block, verbatim except filenames]"; bash opt2.sh
