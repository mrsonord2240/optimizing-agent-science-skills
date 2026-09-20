#!/bin/bash
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
{
echo "== Skill 'Calculate Depth at Position' pileup.pos / .n on chr22:2999-3001 (0-based half-open) real data; truth from samtools depth chr22:3000-3001"
python -W error::DeprecationWarning -c "
import skill_snippets as s; s.skill_depth_at('work/test.paired_end.sorted.bam','chr22',2999,3001)" 2>&1 | tail -4
samtools depth -r chr22:3000-3001 work/test.paired_end.sorted.bam
echo "-- smoke says pysam pileup at chr22:3000 depth 1562 (default), samtools depth default:"
echo "== samtools depth -a on unaligned-only / region outside reads (human slice trap): "
samtools depth -a -r chr22:20000-20003 work/test.paired_end.sorted.bam
echo "== awk mean depth (Skill quick reference) on that empty region: (dividing by 0 covered positions)"
samtools depth -r chr22:20000-20003 work/test.paired_end.sorted.bam | awk '{sum+=$3;n++}END{print sum/n}' 2>&1 | tail -1
} > out/t10_misc.txt 2>&1; cat out/t10_misc.txt
