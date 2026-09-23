#!/bin/bash
# Every fenced bash block of SKILL.md must parse (bash -n) and every python block must compile; then run the simple ones on the real human BAM with placeholders filled.
export LC_ALL=C
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work; rm -rf sweep; mkdir sweep; cd sweep
cp $AFDATA/human/test.paired_end.sorted.bam input.bam; cp $AFDATA/human/test.paired_end.sorted.bam.bai input.bam.bai
printf 'chr22\t1951\t4617\n' > regions.bed; cp $AFDATA/human/genome.fasta ref.fa; cp $AFDATA/human/genome.fasta.fai ref.fa.fai
for f in $R/blocks/*_bash.sh; do bash -n $f 2>/dev/null && echo "syntax OK  $(basename $f)" || echo "SYNTAX FAIL $(basename $f)"; done
for f in $R/blocks/*_python.py; do python -m py_compile $f 2>/dev/null && echo "compile OK $(basename $f)" || echo "COMPILE FAIL $(basename $f)"; done
rm -rf $R/blocks/__pycache__
echo "--- run the plain command blocks (placeholder input.bam / regions.bed / ref.fa; chr1 regions replaced by chr22)"
for n in 002 004 005 006 008 009 010 013 014 015 016 017 019 021 022 023 024 025 026; do
  sed 's#chr1:1000000-2000000#chr22:1952-2952#; s#chr1:1000-2000#chr22:1952-2952#; s#chr1:1-10000000#chr22:1-40001#' $R/blocks/${n}_bash.sh > run_$n.sh
  out=$(bash run_$n.sh 2>&1 | head -3 | tr '\n' '|' | cut -c1-140); echo "block $n rc=${PIPESTATUS[0]} : $out"
done
