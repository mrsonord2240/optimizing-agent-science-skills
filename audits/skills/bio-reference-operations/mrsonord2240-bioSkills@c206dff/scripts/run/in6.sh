#!/bin/bash
# VERBATIM run of every shipped bash block that can run on a small synthetic reference/BAM (names substituted by
# providing files called reference.fa / input.bam / sample.bam, so the blocks run byte-for-byte as written).
R=/mnt/openscience/audits/bio-reference-operations/run
W=$R/work/in6
rm -rf $W; mkdir -p $W; cd $W
cp $R/data/synthetic/synth.fa reference.fa
cp $R/data/synthetic/synth_chr.bam input.bam; cp $R/data/synthetic/synth_chr.bam.bai input.bam.bai
cp input.bam sample.bam
run() {  # name
  f=$R/snippets/$1.txt
  out=$(bash $f 2>err.txt </dev/null); rc=$?
  printf '%-12s rc=%s stdout_lines=%s stderr_lines=%s | %s\n' "$1" "$rc" "$(printf '%s' "$out" | grep -c '')" "$(grep -c '' err.txt)" "$(head -c 110 err.txt | tr '\n' ' ')"
}
for n in skill_01_bash skill_02_bash skill_03_bash skill_04_bash skill_05_bash skill_06_bash skill_08_bash skill_09_bash skill_11_bash \
         skill_12_bash skill_13_bash skill_14_bash skill_15_bash skill_16_bash skill_17_bash skill_18_bash ; do run $n; done
echo "--- blocks that need a live setup"
echo "skill_25 (workflow) with REF_CACHE_DIR UNSET:"; run skill_25_bash
mkdir -p $W/cache; export REF_CACHE_DIR=$W/cache
echo "skill_25 with REF_CACHE_DIR set:"; run skill_25_bash; unset REF_CACHE_DIR
ls -la $W/cache | head -3; find $W/cache -type f | head -3
for n in skill_26_bash skill_27_bash skill_28_bash skill_29_bash skill_30_bash ug_02_bash ug_03_bash ug_04_bash ug_05_bash ug_06_bash ug_07_bash ug_14_bash; do run $n; done
echo "--- ug_07 (chr1..chrM subset) result files:"; ls -la main_chroms.* 2>&1 | head; grep -c '>' main_chroms.fa
echo "--- skill_30 comparison.sam (minimap2 -a reference.fa consensus.fa):"; samtools view -c comparison.sam; samtools view comparison.sam | cut -f1-6 | head -3
echo "--- consensus.fa after skill_12"; grep '>' consensus.fa
echo "--- skill_15 -d 5 / -a lines are in the block:"; cat $R/snippets/skill_15_bash.txt
