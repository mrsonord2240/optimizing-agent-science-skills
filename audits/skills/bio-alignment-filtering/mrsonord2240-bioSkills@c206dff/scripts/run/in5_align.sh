#!/bin/bash
# Input 5a: align the synthetic repeat-genome reads with each aligner in the SKILL.md MAPQ table.
set -u
D=$1; cd $D
python $2/make_repeat_genome.py $D
samtools faidx g.fa
# BWA-MEM
bwa index g.fa >/dev/null 2>&1
bwa mem -t 4 g.fa reads.fq 2>/dev/null | samtools sort -o bwa.bam - && samtools index bwa.bam
# Bowtie2
bowtie2-build g.fa bt2 >/dev/null 2>&1
bowtie2 -x bt2 -U reads.fq -p 4 2>bt2.log | samtools sort -o bowtie2.bam - && samtools index bowtie2.bam; tail -1 bt2.log
# HISAT2
hisat2-build g.fa ht2 >/dev/null 2>&1
hisat2 -x ht2 -U reads.fq -p 4 2>ht2.log | samtools sort -o hisat2.bam - && samtools index hisat2.bam; tail -1 ht2.log
# minimap2 short-read preset
minimap2 -ax sr g.fa reads.fq 2>/dev/null | samtools sort -o minimap2.bam - && samtools index minimap2.bam
# STAR (tiny genome)
mkdir -p star_idx
STAR --runMode genomeGenerate --genomeDir star_idx --genomeFastaFiles g.fa --genomeSAindexNbases 6 --outFileNamePrefix star_idx/ >/dev/null 2>&1
STAR --genomeDir star_idx --readFilesIn reads.fq --outSAMtype BAM SortedByCoordinate --outSAMattributes NH HI AS nM --outFileNamePrefix star_ --runThreadN 4 >/dev/null 2>&1
mv star_Aligned.sortedByCoord.out.bam star.bam && samtools index star.bam
for a in bwa bowtie2 hisat2 minimap2 star; do echo "$a: $(samtools view -c $a.bam) records"; done
