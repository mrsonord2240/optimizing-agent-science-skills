#!/usr/bin/env bash
# Static assertions for the exact copied audit source; no source tree is written.
set -euo pipefail
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
ROOT=/mnt/openscience/audits/bio-alignment-structural/run
SRC="$ROOT/source"
python -m py_compile "$SRC"/examples/*.py
test "$(grep -c '^name: bio-alignment-structural$' "$SRC/SKILL.md")" = 1
test "$(grep -c 'references/foldseek-multimer.md' "$SRC/SKILL.md")" -ge 1
test "$(grep -c "report\['scores'\]" "$SRC/references/foldmason.md")" -eq 1
test "$(grep -c -- '--refine-seed' "$SRC/examples/foldmason_msa.py")" -ge 1
echo 'STATIC_ASSERTIONS_PASS: frontmatter, references, seeded Foldmason, 4 Python examples compile'
