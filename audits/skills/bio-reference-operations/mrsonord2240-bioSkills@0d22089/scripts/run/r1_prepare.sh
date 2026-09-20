#!/bin/bash
# INPUT 1 (regression of pre-fix input 1, extended): shipped examples/prepare_reference.sh run from a COPY
# on many reference filename shapes; then GATK 4.6.2.0 HaplotypeCaller and Picard 3.5.0 ValidateSamFile must actually LOAD each reference.
R=/mnt/openscience/audits/bio-reference-operations/run
W=$R/work/r1; rm -rf $W; mkdir -p $W; cd $W
cp $R/skill/examples/prepare_reference.sh .
BAM=$R/data/real/test.paired_end.sorted.bam
SRC=$R/data/real/genome.fasta

mk() { # mk <relative-path> [gz]
  local p="$1"; mkdir -p "$(dirname "$p")"; cp $SRC "$p"; if [ "$2" = gz ]; then bgzip "$p"; fi
}
declare -a SHAPES=(
  "s1/genome.fasta" "s2/ref.fa" "s3/ref2.fna" "s4/refz.fa.gz" "s5/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"
  "s6/hg38.p14.v2.fasta" "s7/genome.fna.gz" "s8/genome.fasta.gz" "s9/my genome.fasta" "s10.v2/noext" "s11/GENOME.FA" "s12/ref.fas"
)
for s in "${SHAPES[@]}"; do
  gz=""; case "$s" in *.gz) gz=gz; s="${s%.gz}";; esac
  mk "$s" $gz
done
# re-add .gz to names for the ones that were gz
for s in "${SHAPES[@]}"; do
  f="$s"
  echo; echo "########## SHAPE: $f"
  d=$(dirname "$f"); b=$(basename "$f")
  (cd "$d" && bash $W/prepare_reference.sh "$b" > $W/out_$(echo "$f" | tr '/ ' '__').txt 2>&1; echo "prepare rc=$?"; ls)
done
echo; echo "########## error paths"
bash prepare_reference.sh; echo "no-arg rc=$?"
bash prepare_reference.sh nope.fa; echo "missing rc=$?"
