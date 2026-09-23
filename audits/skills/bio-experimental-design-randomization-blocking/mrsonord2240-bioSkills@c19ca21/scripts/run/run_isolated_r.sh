#!/usr/bin/env bash
set -euo pipefail
runtime=/home/sci/openscience-r-isolated-20260923/bin/Rscript
export PATH=/home/sci/openscience-r-isolated-20260923/bin:$PATH
cd "$(dirname "$1")/.."
"$runtime" "$1"
