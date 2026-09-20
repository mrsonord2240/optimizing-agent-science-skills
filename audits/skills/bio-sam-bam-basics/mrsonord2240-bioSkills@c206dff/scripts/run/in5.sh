#!/bin/bash
# Input 5 pipeline: align the SYNTHETIC repeat-containing pairs with five aligners, plus fixmate/markdup chain.
# Everything that later asserts lives in in5.py; this only produces BAMs under data/aln/.
set -u
cd /mnt/openscience/audits/bio-sam-bam-basics/run
python make_reads.py
cd data/aln
G=g.fa; R1=r1.fq; R2=r2.fq
RG='@RG\tID:rgA\tSM:synS\tPL:ILLUMINA'
T=4
echo "== bwa mem"; bwa index $G >/dev/null 2>&1; bwa mem -t $T -R "$RG" $G $R1 $R2 2>/dev/null | samtools sort -o bwa.bam - && samtools index bwa.bam
echo "== bwa-mem2"; bwa-mem2 index $G >/dev/null 2>&1; bwa-mem2 mem -t $T $G $R1 $R2 2>/dev/null | samtools sort -o bwamem2.bam - && samtools index bwamem2.bam
echo "== minimap2 sr"; minimap2 -t $T -ax sr $G $R1 $R2 2>/dev/null | samtools sort -o mm2.bam - && samtools index mm2.bam
echo "== minimap2 sr --eqx"; minimap2 -t $T -ax sr --eqx $G $R1 $R2 2>/dev/null | samtools sort -o mm2eqx.bam - && samtools index mm2eqx.bam
echo "== bowtie2"; bowtie2-build $G bt2idx >/dev/null 2>&1; bowtie2 -p $T -x bt2idx -1 $R1 -2 $R2 2>bt2.log | samtools sort -o bt2.bam - && samtools index bt2.bam; tail -1 bt2.log
echo "== hisat2"; hisat2-build $G hs2idx >/dev/null 2>&1; hisat2 -p $T -x hs2idx -1 $R1 -2 $R2 2>hs2.log | samtools sort -o hs2.bam - && samtools index hs2.bam; tail -1 hs2.log
echo "== STAR"; mkdir -p staridx; STAR --runMode genomeGenerate --genomeDir staridx --genomeFastaFiles $G --genomeSAindexNbases 6 --runThreadN $T --outFileNamePrefix star_gen_ >/dev/null 2>&1
STAR --genomeDir staridx --readFilesIn $R1 $R2 --runThreadN $T --outSAMtype BAM SortedByCoordinate --outSAMattributes NH HI AS nM NM MD --outFileNamePrefix star_ >/dev/null 2>&1; mv star_Aligned.sortedByCoord.out.bam star.bam; samtools index star.bam
STAR --genomeDir staridx --readFilesIn $R1 $R2 --runThreadN $T --outSAMtype BAM SortedByCoordinate --outSAMattributes NH HI AS nM --outSAMattrIHstart 0 --outFileNamePrefix star0_ >/dev/null 2>&1; mv star0_Aligned.sortedByCoord.out.bam star_ih0.bam
echo "== fixmate/markdup chain (samtools 1.24)"
bwa mem -t $T $G $R1 $R2 2>/dev/null | samtools collate -O -u - | samtools fixmate -m -u - - | samtools sort -u - | samtools markdup - chain.bam
samtools index chain.bam
echo "== markdup on a BAM without ms/MC"
samtools view -h -x ms -x MC bwa.bam | samtools collate -O -u - | samtools fixmate - - | samtools sort -o nomc.bam - 2> nomc.err; samtools markdup nomc.bam nomc_md.bam 2> nomc_md.err; echo "markdup-without-fixmate rc=$?"
ls -la *.bam | awk '{print $5, $9}'
