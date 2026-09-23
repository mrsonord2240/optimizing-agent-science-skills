#!/bin/sh
# Pass-5 Input 3. The fixed SKILL.md Philosopher block run VERBATIM in pass5/phil/ on the same real
# Comet pepXML (search.pep.xml = comet.pep.xml, 6,113 spectrum_query).
PHIL="F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/tools/philosopher/philosopher.exe"
C="F:/OpenScience/audits/bio-proteomics-peptide-identification/rerun4/comet_out"
"$PHIL" workspace --init
"$PHIL" database --annotate "$C/target_decoy.fasta" --prefix DECOY_
"$PHIL" peptideprophet --database "$C/target_decoy.fasta" --ppm --accmass \
                       --nonparam --decoy DECOY_ --decoyprobs search.pep.xml
grep -c peptideprophet_result interact-search.pep.xml || { echo 'PeptideProphet modelled 0 PSMs'; exit 1; }
# --- the audit deliberately continued past the guard to test the rest of the block ---
"$PHIL" proteinprophet --maxppmdiff 2000000 interact-search.pep.xml
test -s interact.prot.xml || { echo 'ProteinProphet wrote no prot.xml'; exit 1; }
"$PHIL" filter --psm 0.01 --pep 0.01 --prot 0.01 --tag DECOY_ --picked --razor \
               --pepxml interact-search.pep.xml --protxml interact.prot.xml
"$PHIL" report
[ -s protein.tsv ] && [ "$(wc -l < protein.tsv)" -gt 1 ] || { echo 'filter converged on an EMPTY result'; exit 1; }
