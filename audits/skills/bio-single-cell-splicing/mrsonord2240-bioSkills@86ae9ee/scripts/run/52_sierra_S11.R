# INPUT 6b: Sierra. SKILL.md block S11 run LITERALLY (source) on the package's bundled real 10x BAM (staged by 51_*), with cell_identities defined first (random ctrl/trt split of the whitelist).
# Then (a) content checks, (b) independent pysam-free check: CountPeaks totals vs a per-peak count from the BAM via Rsamtools if available, (c) a planted APA shift built by binomial thinning of the peak matrix, (d) the block's DUTest result on the null split.
setwd('F:/OpenScience/audits/bio-single-cell-splicing/run/out/in6_sierra'); options(warn = 1)
suppressMessages({library(Sierra); library(Matrix)})
bc <- readLines('barcodes.tsv'); set.seed(11); cell_identities <- setNames(sample(c('ctrl', 'trt'), length(bc), replace = TRUE), bc)
r <- tryCatch({ source('F:/OpenScience/audits/bio-single-cell-splicing/run/blocks/S11_r.R', echo = FALSE); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('block S11 status:', r, '\n'); if (r != 'OK') quit(status = 1)
pk <- read.table('peaks.txt', header = TRUE, sep = '\t', stringsAsFactors = FALSE); cat('peaks.txt rows', nrow(pk), ' cols:', paste(colnames(pk)[1:min(6, ncol(pk))], collapse = ','), '\n')
cat('counts class', class(counts)[1], 'dim', dim(counts), ' total UMIs', sum(counts), '\n'); stopifnot(nrow(counts) == nrow(pk), sum(counts) > 1000)
cat('peak.annotations dim', dim(peak.annotations), ' cols:', paste(colnames(peak.annotations), collapse = ','), '\n')
cat('NULL split DUTest: class', class(apa_results)[1], ' rows', nrow(apa_results), ' cols:', paste(colnames(apa_results), collapse = ','), ' padj<0.05:', sum(apa_results$padj < 0.05, na.rm = TRUE), '\n')
# (b) second method for CountPeaks: distinct (CB,UB) per peak from the BAM with Rsamtools, if installed
if (requireNamespace('Rsamtools', quietly = TRUE)) {
  suppressMessages(library(Rsamtools)); bam <- 'possorted_genome_bam.bam'
  top <- order(rowSums(counts), decreasing = TRUE)[1:5]
  pa <- peak.annotations[rownames(counts), ]
  for (i in top) { p <- pa[i, ]; gr <- GenomicRanges::GRanges(as.character(p$seqnames), IRanges::IRanges(p$start, p$end))
    x <- scanBam(bam, param = ScanBamParam(which = gr, what = c('pos', 'strand', 'cigar'), tag = c('CB', 'UB')))[[1]]
    ok <- !is.na(x$tag$CB) & !is.na(x$tag$UB) & x$tag$CB %in% bc; cat(sprintf('peak %-28s Sierra UMIs %5d ; Rsamtools distinct (CB,UB) among reads overlapping the window %5d\n', rownames(counts)[i], rowSums(counts)[i], length(unique(paste(x$tag$CB[ok], x$tag$UB[ok]))))) }
} else cat('Rsamtools not installed: second-method check skipped\n')
# (c) planted APA shift: pick genes with >= 2 peaks; in 'trt' cells thin the first peak of 8 genes to 30% (binomial), keep the rest; then the block's NewPeakSCE + DUTest lines
gene_of <- peak.annotations[rownames(counts), 'gene_id']; g2 <- names(which(table(gene_of) >= 2)); cat('genes with >=2 peaks:', length(g2), '\n')
cnt <- counts; trt <- names(cell_identities)[cell_identities == 'trt']; trt <- trt[trt %in% colnames(cnt)]; sel <- head(g2[order(sapply(g2, function(g) -sum(cnt[which(gene_of == g), ])))], 8)
for (g in sel) { i <- which(gene_of == g)[1]; cnt[i, trt] <- rbinom(length(trt), as.integer(cnt[i, trt]), 0.3) }
cnt <- as(cnt, 'CsparseMatrix'); sce <- NewPeakSCE(peak.data = cnt, annot.info = peak.annotations, cell.idents = cell_identities, min.cells = 0, min.peaks = 0)
res <- DUTest(sce, population.1 = 'ctrl', population.2 = 'trt'); sig <- unique(res$gene_name[res$padj < 0.05])
cat('planted shift (8 genes, first peak thinned to 30% in trt): DUTest rows', nrow(res), ' genes called', length(sig), ' planted recovered', sum(sel %in% sig), '/ 8 ; other genes called', sum(!(sig %in% sel)), 'of', length(unique(res$gene_name)) - 8, 'unchanged\n')
cat('planted genes:', paste(sel, collapse = ','), '\n')
