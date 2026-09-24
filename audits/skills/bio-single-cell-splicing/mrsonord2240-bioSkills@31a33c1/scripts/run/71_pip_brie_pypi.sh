#!/bin/bash
# pip install brie (PyPI sdist) as dry run in a scratch dir; confirms the Skill's claim that it fails (sdist lacks requirements.txt).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
cd /tmp; rm -rf pipchk2; mkdir pipchk2; cd pipchk2
asenv as-sc python -m pip install --dry-run --no-deps brie 2>&1 | grep -v "libmamba\|Waiting" | tail -6 | cut -c1-200
cd /tmp; rm -rf pipchk2
