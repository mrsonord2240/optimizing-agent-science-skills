suppressPackageStartupMessages(library(ATACseqQC))
bam <- 'F:/OpenScience/audit-envs/atac-seq/public-data/encode/GM12878_rep1_filtered.chr1_1-30000000.bam'
png('F:/OpenScience/audits/bio-atac-seq-atac-qc/audit-run/out/fragsize_replot.png', width=900, height=600)
fs <- fragSizeDist(bam, 'rep1')
dev.off()
cat('fragSizeDist returned class:', class(fs), 'n=', length(fs), '\n')
