#!/bin/bash
# T3 determinism: run TM-align, Foldseek search and Foldmason twice, compare outputs byte-for-byte (after stripping time lines)
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-structural/run; cd $R/work; rm -rf det; mkdir det; cd det
S=$R/data/real_pdb
for i in 1 2; do
  TMalign $S/1MBN.pdb $S/1A3N.pdb -outfmt 2 | grep -v '^#Total' > tm$i.txt
  foldseek easy-search $S/1MBN.pdb $R/work/in2/custom fs$i.m8 tmp$i --format-output query,target,evalue,bits,alntmscore,qtmscore,ttmscore,lddt,alnlen,pident -v 0 >/dev/null 2>&1
  mkdir -p st; cp $S/1MBN.pdb $S/1A3N.pdb $S/1ATP.pdb $S/1HCK.pdb $S/2LHB.pdb st/
  foldmason easy-msa st/*.pdb fm$i tmpfm$i --refine-iters 100 -v 0 >/dev/null 2>&1
done
for f in tm fs; do ext=txt; [ $f = fs ] && ext=m8; cmp $f\1.$ext $f\2.$ext && echo "$f identical ($(wc -l < ${f}1.$ext) lines)"; done
cmp fm1_aa.fa fm2_aa.fa && cmp fm1_3di.fa fm2_3di.fa && echo "foldmason aa+3di identical ($(grep -c '>' fm1_aa.fa) seqs)"
