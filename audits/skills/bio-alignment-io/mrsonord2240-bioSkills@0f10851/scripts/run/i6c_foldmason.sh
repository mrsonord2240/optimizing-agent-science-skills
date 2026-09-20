#!/bin/bash
# REAL structures: Foldmason easy-msa on 3 myoglobin-fold PDBs -> result_aa.fa / result_3di.fa (SKILL Related Skills claim: FASTA-loadable; report is HTML)
S=/mnt/openscience/audit-envs/alignment/public-data/structures
O=/mnt/openscience/audits/bio-alignment-io/run/data/fm; rm -rf $O; mkdir -p $O; cd $O
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
foldmason easy-msa $S/1MBN.pdb $S/1A6M.pdb $S/1EMY.pdb result tmp --report-mode 1 </dev/null > fm.log 2>&1
tail -2 fm.log; ls -l
head -c 200 result.html | head -3
