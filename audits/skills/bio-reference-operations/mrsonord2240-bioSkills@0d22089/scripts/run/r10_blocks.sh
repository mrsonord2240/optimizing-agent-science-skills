#!/bin/bash
# Every `samtools consensus ...` command line printed in SKILL.md (snippets 13-19), run as written with input.bam -> a real BAM and reference.fa/ref.fa -> its FASTA.
# Judged by OUTPUT: rc 0 AND a non-empty FASTA/FASTQ record with the expected header; the --config profile names must be accepted.
R=/mnt/openscience/audits/bio-reference-operations/run
W=$R/work/r10; rm -rf $W; mkdir -p $W; cd $W
cp $R/data/real/test.paired_end.sorted.bam* $R/data/real/genome.fasta* .
BAM=test.paired_end.sorted.bam
n=0; bad=0
for f in $R/snippets/skill_13_bash.txt $R/snippets/skill_14_bash.txt $R/snippets/skill_15_bash.txt $R/snippets/skill_16_bash.txt $R/snippets/skill_17_bash.txt $R/snippets/skill_18_bash.txt $R/snippets/skill_19_bash.txt; do
  grep -E '^samtools consensus' $f | sed -e "s/#.*//" | while IFS= read -r line; do
    cmd=$(echo "$line" | sed -e "s#input.bam#$BAM#" -e 's#-r chr1:1000-2000#-r chr22:2000-2500#' -e 's#-T ref.fa#-T genome.fasta#' -e 's#-o [a-z_]*\.f[aq]#-o out.txt#')
    rm -f out.txt
    eval "$cmd" 2> err.txt; rc=$?
    sz=$(wc -c < out.txt 2>/dev/null); first=$(head -c1 out.txt 2>/dev/null)
    echo "rc=$rc bytes=$sz first='$first' :: $cmd"
  done
done
echo "--- bcftools consensus lines (placeholders reference.fa / variants.vcf.gz do not exist; syntax checked with --help only)"
bcftools consensus --help 2>&1 | grep -E -- '-H, --haplotype|-s, --sample|-f, --fasta-ref' | head -3
