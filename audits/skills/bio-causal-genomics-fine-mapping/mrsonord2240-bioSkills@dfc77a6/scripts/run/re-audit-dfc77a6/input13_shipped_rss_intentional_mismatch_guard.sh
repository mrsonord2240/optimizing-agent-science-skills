#!/usr/bin/env bash
# New adversarial regression: the documented mismatch-only environment switch
# must stop before a fit or any result TSV is written.
set -euo pipefail
ROOT=/f/OpenScience/audits/bio-causal-genomics-fine-mapping/run/re-audit-dfc77a6
OUT="$ROOT/rss-intentional-mismatch"
rm -rf "$OUT"
mkdir -p "$OUT"
cd "$OUT"
set +e
SUSIE_RSS_DEMO_LD_MISMATCH=1 /f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh "$ROOT/skill-src/examples/susie_rss_finemap.R" > stdout.txt 2>&1
RC=$?
set -e
echo "example exit code: $RC"
test "$RC" -ne 0
LAMBDA=$(awk '/estimate_s_rss lambda/ {print $4}' stdout.txt)
awk -v x="$LAMBDA" 'BEGIN { if (x > 0.10) {print "ASSERT mismatch lambda > 0.10: TRUE (" x ")"} else {print "ASSERT mismatch lambda > 0.10: FALSE (" x ")"; exit 1} }'
grep -q 'no credible sets will be reported' stdout.txt
! grep -q 'Valid credible sets after purity filter' stdout.txt
! test -e finemap_pips.tsv
! test -e finemap_credible_sets.tsv
echo 'ASSERT mismatch stops before fit/report/output TSVs: TRUE'
