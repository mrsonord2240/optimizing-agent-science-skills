#!/usr/bin/env bash
set -euo pipefail
python - <<'PY'
import importlib.util
print('scglue_spec', importlib.util.find_spec('scglue'))
PY
