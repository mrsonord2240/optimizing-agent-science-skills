#!/bin/bash
# Ground truth from independent tools (WSL). Run: wsl_run.sh 'bash /mnt/openscience/audits/bio-alignment-pairwise/run/input1_emboss_blast.sh'
cd /mnt/openscience/audits/bio-alignment-pairwise/run/data
python3 - <<'PY'
from itertools import islice
recs=open('hba_hbb.fasta').read().split('>')[1:]
for r,n in zip(recs,('hba.fa','hbb.fa')):
    open(n,'w').write('>'+r)
PY
echo "--- needle open 11 ext 1, end gaps penalised (-endweight Y, endopen 11 endextend 1), BLOSUM62"
needle -asequence hba.fa -bsequence hbb.fa -datafile EBLOSUM62 -gapopen 11 -gapextend 1 -endweight Y -endopen 11 -endextend 1 -outfile needle_11_1.txt -auto 2>&1 | tail -2
grep -E '^# (Score|Identity|Similarity|Gaps|Length)' needle_11_1.txt
echo "--- needle open 10 ext 0.5 (EMBOSS default gaps), end gaps penalised"
needle -asequence hba.fa -bsequence hbb.fa -datafile EBLOSUM62 -gapopen 10 -gapextend 0.5 -endweight Y -endopen 10 -endextend 0.5 -outfile needle_10_05.txt -auto 2>&1 | tail -2
grep -E '^# (Score|Identity|Similarity|Gaps|Length)' needle_10_05.txt
echo "--- needle default (end gaps NOT penalised)"
needle -asequence hba.fa -bsequence hbb.fa -gapopen 10 -gapextend 0.5 -outfile needle_default.txt -auto 2>&1 | tail -2
grep -E '^# (Score|Identity)' needle_default.txt
echo "--- water 10/0.5"
water -asequence hba.fa -bsequence hbb.fa -gapopen 10 -gapextend 0.5 -outfile water.txt -auto 2>&1|tail -2
grep -E '^# (Score|Identity|Length)' water.txt
echo "--- water 11/1 and 12/1 (local, EMBOSS convention == Biopython convention)"
for o in 11 12; do water -asequence hba.fa -bsequence hbb.fa -gapopen $o -gapextend 1 -outfile water_$o.txt -auto 2>&1|tail -1; echo "water open=$o ext=1: $(grep '^# Score' water_$o.txt)"; done
echo "--- BLASTP (gapopen 11 gapextend 1 = BLASTP defaults), no comp-based stats, no seg"
blastp -query hba.fa -subject hbb.fa -matrix BLOSUM62 -gapopen 11 -gapextend 1 -comp_based_stats 0 -seg no -outfmt '6 qseqid sseqid score bitscore evalue length pident qstart qend sstart send' 2>&1 | head
