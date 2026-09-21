#!/bin/bash
# Input 4: WebLogo CLI in WSL (science/dv-cli). Run: MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc 'bash /mnt/openscience/audits/bio-data-visualization-sequence-logos/run/i4_weblogo.sh'
export PATH=/home/sci/micromamba/envs/dv-cli/bin:$PATH
R=/mnt/openscience/audits/bio-data-visualization-sequence-logos/run
D=$R/data; O=$R/out/wl; mkdir -p $O; cd $O
W="weblogo"
mk() { awk '{print ">s"NR; print $0}' $1 > $2; }
mk $D/dna_n5.txt n5.fa; mk $D/dna_n200.txt n200.fa; mk $D/dna_gcrich_n500.txt gc500.fa; mk $D/rna_n200.txt rna200.fa; mk $D/prot_n200.txt prot200.fa
echo "== weblogo $($W --version 2>/dev/null)"
echo "== SKILL command verbatim (pdf) on n=200"
$W --format pdf --sequence-type dna --color-scheme classic --units bits --composition equiprobable --fineprint '' --size large < n200.fa > logo_skill_n200.pdf 2> pdf.err; echo "exit=$? bytes=$(stat -c %s logo_skill_n200.pdf)"; grep -v -e pkg_resources -e DistributionNotFound pdf.err | head -5
echo "== formats on n=200"
for f in png png_print svg eps jpeg; do $W --format $f --sequence-type dna --units bits --composition equiprobable --size large < n200.fa > logo_n200.$f 2> $f.err; echo "$f exit=$? bytes=$(stat -c %s logo_n200.$f)"; grep -v -e pkg_resources -e DistributionNotFound $f.err | head -3; done
echo "== logodata (numbers)"
for n in n5 n200; do $W --format logodata --sequence-type dna --units bits --composition equiprobable < $n.fa > $n.equi.logodata 2>/dev/null; $W --format logodata --sequence-type dna --units bits --composition equiprobable --weight 0 < $n.fa > $n.equi.w0.logodata 2>/dev/null; $W --format logodata --sequence-type dna --units bits --composition none < $n.fa > $n.none.logodata 2>/dev/null; done
$W --format logodata --sequence-type dna --units bits --composition 64 < gc500.fa > gc500.cg64.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units bits --composition equiprobable < gc500.fa > gc500.equi.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units bits --composition "{'A':0.18,'C':0.32,'G':0.32,'T':0.18}" < gc500.fa > gc500.dict.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units bits --composition "H. sapiens" < n200.fa > n200.human.logodata 2>/dev/null; echo "H. sapiens exit=$?"
$W --format logodata --sequence-type rna --units bits --composition equiprobable < rna200.fa > rna200.logodata 2>/dev/null; echo "rna exit=$?"
$W --format logodata --sequence-type dna --units bits < rna200.fa > rna_as_dna.logodata 2> rna_as_dna.err; echo "rna fed as dna exit=$? lines=$(wc -l < rna_as_dna.logodata)"
$W --format logodata --sequence-type protein --units bits --composition equiprobable < prot200.fa > prot200.logodata 2>/dev/null; echo "protein exit=$?"
$W --format logodata --sequence-type protein --units bits < prot200.fa > prot200.auto.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units probability < n200.fa > n200.prob.logodata 2>/dev/null
$W --format png --sequence-type dna --units probability --composition equiprobable < n200.fa > logo_n200_prob.png 2>/dev/null
$W --format png --sequence-type dna --units bits --composition equiprobable --size large < n5.fa > logo_n5.png 2>/dev/null
$W --format png --sequence-type rna --units bits < rna200.fa > logo_rna200.png 2>/dev/null
$W --format png --sequence-type protein --units bits --color-scheme chemistry < prot200.fa > logo_prot200.png 2>/dev/null
$W --format png --sequence-type dna --units bits --composition 64 < gc500.fa > logo_gc500_cg64.png 2>/dev/null
$W --format png --sequence-type dna --units bits --composition equiprobable < gc500.fa > logo_gc500_equi.png 2>/dev/null
# unequal length / bad input
printf ">a\nACGT\n>b\nACG\n" | $W --format logodata --sequence-type dna > uneq.out 2> uneq.err; echo "unequal-length exit=$? :: $(grep -v -e pkg_resources -e DistributionNotFound uneq.err | tail -1)"
ls -la
