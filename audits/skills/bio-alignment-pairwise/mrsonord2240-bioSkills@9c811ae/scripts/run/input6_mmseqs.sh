#!/bin/bash
# Scope-boundary route: skill says 'one query vs many targets -> MMseqs2, do not iterate Bio.Align'. 8 real UniProt globins all-vs-all.
cd /mnt/openscience/audits/bio-alignment-pairwise/run/data
mkdir -p mm_tmp
mmseqs easy-search globins_uniprot.fasta globins_uniprot.fasta mm_out.tsv mm_tmp --format-output query,target,raw,bits,pident,evalue,alnlen,qstart,qend,tstart,tend -s 7.5 --min-seq-id 0 -e 1000 -v 1 >/dev/null 2>&1
echo "rows: $(wc -l < mm_out.tsv)"
grep -E 'P69905.*P68871|P68871.*P69905' mm_out.tsv | head
