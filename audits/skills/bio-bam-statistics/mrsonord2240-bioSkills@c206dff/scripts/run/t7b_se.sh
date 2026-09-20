#!/bin/bash
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
{
echo "== Skill 'Count Reads' on single-end BAM (real nf-core SE BAM and synthetic):"
python -c "
import skill_snippets as s; s.skill_count_reads('work/batch/sc2_se.bam')" 2>&1 | tail -4
echo "rc of the above python = $(python -c "
import skill_snippets as s; s.skill_count_reads('work/batch/sc2_se.bam')" >/dev/null 2>&1; echo $?)"
echo "== usage-guide flagstat() on empty BAM:"; python -c "
import skill_snippets as s; print(s.guide_flagstat('data/empty.bam'))" 2>&1 | tail -2
echo "== Skill insert-size snippet on SE BAM:"; python -c "
import skill_snippets as s; s.skill_insert_size('data/se.bam')" 2>&1 | tail -2
echo "== mosdepth on empty BAM: rc=$(mosdepth work/t7e data/empty.bam >/dev/null 2>&1; echo $?), files: $(ls work/t7e* 2>/dev/null | tr '\n' ' ')"
echo "== multiqc sources"; cat work/mq/out/multiqc_data/multiqc_sources.txt 2>/dev/null | head; ls work/mq/out/multiqc_data | head -20
} > out/t7b_se.txt 2>&1; cat out/t7b_se.txt
