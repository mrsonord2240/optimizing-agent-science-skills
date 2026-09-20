#!/bin/bash
# MAFFT nucleotide alignment of the 6 real HBB CDS -> data/hbb6_aln.fa (stdin closed)
D=/mnt/openscience/audits/bio-alignment-io/run/data
mafft --quiet --auto $D/hbb6.fa > $D/hbb6_aln.fa </dev/null
grep -c '>' $D/hbb6_aln.fa
