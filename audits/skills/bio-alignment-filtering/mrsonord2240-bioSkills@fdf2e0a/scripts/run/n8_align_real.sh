#!/bin/bash
# NEW input 8, step 1: REAL Illumina reads (usage: n8_align_real.sh <outdir> <source BAM>; used with the nf-core human PE BAM and the nf-core RNA-seq BAM)
# (nf-core human PE BAM: 2821 pairs) re-aligned with every aligner of the MAPQ table
# against the real 40 kb chr22 slice; plus bowtie2 -k 10 to enumerate loci (independent multiplicity truth).
set -u
D=$1; SRC=$2; mkdir -p $D; cd $D
G=$AFDATA/human/genome.fasta
cp $G g.fa; samtools faidx g.fa
samtools view -b -F 2304 $SRC | samtools collate -O -u - tmpc | samtools fastq -1 r1.fq -2 r2.fq -0 /dev/null -s /dev/null -n - 2>/dev/null
echo "pairs: $(( $(wc -l < r1.fq) / 4 )) / $(( $(wc -l < r2.fq) / 4 ))"
bwa index g.fa >/dev/null 2>&1
bwa mem -t 4 g.fa r1.fq r2.fq 2>/dev/null | samtools sort -o bwa.bam - && samtools index bwa.bam
bowtie2-build g.fa bt2 >/dev/null 2>&1
bowtie2 -x bt2 -1 r1.fq -2 r2.fq -p 4 2>bt2.log | samtools sort -o bowtie2.bam - && samtools index bowtie2.bam; tail -1 bt2.log
bowtie2 -x bt2 -1 r1.fq -2 r2.fq -p 4 --local 2>bt2l.log | samtools sort -o bowtie2_local.bam - && samtools index bowtie2_local.bam; tail -1 bt2l.log
bowtie2 -x bt2 -1 r1.fq -2 r2.fq -p 4 -k 10 2>bt2k.log | samtools sort -o bowtie2_k10.bam - && samtools index bowtie2_k10.bam
hisat2-build g.fa ht2 >/dev/null 2>&1
hisat2 -x ht2 -1 r1.fq -2 r2.fq -p 4 2>ht2.log | samtools sort -o hisat2.bam - && samtools index hisat2.bam; tail -1 ht2.log
minimap2 -ax sr g.fa r1.fq r2.fq 2>/dev/null | samtools sort -o minimap2.bam - && samtools index minimap2.bam
mkdir -p star_idx
STAR --runMode genomeGenerate --genomeDir star_idx --genomeFastaFiles g.fa --genomeSAindexNbases 6 --outFileNamePrefix star_idx/ >/dev/null 2>&1
STAR --genomeDir star_idx --readFilesIn r1.fq r2.fq --outSAMtype BAM SortedByCoordinate --outSAMattributes NH HI AS nM --outFileNamePrefix star_ --runThreadN 4 >/dev/null 2>&1
mv star_Aligned.sortedByCoord.out.bam star.bam && samtools index star.bam
for a in bwa bowtie2 bowtie2_local bowtie2_k10 hisat2 minimap2 star; do echo "$a: $(samtools view -c $a.bam) records, $(samtools view -c -F 2308 $a.bam) primary mapped"; done
