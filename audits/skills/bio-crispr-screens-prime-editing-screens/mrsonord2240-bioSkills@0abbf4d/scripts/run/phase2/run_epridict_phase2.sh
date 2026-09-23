#!/usr/bin/env bash
# Phase 2 dynamic checks 7-8: ePRIDICT light model and documented bigWig validation.
set -euo pipefail
REPO=/mnt/openscience/audit-envs/crispr-screen-analyst/tools/dl/epridict
cd "$REPO"
echo '=== Input 7: documented single locus ==='
micromamba run -n epridict python epridict_prediction.py single --chromosome chr3 --position_hg38 44843504
echo '=== Input 8: all light-model bigWigs parse and carry signal ==='
micromamba run -n epridict python - <<'PY'
import os
import pyBigWig
repo = os.getcwd()
accs = sorted({line.split('_')[1] for line in open(f'{repo}/misc/ePRIDICT_slim_model_column_names.txt')})
for acc in accs:
    path = f'{repo}/bigwig/{acc}.bigWig'
    bw = pyBigWig.open(path)
    values = bw.values('chr3', 44843404, 44843604)
    n = sum(v is not None for v in values)
    print(f'{acc}: bytes={os.path.getsize(path)} chroms={len(bw.chroms())} signal={n}/200')
    bw.close()
    assert n > 0
PY
