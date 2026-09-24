#!/usr/bin/env bash
# Purpose: verify the final-pass reference split preserves all moved method entrypoints.
# Inputs: final source files; Usage: bash 07_reference_integrity.sh
set -euo pipefail

ROOT=/mnt/openscience
SKILL="$ROOT/worktrees/bio-alignment-validation-finalpass/alignment-files/alignment-validation"
MAIN="$SKILL/SKILL.md"
REF="$SKILL/references/library-metrics.md"

test "$(wc -l < "$MAIN")" -le 300
grep -q 'references/library-metrics.md' "$MAIN"
grep -q 'samtools stats input.bam' "$REF"
grep -q 'picard CollectInsertSizeMetrics' "$REF"
grep -q 'def get_insert_sizes' "$REF"
grep -q 'picard CollectGcBiasMetrics' "$REF"
grep -q 'computeGCBias' "$REF"
grep -q 'Rscript' "$REF"
python - "$REF" <<'PY'
import re
import sys
text = open(sys.argv[1], encoding="utf-8").read()
assert text.count("~~~") == 10
python_block = re.search(r"~~~python\n(.*?)~~~", text, re.S).group(1)
compile(python_block, "library-metrics-python-snippet", "exec")
print("main_lines=%d reference_fences=%d python_snippet=PASS" % (
    len(open("/mnt/openscience/worktrees/bio-alignment-validation-finalpass/alignment-files/alignment-validation/SKILL.md", encoding="utf-8").read().splitlines()),
    text.count("~~~") // 2,
))
PY
