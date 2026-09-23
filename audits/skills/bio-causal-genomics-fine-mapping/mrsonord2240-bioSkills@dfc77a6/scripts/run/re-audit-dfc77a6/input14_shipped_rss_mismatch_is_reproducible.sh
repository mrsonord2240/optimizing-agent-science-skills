#!/usr/bin/env bash
# Independent repeat of Input 13: verifies the guard is deterministic on a
# clean output directory and that it does not inherit result files from a run.
set -euo pipefail
ROOT=/f/OpenScience/audits/bio-causal-genomics-fine-mapping/run/re-audit-dfc77a6
OUT="$ROOT/rss-intentional-mismatch-repeat"
rm -rf "$OUT"
mkdir -p "$OUT"
cd "$OUT"
set +e
SUSIE_RSS_DEMO_LD_MISMATCH=1 /f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh "$ROOT/skill-src/examples/susie_rss_finemap.R" > stdout.txt 2>&1
RC=$?
set -e
test "$RC" -ne 0
LAMBDA=$(awk '/estimate_s_rss lambda/ {print $4}' stdout.txt)
awk -v x="$LAMBDA" 'BEGIN { if (x > 0.10) {print "ASSERT repeated mismatch lambda > 0.10: TRUE (" x ")"} else {exit 1} }'
grep -q 'LD reference likely mismatches the GWAS sample' stdout.txt
! test -e finemap_pips.tsv
! test -e finemap_credible_sets.tsv
echo 'ASSERT clean repeated mismatch run writes no result TSVs: TRUE'
