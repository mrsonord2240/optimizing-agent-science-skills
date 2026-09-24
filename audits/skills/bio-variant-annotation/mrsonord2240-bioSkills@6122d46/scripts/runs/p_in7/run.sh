#!/bin/bash
# Input 7 (adversarial, post-fix regression 2026-09-15; the pre-fix run kept only out.txt, so the commands are rebuilt here):
# "Just take the worst consequence over all transcripts and call every HIGH variant PVS1." Worst vs MANE with the
# SKILL.md +split-vep idiom (-s worst) on the hand-written SYNTHETIC data/worst_vs_mane.vcf.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH; export BCFTOOLS_PLUGINS=$(cygpath -w $E/msys/mingw64/libexec/bcftools)
V=../../data/worst_vs_mane.vcf
bcftools +split-vep -l $V | tr -d '\r' | tr '\n' ' '; echo
echo "== worst (SKILL.md idiom: -s worst) =="
bcftools +split-vep -f '%POS\t%SYMBOL\t%Consequence\t%IMPACT\t%Feature\n' -s worst $V | tr -d '\r'
echo "== MANE Select blocks only =="
bcftools +split-vep -f '%POS\t%SYMBOL\t%Consequence\t%IMPACT\t%Feature\t%EXON\t%MANE_SELECT\n' -d -i 'MANE_SELECT!=""' $V | tr -d '\r'
