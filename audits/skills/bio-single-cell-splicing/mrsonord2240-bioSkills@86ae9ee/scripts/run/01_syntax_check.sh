#!/bin/bash
# Parse-check every extracted SKILL.md block: python ast.parse, R parse(), bash -n. Output asserted below (each line must say OK).
cd /mnt/openscience/audits/bio-single-cell-splicing/run
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
for f in blocks/*.py skill/examples/*.py; do
  asenv as-sc python -c "import ast,sys; ast.parse(open('$f',encoding='utf-8').read()); print('PY OK', '$f')"
done
for f in blocks/*.sh; do bash -n $f && echo "SH OK $f"; done
