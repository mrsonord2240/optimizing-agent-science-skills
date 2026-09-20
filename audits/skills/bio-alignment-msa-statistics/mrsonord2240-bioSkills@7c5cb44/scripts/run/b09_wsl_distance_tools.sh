#!/bin/bash
# INPUT 6 (scope boundary) WSL half: the exact commands from SKILL.md "Distance Correction Models" on REAL alignments.
# Run: wsl_run.sh 'bash /mnt/openscience/audits/bio-alignment-msa-statistics/run/b09_wsl_distance_tools.sh'
W=/mnt/openscience/audits/bio-alignment-msa-statistics/run/work_b09
rm -rf $W; mkdir -p $W; cd $W
cp ../data/globins_mafft_default.fa alignment_aa.fasta      # 8 globins, protein
cp ../data/hbb6_mafft_default.fa   alignment_nt.fasta       # 6 HBB CDS, nucleotide, lowercase (MAFFT default)
echo "### modeltest-ng version"; micromamba run -n aln-mtng modeltest-ng --version </dev/null 2>&1 | grep -i -m1 "modeltest-ng"
echo "### SKILL.md: modeltest-ng -i alignment.fasta -d nt -t ml   (nucleotide, lowercase input)"
timeout 240 micromamba run -n aln-mtng modeltest-ng -i alignment_nt.fasta -d nt -t ml </dev/null > mt_nt.log 2>&1; echo "exit=$?"
grep -E "Best model according|BIC|AIC" mt_nt.log | head -8; tail -3 mt_nt.log | cut -c1-160
echo "### SKILL.md: modeltest-ng -i alignment.fasta -d aa -t ml -p 4   (protein, 8 globins)"
timeout 280 micromamba run -n aln-mtng modeltest-ng -i alignment_aa.fasta -d aa -t ml -p 4 </dev/null > mt_aa.log 2>&1; echo "exit=$?"
grep -E "Best model according|BIC|AIC" mt_aa.log | head -8; tail -3 mt_aa.log | cut -c1-160
echo "### IQ-TREE .mldist claim: iqtree3 -s alignment_aa.fasta -m LG (writes .mldist?)"
timeout 120 iqtree3 -s alignment_aa.fasta -m LG -redo -nt 2 </dev/null > iq.log 2>&1; echo "exit=$?"; ls alignment_aa.fasta.* | tr '\n' ' '; echo
head -3 alignment_aa.fasta.mldist | cut -c1-100
echo "### EMBOSS distmat (protein alignment, Kimura)"
distmat -sequence alignment_aa.fasta -protmethod 2 -outfile distmat_aa.txt </dev/null 2>&1 | tail -2; head -14 distmat_aa.txt | cut -c1-120
