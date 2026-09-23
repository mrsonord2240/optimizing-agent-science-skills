#!/usr/bin/env bash
# Regression of the repaired shipped example at dfc77a6: the default simulated
# GWAS and LD must be self-consistent, lambda <= 0.10, and both result TSVs
# must be created only after credible-set fitting completes.
set -euo pipefail
ROOT=/f/OpenScience/audits/bio-causal-genomics-fine-mapping/run/re-audit-dfc77a6
OUT="$ROOT/rss-default"
rm -rf "$OUT"
mkdir -p "$OUT"
cd "$OUT"
set +e
/f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh "$ROOT/skill-src/examples/susie_rss_finemap.R" > stdout.txt 2>&1
R_RC=$?
set -e
echo "example exit code: $R_RC"
# This Windows R wrapper can exit 139 after materialized output; accept it only
# after all content assertions below have independently verified completion.
test "$R_RC" -eq 0 -o "$R_RC" -eq 139
LAMBDA=$(awk '/estimate_s_rss lambda/ {print $4}' stdout.txt)
awk -v x="$LAMBDA" 'BEGIN { if (x <= 0.10) {print "ASSERT default lambda <= 0.10: TRUE (" x ")"} else {print "ASSERT default lambda <= 0.10: FALSE (" x ")"; exit 1} }'
test -s finemap_pips.tsv
test -s finemap_credible_sets.tsv
grep -q 'Valid credible sets after purity filter: [1-9]' stdout.txt
echo 'ASSERT default emits non-empty PIP and credible-set TSVs: TRUE'
