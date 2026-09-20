#!/bin/bash
# rb.sh <block-number> <bam> [workdir] : run SKILL.md fenced block NNN verbatim with input.bam -> <bam>
R=/mnt/openscience/audits/bio-bam-statistics/run
n=$(printf '%03d' $1); f=$(ls $R/blocks/${n}_*.sh | head -1)
sed "s#input\.bam#$2#g" "$f" > $R/work/blk_${n}_$$.sh
bash $R/work/blk_${n}_$$.sh; echo "[rc=$?]"; rm -f $R/work/blk_${n}_$$.sh
