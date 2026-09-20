#!/bin/bash
# MAFFT nucleotide alignment of the 6 real HBB CDS with short ids (data/tools/hbb6_short.fa, made by i7_prep.py)
D=/mnt/openscience/audits/bio-alignment-io/run/data/tools; source /mnt/openscience/audit-envs/alignment/wsl_env.sh
mafft --quiet --auto $D/hbb6_short.fa > $D/hbb6_aln.fa </dev/null; grep -c '>' $D/hbb6_aln.fa
