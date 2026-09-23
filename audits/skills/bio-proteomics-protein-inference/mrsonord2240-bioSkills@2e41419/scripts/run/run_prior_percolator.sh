#!/usr/bin/env bash
# Prior Input 2 replay: exact Percolator picked-protein route from the Skill reference.
set -euo pipefail
ENV='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst'
PERC="$ENV/tools/percolator/percolator.exe"
ROOT='F:/OpenScience/audits/bio-proteomics-protein-inference/run'
FASTA='F:/OpenScience/audits/bio-proteomics-peptide-identification/rerun4/comet_out/target_decoy.fasta'
PIN='F:/OpenScience/audits/bio-proteomics-peptide-identification/rerun4/comet_out/comet.pin'
WORK="$ROOT/outputs/prior2_percolator"
test ! -e "$WORK" || { echo "Refusing to overwrite $WORK"; exit 2; }
mkdir -p "$WORK"
cd "$WORK"
DECOY_PREFIX=DECOY_
"$PERC" -f "$FASTA" -P "$DECOY_PREFIX" -z trypsin \
  -l prot.target.tsv -L prot.decoy.tsv -r pep.target.tsv -B pep.decoy.tsv \
  -m psm.target.tsv -M psm.decoy.tsv -S 1 "$PIN"
PASSING=$(awk -F'\t' 'NR>1 && $3<=0.01 {n++} END {print n+0}' prot.target.tsv)
test "$PASSING" -eq 458
test -s prot.target.tsv
echo "prior2 ASSERT: Percolator wrote prot.target.tsv with $PASSING q<=0.01 representatives"
