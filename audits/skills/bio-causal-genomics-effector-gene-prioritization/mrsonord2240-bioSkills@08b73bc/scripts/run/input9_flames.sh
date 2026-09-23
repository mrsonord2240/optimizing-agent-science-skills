#!/usr/bin/env bash
set -euo pipefail

# Fresh Phase-2 test of the FLAMES workflow newly documented at this pinned tip.
AUDIT=/mnt/openscience/audits/bio-causal-genomics-effector-gene-prioritization
TOOL=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools/flames
OUT="$AUDIT/run/outputs/input9_flames"

rm -rf "$OUT"
mkdir -p "$OUT"
cp -a "$TOOL/example_data/." "$OUT/"
cd "$OUT"
rm -rf annots FLAMES_scores.pred FLAMES_scores.raw

export PYTHONDONTWRITEBYTECODE=1
micromamba run -n flames-py38 python "$TOOL/FLAMES.py" annotate \
  -a "$TOOL/Annotation_data/" -p PoPS.preds -m magma.genes.out \
  -mt magma_exp_gtex_v8_ts_avg_log2TPM.txt.gsa.out -id indexfile.txt \
  -pc prob1 -sc cred1 -g genes.txt -c95 False | tee input9_flames_annotate.log
micromamba run -n flames-py38 python "$TOOL/FLAMES.py" FLAMES -id indexfile.txt -o ./ \
  | tee input9_flames_score.log

test -s FLAMES_scores.pred
for g in GNRH1 FSHB SMAD3 ZFPM1; do grep -q "$g" FLAMES_scores.pred; done
echo 'ASSERTIONS PASS: all four expected example-locus genes occur in FLAMES_scores.pred.'
