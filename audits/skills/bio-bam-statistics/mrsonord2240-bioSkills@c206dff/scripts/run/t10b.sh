#!/bin/bash
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
{
python -c "
import skill_snippets as s; out = s.skill_depth_at('work/test.paired_end.sorted.bam','chr22',2999,3000)
print('columns printed for a 1-bp query (start=2999,stop=3000):', len(out), ' min pos', min(out), ' max pos', max(out), '; requested position 2999 depth =', out.get(2999))"
} > out/t10b_depth_at.txt 2>&1; cat out/t10b_depth_at.txt | tail -3
