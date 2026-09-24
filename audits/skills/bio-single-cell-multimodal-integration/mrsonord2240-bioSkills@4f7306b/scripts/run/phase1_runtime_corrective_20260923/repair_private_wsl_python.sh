#!/usr/bin/env bash
set -euo pipefail

env_dir=/home/sci/multimodal-private-20260923/packages
python3 -m pip install --target "$env_dir" --upgrade --force-reinstall "h5py==3.16.0" "muon==0.1.9" "scanpy==1.12.4" "leidenalg==0.11.0"
PYTHONPATH="$env_dir" python3 - <<'PY'
import h5py
import leidenalg
import mudata
import muon
import scanpy
print(f"private_runtime_repaired h5py={h5py.__version__} muon={muon.__version__} scanpy={scanpy.__version__} leidenalg={leidenalg.__version__}")
PY
