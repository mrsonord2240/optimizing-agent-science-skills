#!/bin/bash
# Size scan of the microexon recipe with a SKIPPING-read control: sizes 4,5,6,8,10,15,18,21 nt (gene MX1..MX8 in that order), 200 inc + 200 skip reads each.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/micro_scan; O=$R/out/micro_scan; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
gffread $D/ref_full.gtf --bed -o full.bed12
echo "sizes: MX1=4 MX2=5 MX3=6 MX4=8 MX5=10 MX6=15 MX7=18 MX8=21 nt"
for P in hifi ontunstr drna; do
  case $P in hifi) PRE="splice:hq";; ontunstr) PRE="splice -k14";; drna) PRE="splice -uf -k14";; esac
  for V in "plain|" "juncbed|--junc-bed full.bed12" "juncbed+bonus20|--junc-bed full.bed12 --junc-bonus 20"; do
    N=${V%%|*}; A=${V#*|}
    minimap2 -ax $PRE --secondary=no $A -t 8 $D/chrU.fa $D/$P.fastq 2>/dev/null | samtools sort -o t.bam - 2>/dev/null; samtools index t.bam
    asenv as-lr python $R/micro_table.py t.bam $D/truth_chains.tsv "$P $N"
  done
done
