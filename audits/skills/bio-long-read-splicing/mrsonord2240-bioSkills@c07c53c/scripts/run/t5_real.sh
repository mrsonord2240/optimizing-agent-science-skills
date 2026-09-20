#!/bin/bash
# REAL long reads (LRGASP WTC-11 cDNA, FLAIR test set, hg38 chr12/17/20): run the Skill's OWN code blocks (extracted verbatim by extract_blocks.py) in a work dir
# that has the file names the blocks expect. Nothing is written into public-data (all copied).
R=/mnt/openscience/audits/bio-long-read-splicing/run; P=/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/flair_test
B=$R/out/blocks; O=$R/out/real; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
cp $P/genome.fa reference.fa; cp $P/input/basic.annotation.gtf gencode.v45.annotation.gtf; cp $P/input/basic.shortread_junctions.tab SJ.out.tab
gzip -c $P/input/basic.reads.fa > isoseq.fastq.gz; cp isoseq.fastq.gz ont_cdna.fastq.gz; cp isoseq.fastq.gz ont_rna.fastq.gz; cp isoseq.fastq.gz sample.fastq.gz
cp $P/input/basic.reads.1.fa s1.fa; cp $P/input/basic.reads.2.fa s2.fa; cp $P/input/basic.reads.3.fa s3.fa; cp $P/input/basic.reads.4.fa s4.fa; cp $P/input/basic.reads.5.fa s5.fa; cp $P/input/basic.reads.6.fa s6.fa
gzip -c s1.fa > sample1.fastq.gz; gzip -c s2.fa > sample2.fastq.gz
printf 'A1\tA\tb0\t%s/s1.fa\nA2\tA\tb0\t%s/s2.fa\nA3\tA\tb0\t%s/s3.fa\nB1\tB\tb0\t%s/s4.fa\nB2\tB\tb0\t%s/s5.fa\nB3\tB\tb0\t%s/s6.fa\n' $O $O $O $O $O $O > reads_manifest.tsv
echo "############ splice-aware-alignment_1.sh (verbatim: gffread + 3 minimap2 recipes, -t 16)"
bash $B/splice-aware-alignment_1.sh > align_block.log 2>&1; echo "rc=$?"; ls -la *_aligned.bam annotation.bed12 | awk '{print $5, $9}'
for b in isoseq_aligned ont_cdna_aligned ont_rna_aligned; do echo "$b: spliced primary reads $(samtools view -F 2308 -c $b.bam), flagstat: $(samtools flagstat $b.bam | sed -n 1p)"; done
echo "############ orientation check block (verbatim) on the ONT-cDNA (no -uf) alignment, and on the isoseq alignment"
cp ont_cdna_aligned.bam aligned.bam; cp ont_cdna_aligned.bam.bai aligned.bam.bai
echo "ont_cdna (no -uf): $(bash $B/splice-aware-alignment_2.sh)"
cp isoseq_aligned.bam aligned.bam; cp isoseq_aligned.bam.bai aligned.bam.bai
echo "isoseq recipe (splice:hq, no -uf): $(bash $B/splice-aware-alignment_2.sh)"
cp ont_cdna_aligned.bam aligned.bam; cp ont_cdna_aligned.bam.bai aligned.bam.bai
echo "############ FLAIR block (verbatim, incl. diffSplice --test)"
bash $B/flair-workflow-correct-collapse-quantify_1.sh > flair_block.log 2>&1; echo "rc=$?"
grep -a -i -E "error|Traceback|failed|took" flair_block.log | head -12
ls flair_* | head -40
echo "counts.tsv head:"; head -3 flair_quantified.counts.tsv | cut -c1-200
echo "corrected reads: $(wc -l < flair_corrected_all_corrected.bed)  inconsistent: $(wc -l < flair_corrected_all_inconsistent.bed)  collapsed isoforms: $(grep -c '>' flair_collapsed.isoforms.fa)"
