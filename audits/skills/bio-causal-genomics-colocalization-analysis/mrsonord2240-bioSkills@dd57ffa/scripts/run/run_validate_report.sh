#!/usr/bin/env bash
set -euo pipefail
root="F:/OpenScience/audits/bio-causal-genomics-colocalization-analysis/run"
python "$root/validate_report.py" > "$root/validate_report_output.txt" 2>&1
