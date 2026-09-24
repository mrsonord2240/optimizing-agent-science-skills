#!/usr/bin/env bash
set -euo pipefail

env_dir=/home/sci/multimodal-private-20260923/packages
mkdir -p "$env_dir"
python3 -m pip install --target "$env_dir" "muon==0.1.9" "scanpy==1.12.4" "leidenalg==0.11.0"
PYTHONPATH="$env_dir" python3 - <<'PY'
import mudata
import muon
import scanpy
print(f"private_runtime_ready muon={muon.__version__} scanpy={scanpy.__version__} mudata={mudata.__version__}")
PY
