#!/bin/bash
# Audit smoke test of examples/diann_analysis.sh with a stub `diann` on PATH (real DIA-NN not available).
EX=F:/OpenScience/external/GPTomics__bioSkills/proteomics/dia-analysis/examples/diann_analysis.sh
BIN=/f/OpenScience/audits/bio-proteomics-dia-analysis/runs/smoke/bin
for c in case_ok case_space case_none; do
  d=F:/OpenScience/audits/bio-proteomics-dia-analysis/runs/smoke/$c
  cd "$d"; rm -rf diann_out; echo "===== $c : files: $(ls -1 | tr '\n' ' ')"
  PATH="$BIN:$PATH" bash "$EX"; echo "exit=$?"
done
