#!/bin/bash
export PATH=/home/sci/micromamba/envs/dv-cli/bin:$PATH
S=/mnt/openscience/audits/bio-data-visualization-sequence-logos/run
for f in logo_comparison multi_logo protein_logo; do pdftoppm -png -r 130 -singlefile $S/scratch_ex2/b/$f.pdf $S/out/ex/$f; done
ls -la $S/out/ex
