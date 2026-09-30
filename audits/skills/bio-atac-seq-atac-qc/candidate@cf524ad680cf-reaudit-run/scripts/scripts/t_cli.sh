source /mnt/openscience/audits/bio-atac-seq-atac-qc/reaudit-run/scripts/env.sh; cd $O; mkdir -p cli; cd cli
U=$ATACDATA/encode/GM12878_rep1_unfiltered.chr1_1-30000000.bam; F=$ATACDATA/encode/GM12878_rep1_filtered.chr1_1-30000000.bam; F2=$ATACDATA/encode/GM12878_rep2_filtered.chr1_1-30000000.bam
echo "## mt fraction path on labeled SYNTHETIC planted_pe (chrM 600 recs of 1240 mapped; truth 0.4839)"
samtools idxstats ../planted_pe.bam | tee idx.txt | awk '$1=="chrM"{m=$3} {t+=$3} END{print "chrM",m,"total",t,"frac",m/t}'
echo "## preseq c_curve -P -s 1e5 (unfiltered, coordsorted)"; preseq c_curve -B -P -s 1e5 -o cc.tsv $U 2>&1 | tail -1; cat cc.tsv
echo "## preseq lc_extrap -P"; preseq lc_extrap -B -P -e 20000000 -s 1000000 -o lc.tsv $U 2>&1 | tail -1; sed -n '1,3p;$p' lc.tsv
echo "## flagstat/idxstats filtered"; samtools flagstat $F | sed -n 1,5p
echo "## Picard"; picard CollectInsertSizeMetrics I=$F O=isize.txt H=isize.pdf M=0.5 VALIDATION_STRINGENCY=SILENT 2>&1 | tail -1; grep -A1 '^MEDIAN_INSERT_SIZE' isize.txt | cut -f1-6
echo "## multiBamSummary/plotCorrelation"; multiBamSummary bins -bs 10000 -p 4 --bamfiles $F $F2 -o multi.npz --outRawCounts raw.tsv 2>&1 | tail -1
plotCorrelation -in multi.npz --corMethod spearman --whatToPlot heatmap --skipZeros -o spearman.png --outFileCorMatrix spearman.tsv 2>&1|tail -1; cat spearman.tsv
echo "## plotFingerprint"; plotFingerprint -p 4 -b $F $F2 --labels rep1 rep2 --skipZeros --numberOfSamples 50000 -o fingerprint.png --outQualityMetrics fp.txt 2>&1 | tail -1; cut -f1,2,3 fp.txt | head -4
echo "## multiqc"; cp isize.txt fp.txt . 2>/dev/null; samtools flagstat $F > rep1.flagstat.txt; multiqc . -o mqc -f -q 2>&1 | tail -1; cat mqc/multiqc_data/multiqc_sources.txt | cut -f1-3
