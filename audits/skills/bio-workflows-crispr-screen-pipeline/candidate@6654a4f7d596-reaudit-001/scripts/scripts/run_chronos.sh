#!/bin/bash
# chronos route snippet extracted verbatim from the candidate, run against the standard NEGv1 (header GENE).
SK=/f/OpenScience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline
ENV=/f/OpenScience/audit-envs/crispr-screen-analyst
DATA=$ENV/public-data/derived/crispr-pipeline
W=/f/OpenScience/fix-evidence/recut-crispr-pipeline/reaudit-001/work/chronos
rm -rf $W; mkdir -p $W; cp $DATA/chronos/* $W/; cd $W
"$ENV/tools/chronos-venv/Scripts/python.exe" - <<'PYX'
import re
t = open('F:/OpenScience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline/routes/chronos.md', encoding='utf-8').read()
code = re.search(r"```python\n(.*?)```", t, re.S).group(1)
open('snippet.py', 'w', encoding='utf-8').write(code)
PYX
head -c 300 NEGv1.txt | head -1
time "$ENV/tools/chronos-venv/Scripts/python.exe" snippet.py > run.log 2>&1
echo "EXIT[chronos]=$?"
tail -5 run.log
