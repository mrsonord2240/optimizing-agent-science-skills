#!/bin/bash
# Probe (self-contained): which REF_PATH forms make samtools find a CRAM's reference?
# Fixtures come from public-data (real human chr22 slice CRAM + FASTA). Counts are records printed for chr22:1952-1960 (truth: 2).
set -u
R=/mnt/openscience/audits/bio-alignment-indexing/run
rm -rf $R/work/rp && mkdir -p $R/work/rp && cd $R/work/rp
cp $AFDATA/human/test.paired_end.sorted.cram s.cram; cp $AFDATA/human/genome.fasta genome.fasta
samtools index s.cram
MD5=$(samtools dict genome.fasta | grep -o 'M5:[0-9a-f]*' | cut -d: -f2); echo "MD5=$MD5"
SEQ=$(grep -v '^>' genome.fasta | tr -d '\n' | tr a-z A-Z)
mkdir -p flat nested/${MD5:0:2}/${MD5:2:2} plain
printf '%s' "$SEQ" > flat/$MD5
printf '%s' "$SEQ" > nested/${MD5:0:2}/${MD5:2:2}/${MD5:4}
cp genome.fasta plain/
n() { samtools view s.cram chr22:1952-1960 2>/dev/null | wc -l; }
echo "no reference at all                           : $(n)  (expect 0: Failed to populate reference)"
echo "REF_PATH=<dir holding genome.fasta (plain)>   : $(REF_PATH=$PWD/plain n)  (expect 0: REF_PATH is an MD5 store, not a FASTA dir)"
echo "REF_PATH=<flat dir of MD5-named files>        : $(REF_PATH=$PWD/flat n)  (expect 2)"
echo "REF_PATH=<bare dir with nested 19/22/... tree>: $(REF_PATH=$PWD/nested n)  (expect 0: nested layout needs the %2s/%2s/%s pattern)"
echo "REF_PATH='<dir>/%2s/%2s/%s' nested pattern    : $(REF_PATH="$PWD/nested/%2s/%2s/%s" n)  (expect 2)"
echo "samtools view -T genome.fasta                 : $(samtools view -T genome.fasta s.cram chr22:1952-1960 | wc -l)  (expect 2)"
# @SQ UR: CRAM re-encoded with an absolute local reference path
samtools view -b -T genome.fasta s.cram > s.bam 2>/dev/null; samtools index s.bam
samtools view -C -T $PWD/genome.fasta -o ur.cram s.bam; samtools index ur.cram
echo "@SQ UR path exists (ur.cram, no -T)           : $(samtools view ur.cram chr22:1952-1960 2>/dev/null | wc -l)  (expect 2)"
mv genome.fasta moved.fa
echo "@SQ UR path moved away (ur.cram, no -T)       : $(samtools view ur.cram chr22:1952-1960 2>/dev/null | wc -l)  (expect 0)"
mv moved.fa genome.fasta
