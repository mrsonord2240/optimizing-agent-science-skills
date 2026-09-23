#!/bin/sh
# Pass-5 Input 2. The fixed SKILL.md "Protein Groups from the CLI" Percolator block, run VERBATIM
# (paths substituted) on PXD070049 Condition_A REP1 Comet 2026.02 .pin + 31,437-protein target/DECOY_ FASTA.
P="F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/tools/percolator/percolator.exe"
C="F:/OpenScience/audits/bio-proteomics-peptide-identification/rerun4/comet_out"
"$P" -f "$C/target_decoy.fasta" -P DECOY_ -z trypsin \
     -l prot.target.tsv -L prot.decoy.tsv \
     -r pep.target.tsv  -B pep.decoy.tsv \
     -m psm.target.tsv  -M psm.decoy.tsv -S 1 "$C/comet.pin" > perc.log 2>&1
echo "exit=$?"
# SKILL.md OUTPUT CHECK, verbatim:
awk -F'\t' 'NR>1 && $3<=0.01' prot.target.tsv | wc -l
