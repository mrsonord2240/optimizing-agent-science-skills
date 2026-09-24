#!/bin/bash
set -euo pipefail
export PATH=/home/sci/micromamba/envs/dv-cli/bin:$PATH
OUT=/mnt/openscience/audits/bio-data-visualization-sequence-logos/run/exact-commit-20260923-200710
EX=$OUT/examples
cd "$OUT"
weblogo --format pdf --sequence-type dna --color-scheme classic --units bits --composition equiprobable --fineprint '' --size large < "$EX/aligned_motif.fa" > weblogo_dna.pdf
printf '>r1\nACGU\n>r2\nACGU\n>r3\nACGU\n' | weblogo --format png --sequence-type rna --units bits --composition equiprobable > weblogo_rna.png
printf '>r1\nAA\n>r2\nAA\n>r3\nAA\n>r4\nAA\n>r5\nAA\n' | weblogo --format logodata --sequence-type dna --units bits --composition equiprobable > weblogo_n5_default.txt
printf '>r1\nAA\n>r2\nAA\n>r3\nAA\n>r4\nAA\n>r5\nAA\n' | weblogo --format logodata --sequence-type dna --units bits --composition equiprobable --weight 0 > weblogo_n5_weight0.txt
test -s weblogo_dna.pdf
test -s weblogo_rna.png
test -s weblogo_n5_default.txt
test -s weblogo_n5_weight0.txt
if cmp -s weblogo_n5_default.txt weblogo_n5_weight0.txt; then
  echo 'default WebLogo prior did not change n=5 logodata' >&2
  exit 1
fi
echo "weblogo_version=$(weblogo --version 2>/dev/null)"
echo "assertions=dna_pdf_nonempty,rna_sequence_type_nonempty,small_n_prior_differs_from_weight0"
