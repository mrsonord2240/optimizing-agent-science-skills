#!/bin/bash
# Every WSL tool call of the re-audit (env `alignment`; `bash wsl_tools.sh <step>`; paths are /mnt/openscience/...).
# Steps: mafft_globins | hmmbuild_pf | hmmalign_globins | hmmalign_a2m | mafft_hbb | trim | muscle_help | muscle_ens8 | muscle_ens73
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-msa-parsing/run/regression_phase1
PUB=/mnt/openscience/audit-envs/alignment/public-data/msa
cd $R/data
case "$1" in
mafft_globins)   # 8 REAL UniProt globins, L-INS-i
  mafft --version 2>&1 | head -1
  mafft --localpair --maxiterate 1000 --quiet $PUB/globins_uniprot.fasta < /dev/null > globins8_mafft_linsi.fasta
  grep -c '>' globins8_mafft_linsi.fasta ;;
hmmbuild_pf)     # ground truth for Neff (hmmbuild eff_nseq) and the profile for hmmalign
  hmmbuild --amino -n pf --informat stockholm pf.hmm $PUB/PF00042_seed.sto < /dev/null > hmmbuild_out.txt 2>&1
  grep -v '^#' hmmbuild_out.txt | head -5 ;;
hmmalign_globins) # real HMMER output: '.' gaps, lowercase inserts, PP lines; 8 UniProt globins onto the Pfam globin profile
  hmmalign -o hmmalign_globins8.sto pf.hmm $PUB/globins_uniprot.fasta < /dev/null
  head -c 700 hmmalign_globins8.sto ;;
hmmalign_a2m)     # same alignment as A2M (HMMER writes it UNPADDED: rows differ in length, no '.' characters)
  hmmalign --outformat a2m -o hmmalign_globins8.a2m pf.hmm $PUB/globins_uniprot.fasta < /dev/null
  awk '/^>/{if(n)print n, l; n=$1; l=0; next}{l+=length($0)}END{print n, l}' hmmalign_globins8.a2m ;;
mafft_hbb)       # 6 clean RefSeq HBB CDS (nucleotide alignment)
  mafft --auto --quiet hbb6_cds.fa < /dev/null > hbb6_cds_mafft.fasta
  grep -c '>' hbb6_cds_mafft.fasta ;;
trim)
  trimal --version < /dev/null 2>&1 | head -2
  trimal -in pfam_PF00042_seed.fasta -out trimal_gappyout.fa -gappyout -colnumbering < /dev/null > trimal_colnumbering.txt 2>&1
  head -c 300 trimal_colnumbering.txt; echo
  clipkit pfam_PF00042_seed.fasta -m kpic-smart-gap -o clipkit_kpic.fa -l < /dev/null 2>&1 | tail -7 ;;
muscle_help)
  muscle -version < /dev/null 2>&1 | head -2
  muscle 2>&1 < /dev/null | grep -i "stratified\|addconfseq\|maxcc\|letterconf" | head -12
  echo "== guidance2 on PATH?"; which guidance guidance.pl 2>&1 | head -2; echo "(none expected)" ;;
muscle_ens8)     # exactly the four commands of SKILL.md "Identifying Unreliable Alignment Regions" step 3
  mkdir -p ens8 && cd ens8
  muscle -align $PUB/globins_uniprot.fasta -stratified -output ens.efa < /dev/null 2>&1 | tail -3
  muscle -maxcc ens.efa -output maxcc.afa < /dev/null 2>&1 | tail -3
  muscle -addconfseq ens.efa -output ens_cc.efa < /dev/null 2>&1 | tail -3
  ls -la; grep '^<' ens.efa | head -20 ;;
muscle_ens73)
  mkdir -p ens73 && cd ens73
  muscle -align ../pfam73_ungapped.fa -stratified -output ens.efa < /dev/null 2>&1 | tail -3
  muscle -maxcc ens.efa -output maxcc.afa < /dev/null 2>&1 | tail -3
  muscle -addconfseq ens.efa -output ens_cc.efa < /dev/null 2>&1 | tail -3
  ls -la ;;
*) echo "unknown step $1"; exit 2 ;;
esac
