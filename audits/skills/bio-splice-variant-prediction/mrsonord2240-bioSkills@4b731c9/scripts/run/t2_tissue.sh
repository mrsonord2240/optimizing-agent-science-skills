#!/bin/bash
# Input 2: examples/pangolin_tissue.py (SKILL.md command) vs CLI -m False output
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
FA=/mnt/openscience/as-spvp-scratch/g38/hg38_chr17_chrX.upper.fa
run() { micromamba run -n as-pangolin python skill/examples/pangolin_tissue.py "$@" --fasta $FA 2>&1 | grep -av "pkg_resources\|^$\|Using CPU"; }
echo "== TP53 c.673-2A>G (minus strand) [SKILL.md command]"; run chr17 7674292 T C --strand -
echo "== PLCXD1 G>A donor (plus strand)"; run chrX 276395 G A --strand +
echo "== OTC c.386+5G>A (plus)"; run chrX 38381434 G A --strand +
echo "== DMD c.9563+1G>A (minus)"; run chrX 31209497 C T --strand -
echo "== REF mismatch guard (wrong REF)"; run chr17 7674292 A C --strand -
