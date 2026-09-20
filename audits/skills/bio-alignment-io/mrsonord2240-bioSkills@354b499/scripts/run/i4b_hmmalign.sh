#!/bin/bash
# REAL data: build HMM from real Pfam PF00042 seed, align 8 real UniProt globins to it -> real A2M (lowercase inserts, '.' gaps) and Pfam-format
set -e
D=/mnt/openscience/audits/bio-alignment-io/run/data
P=/mnt/openscience/audit-envs/alignment/public-data/msa
hmmbuild --amino $D/pf00042.hmm $P/PF00042_seed.sto > $D/hmmbuild.log
hmmalign --amino --outformat A2M $D/pf00042.hmm $P/globins_uniprot.fasta > $D/globins_hmm.a2m
hmmalign --amino --outformat Pfam $D/pf00042.hmm $P/globins_uniprot.fasta > $D/globins_hmm.sto
grep -E '^LENG' $D/pf00042.hmm
head -c 400 $D/globins_hmm.a2m
