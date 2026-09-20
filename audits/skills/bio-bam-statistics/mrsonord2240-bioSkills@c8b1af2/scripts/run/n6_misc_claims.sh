#!/bin/bash
# NEW: remaining checkable claims not exercised before: the mosdepth command block, --quantize, mosdepth on CRAM (needs -f and .crai), `samtools coverage` overlap option, stats -r GC-depth wording,
# mpileup depth column vs D/N, unindexed idxstats, `depth -q` flag, Skill statements about --flag defaults.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; N=$R/data/new; cd $R/work; rm -rf mm; mkdir mm; cd mm
H=$AFDATA/human/test.paired_end.sorted.bam; cp $H input.bam; cp $H.bai input.bam.bai; printf 'chr22\t1951\t4617\n' > exome.bed; cp $AFDATA/human/genome.fasta ref.fa; cp $AFDATA/human/genome.fasta.fai ref.fa.fai
echo "=== SKILL mosdepth block (line-by-line, placeholders filled)"
sed -n '2,5p' $R/blocks/020_bash.sh | sed 's/-t 4/-t 2/' | sed 's#input.cram#c.cram#' > mdblock.sh; cat mdblock.sh | cut -c1-120
cp $N/own_ctg.cram c.cram; cp $N/own_ctg.cram.crai c.cram.crai; cp $N/own_ctg.fa ref.fa.own; 
mosdepth -t 2 sample input.bam && tail -1 sample.mosdepth.summary.txt | cut -f1-4
mosdepth -t 2 --by exome.bed --thresholds 1,10,20,30,100 --no-per-base sample2 input.bam && zcat sample2.thresholds.bed.gz | tail -1
mosdepth -t 2 --quantize 0:1:10:100: sample3 input.bam && zcat sample3.quantized.bed.gz | head -5 | tr '\t' ' '
echo "--- mosdepth -f ref on CRAM with .crai / without"; mosdepth -t 2 -f ref.fa.own cm c.cram && tail -1 cm.mosdepth.summary.txt | cut -f1-4
cp $N/own_ctg_noidx.cram n.cram; mosdepth -t 2 -f ref.fa.own cn n.cram 2>&1 | tail -1
echo "=== truth quantize: chr22 covered positions 1181 of 40001 -> bands: expect 0:1 (zero), 1:10 ... (count rows)"; zcat sample3.quantized.bed.gz | awk '{n[$4]++; l[$4]+=$3-$2} END{for(k in n) print k, n[k], l[k]}'
echo "=== samtools coverage: any overlap option? (Skill: none)"; samtools coverage --help 2>&1 | grep -ciE 'overlap'; samtools coverage --help 2>&1 | grep -E -- '^ +-[a-zA-Z]' | cut -c1-70 | head -14
echo "=== samtools stats -r wording: 'GC-depth'; GCD row count with/without -r at --GC-depth 1000"
samtools stats --help 2>&1 | grep -E -- '-r, --ref-seq|--GC-depth' | cut -c1-140
echo -n "without -r: "; samtools stats --GC-depth 1000 input.bam | grep -c '^GCD'; echo -n "with -r:    "; samtools stats --GC-depth 1000 -r ref.fa input.bam | grep -c '^GCD'
echo -n "error rate without -r: "; samtools stats input.bam | grep -E '^SN\s+error rate' | cut -f3; echo -n "error rate with -r: "; samtools stats -r ref.fa input.bam | grep -E '^SN\s+error rate' | cut -f3
echo "=== depth -q meaning and mosdepth 'does not honor base quality'"; samtools depth --help 2>&1 | grep -E -- ' -q,| -Q,' | head -2
echo "=== plot-bamstats needs perl-uri claim: conda list"; micromamba list -n alignment-files 2>/dev/null | grep -E 'perl-uri|samtools |mosdepth|gnuplot' | awk '{print $1, $2}'
echo "=== 'samtools view -c -F 2308 -q 30' idiom on own_ctg: primary mapped incl. QC-fail and dup (2308 = 4+256+2048): truth 1092 (1085 passed + 7 qc-fail primary mapped)"
samtools view -c -F 2308 $N/own_ctg.bam; samtools view -c -F 2308 -q 30 $N/own_ctg.bam
