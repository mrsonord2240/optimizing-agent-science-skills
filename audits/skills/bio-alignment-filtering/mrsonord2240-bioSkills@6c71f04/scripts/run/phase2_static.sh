#!/bin/bash
set -euo pipefail
skill=/mnt/openscience/wt/alignment-files-alignment-filtering/alignment-files/alignment-filtering
find "$skill" -type f -name '*.py' -print0 | xargs -0 -n1 python -B -c 'import ast,pathlib,sys; ast.parse(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")); print("PASS python parse",sys.argv[1])'
find "$skill" -type f -name '*.sh' -print0 | xargs -0 -n1 bash -n
test -f "$skill/SKILL.md"
test -f "$skill/usage-guide.md"
test -f "$skill/scripts/filter_by_bed.py"
test -f "$skill/scripts/subsample_pysam.py"
test -f "$skill/scripts/match_read_count.sh"
test -f "$skill/examples/filter_bam.py"
if find "$skill" -type d -name __pycache__ -print -quit | grep -q .; then
  echo 'FAIL source __pycache__ exists'
  exit 1
fi
echo 'PASS static shipped files, syntax, and source cleanliness'
