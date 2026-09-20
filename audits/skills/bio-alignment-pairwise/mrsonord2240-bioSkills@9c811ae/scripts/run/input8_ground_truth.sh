#!/bin/bash
# Independent ground truth for input 8 (WSL env alignment): EMBOSS needle/water and BLAST+ 2.17.0 on the PKA/CDK2 pair
cd /mnt/openscience/audits/bio-alignment-pairwise/run/data
python3 - <<'PY'
recs=open('kin.fasta').read().split('>')[1:]
for r,n in zip(recs,('pka.fa','cdk.fa')): open(n,'w').write('>'+r)
PY
echo "--- needle 11/1 (end gaps penalised) global"; needle -asequence pka.fa -bsequence cdk.fa -datafile EBLOSUM62 -gapopen 11 -gapextend 1 -endweight Y -endopen 11 -endextend 1 -outfile kin_needle_11_1.txt -auto 2>&1|tail -1; grep -E '^# (Score|Identity)' kin_needle_11_1.txt
echo "--- needle 10/0.5"; needle -asequence pka.fa -bsequence cdk.fa -datafile EBLOSUM62 -gapopen 10 -gapextend 0.5 -endweight Y -endopen 10 -endextend 0.5 -outfile kin_needle_10_05.txt -auto 2>&1|tail -1; grep -E '^# (Score|Identity)' kin_needle_10_05.txt
echo "--- needle 12/1"; needle -asequence pka.fa -bsequence cdk.fa -datafile EBLOSUM62 -gapopen 12 -gapextend 1 -endweight Y -endopen 12 -endextend 1 -outfile kin_needle_12_1.txt -auto 2>&1|tail -1; grep -E '^# (Score)' kin_needle_12_1.txt
echo "--- water 11/1"; water -asequence pka.fa -bsequence cdk.fa -gapopen 11 -gapextend 1 -outfile kin_water_11.txt -auto 2>&1|tail -1; grep -E '^# Score' kin_water_11.txt
echo "--- water 12/1"; water -asequence pka.fa -bsequence cdk.fa -gapopen 12 -gapextend 1 -outfile kin_water_12.txt -auto 2>&1|tail -1; grep -E '^# Score' kin_water_12.txt
echo "--- blastp gapopen 11 gapextend 1 (BLASTP default gaps), comp_based_stats 0, seg no: raw score + HSP"
blastp -query pka.fa -subject cdk.fa -matrix BLOSUM62 -gapopen 11 -gapextend 1 -comp_based_stats 0 -seg no -outfmt '6 qseqid sseqid score bitscore evalue length pident qstart qend sstart send' 2>&1 | head -3
echo "--- blastp default parameters (comp-based stats on)"
blastp -query pka.fa -subject cdk.fa -outfmt '6 qseqid sseqid score bitscore evalue pident qstart qend sstart send' 2>&1 | head -3
