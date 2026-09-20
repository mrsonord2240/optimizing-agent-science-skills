#!/bin/bash
# REAL structures (public-data): Foldmason easy-msa on 3 myoglobin-fold PDBs -> result_aa.fa / result_3di.fa (SKILL related-skills claim: FASTA-loadable)
S=/mnt/openscience/audit-envs/alignment/public-data/structures
O=/mnt/openscience/audits/bio-alignment-io/run/data/fm; rm -rf $O; mkdir -p $O; cd $O
foldmason easy-msa $S/1MBN.pdb $S/1A6M.pdb $S/1EMY.pdb result tmp --report-mode 0 </dev/null > fm.log 2>&1
tail -2 fm.log; ls
