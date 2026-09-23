#!/usr/bin/env bash
# Probe the documented no-global use_unmod route with only the stated PTM-side files.
set -uo pipefail
ROOT='F:/OpenScience'
ENV="$ROOT/audit-envs/mass-spec-proteomics-analyst"
DATA="$ROOT/audits/bio-proteomics-ptm-analysis/data/phospho"
rm -rf in6_no_global in6_no_global_out
mkdir in6_no_global
cp "$DATA/evidence_phospho.txt" "$DATA/annotation_ptm.csv" "$DATA/synthetic.fasta" in6_no_global/
if "$ENV/r.sh" msstatsptm_labelfree.R dir=in6_no_global fasta=synthetic.fasta use_unmod=TRUE out=in6_no_global_out > in6_no_global.out 2>&1; then
  echo 'UNEXPECTED_SUCCESS_NO_GLOBAL' >> in6_no_global.out
else
  echo 'EXPECTED_NO_GLOBAL_FAILURE' >> in6_no_global.out
fi
