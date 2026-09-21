#!/bin/bash
# Install-command checks that do not modify any env: git ls-remote for every repo named in S01/S02/S08, and pip --dry-run (no install) inside as-sc for the pip lines.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
for r in huangyh09/brie lareaulab/psix songlab-cal/scquint wenweixiong/MARVEL VCCRI/Sierra salzmanlab/SpliZ salzmanlab/spliz; do echo -n "$r: "; git ls-remote --heads https://github.com/$r 2>&1 | head -1 | cut -c1-80; done
cd /tmp; rm -rf pipchk; mkdir pipchk; cd pipchk
echo "--- pip install brie (PyPI name, as an unaware user would)"; asenv as-sc python -m pip install --dry-run --no-deps brie 2>&1 | tail -3 | cut -c1-200
echo "--- pip install git+brie (--no-deps dry run)"; asenv as-sc python -m pip install --dry-run --no-deps git+https://github.com/huangyh09/brie 2>&1 | tail -2 | cut -c1-200
echo "--- psix, no build isolation"; asenv as-sc python -m pip install --dry-run --no-deps --no-build-isolation git+https://github.com/lareaulab/psix 2>&1 | tail -2 | cut -c1-200
echo "--- psix WITHOUT --no-build-isolation"; asenv as-sc python -m pip install --dry-run --no-deps git+https://github.com/lareaulab/psix 2>&1 | tail -2 | cut -c1-200
echo "--- scquint"; asenv as-sc python -m pip install --dry-run --no-deps git+https://github.com/songlab-cal/scquint 2>&1 | tail -2 | cut -c1-200
echo "--- SpliZ as pip (deleted from Skill; confirm why)"; asenv as-sc python -m pip install --dry-run --no-deps git+https://github.com/salzmanlab/SpliZ 2>&1 | tail -2 | cut -c1-200
echo "--- SpliZ nextflow.config keys named in the Skill"; git clone -q --depth 1 https://github.com/salzmanlab/spliz sz 2>&1 | tail -1; grep -n "dataname\|input_file\|libraryType\|grouping_level_1\|grouping_level_2\|SICILIAN" sz/nextflow.config | head -12; ls sz | head
which nextflow || echo "nextflow: not installed"
cd /tmp; rm -rf pipchk
