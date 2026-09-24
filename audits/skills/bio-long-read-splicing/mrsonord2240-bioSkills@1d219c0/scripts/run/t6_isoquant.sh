#!/bin/bash
# SKILL "IsoQuant for Discovery + Quantification" block, verbatim (extracted), on MY planted HiFi reads (2 input files, default prefix OUT);
# then --illumina_bam on the novel-splice-site question.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/plant; B=$R/out/blocks; O=$R/out/iq; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
cp $D/chrQ.fa reference.fa; cp $D/ref.gtf gencode.v45.annotation.gtf
gzip -c $D/hifi/ctrl1.fastq > sample1.fastq.gz; gzip -c $D/hifi/trt1.fastq > sample2.fastq.gz
echo "########## block verbatim"; cat $B/isoquant-for-discovery-quantification_1.sh
bash $B/isoquant-for-discovery-quantification_1.sh > iq_block.log 2>&1; echo "rc=$?"
echo "files in isoquant_output/OUT:"; ls isoquant_output/OUT | tr '\n' ' '; echo
for f in transcript_models.gtf transcript_counts.tsv transcript_grouped_file_name_counts.tsv transcript_model_counts.tsv; do echo "SKILL names OUT.$f -> $([ -f isoquant_output/OUT/OUT.$f ] && echo EXISTS || echo MISSING)"; done
head -3 isoquant_output/OUT/OUT.transcript_grouped_file_name_counts.tsv 2>/dev/null
echo "########## --illumina_bam: short-read BAM (minimap2 -ax splice:sr) + long-read BAM (hifi recipe)"
minimap2 -ax splice:sr -t 8 $D/chrQ.fa $D/sr_ctrl1.fastq 2>/dev/null | samtools sort -o sr.bam - 2>/dev/null; samtools index sr.bam
echo "short-read spliced: $(samtools view -c -F 2308 sr.bam) mapped; with N: $(samtools view -F 2308 sr.bam | awk '$6 ~ /N/' | wc -l)"
minimap2 -ax splice:hq --secondary=no -t 8 $D/chrQ.fa $D/hifi/ctrl1.fastq 2>/dev/null | samtools sort -o lr.bam - 2>/dev/null; samtools index lr.bam
isoquant --reference reference.fa --genedb gencode.v45.annotation.gtf --bam lr.bam --data_type pacbio_ccs --output iq_noillu --threads 8 --prefix s > iq_noillu.log 2>&1; echo "no illumina rc=$?"
isoquant --reference reference.fa --genedb gencode.v45.annotation.gtf --bam lr.bam --illumina_bam sr.bam --data_type pacbio_ccs --output iq_illu --threads 8 --prefix s > iq_illu.log 2>&1; echo "with --illumina_bam rc=$?"
grep -a -i "illumina" iq_illu.log | head -5
for v in iq_noillu iq_illu; do echo "== $v"; asenv as-lr python $R/iq_novel_check.py $O/$v/s s; done
