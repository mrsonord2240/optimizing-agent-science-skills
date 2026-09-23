#!/usr/bin/env bash
# Prior Input 3 replay.  Exit 1 is the intentional documented guard for zero modelled PSMs.
set -euo pipefail
ENV='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst'
PHIL="$ENV/tools/philosopher/philosopher.exe"
ROOT='F:/OpenScience/audits/bio-proteomics-protein-inference/run'
FASTA='F:/OpenScience/audits/bio-proteomics-peptide-identification/rerun4/comet_out/target_decoy.fasta'
PEPXML='F:/OpenScience/audits/bio-proteomics-peptide-identification/rerun4/comet_out/comet.pep.xml'
WORK="$ROOT/outputs/prior3_philosopher"
test ! -e "$WORK" || { echo "Refusing to overwrite $WORK"; exit 2; }
mkdir -p "$WORK"
cd "$WORK"
cp "$PEPXML" search.pep.xml
"$PHIL" workspace --init
"$PHIL" database --annotate "$FASTA" --prefix DECOY_
"$PHIL" peptideprophet --database "$FASTA" --ppm --accmass --nonparam --decoy DECOY_ --decoyprobs search.pep.xml
grep -c peptideprophet_result interact-search.pep.xml || { echo 'prior3 ASSERT: PeptideProphet modelled 0 PSMs; documented guard fired'; exit 1; }
