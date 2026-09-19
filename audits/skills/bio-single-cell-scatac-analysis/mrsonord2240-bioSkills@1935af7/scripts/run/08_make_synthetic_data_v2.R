.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(EnsDb.Hsapiens.v86)
  library(GenomicRanges)
  library(Rsamtools)
})

set.seed(99)  # independent of the original audit's seed 42/123/7

out_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit_v2_20260919'
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

edb <- EnsDb.Hsapiens.v86
genes <- genes(edb, filter = SymbolFilter(c('CD3D','MS4A1','CD14','GAPDH')))
genes <- genes[grepl('^ENSG', names(genes))]
genes <- keepStandardChromosomes(genes, pruning.mode = 'coarse')
genes <- genes[!duplicated(genes$symbol)]
seqlevelsStyle(genes) <- 'UCSC'
print(as.data.frame(genes)[, c('seqnames','start','end','symbol')])

strand_sign <- as.character(strand(genes))
win_start <- ifelse(strand_sign == '-', start(genes), pmax(1, start(genes) - 2000))
win_end   <- ifelse(strand_sign == '-', end(genes) + 2000, end(genes))
gene_windows <- GRanges(seqnames(genes), IRanges(win_start, win_end), symbol = genes$symbol)
names(gene_windows) <- genes$symbol

tile_peaks <- function(gr, width = 500) {
  s <- seq(start(gr) - 1000, end(gr) + 1000, by = width)
  GRanges(seqnames(gr), IRanges(s, s + width - 1))
}
marker_peak_list <- lapply(seq_along(gene_windows), function(i) {
  gr <- tile_peaks(gene_windows[i], 500)
  gr$marker <- names(gene_windows)[i]
  gr
})
marker_peaks <- do.call(c, marker_peak_list)

noise_starts <- sample(seq(1e6, 5e7, by = 5000), 200)
noise_peaks <- GRanges('chr1', IRanges(noise_starts, noise_starts + 499))
noise_peaks$marker <- 'noise'

all_peaks <- sort(c(marker_peaks, noise_peaks))
all_peaks <- all_peaks[!duplicated(all_peaks)]
cat('Total peaks:', length(all_peaks), '\n')
print(table(all_peaks$marker))

saveRDS(all_peaks, file.path(out_dir, 'peaks.rds'))
saveRDS(gene_windows, file.path(out_dir, 'gene_windows.rds'))

# ---- 3 cell types (Tcell/Bcell/Monocyte) x 2 depth strata (depth orthogonal to type), different
# proportions and depth ratio than the original audit's 2-type/2-strata design ----
n_t <- 60; n_b <- 60; n_m <- 60
cell_types <- c(rep('Tcell', n_t), rep('Bcell', n_b), rep('Monocyte', n_m))
depth_strata <- c(rep(c('high','low'), c(round(n_t*0.4), n_t - round(n_t*0.4))),
                   rep(c('high','low'), c(round(n_b*0.4), n_b - round(n_b*0.4))),
                   rep(c('high','low'), c(round(n_m*0.4), n_m - round(n_m*0.4))))
barcodes <- paste0('cellv2_', seq_along(cell_types), '-1')
cell_meta <- data.frame(barcode = barcodes, cell_type = cell_types, depth_strata = depth_strata,
                         stringsAsFactors = FALSE)

marker_of_type <- c(Tcell = 'CD3D', Bcell = 'MS4A1', Monocyte = 'CD14')
depth_mult <- c(high = 4.0, low = 1.2)   # different ratio than the original (3.0/1.0)

frag_list <- vector('list', nrow(cell_meta))
for (i in seq_len(nrow(cell_meta))) {
  ct <- cell_meta$cell_type[i]
  ds <- cell_meta$depth_strata[i]
  bc <- cell_meta$barcode[i]
  mult <- depth_mult[[ds]]

  n_frag_marker  <- rpois(1, 45 * mult)
  n_frag_gapdh   <- rpois(1, 30 * mult)
  n_frag_offmark <- rpois(1, 2  * mult)
  n_frag_noise   <- rpois(1, 55 * mult)

  sample_frags_from_peaks <- function(peak_set, n) {
    if (n == 0 || length(peak_set) == 0) return(NULL)
    idx <- sample(length(peak_set), n, replace = TRUE)
    p <- peak_set[idx]
    w <- width(p)
    frag_len <- pmin(w - 20, pmax(50, round(rnorm(n, 200, 40))))
    frag_start <- start(p) + sample(0:10, n, replace = TRUE)
    frag_end <- frag_start + frag_len
    data.frame(chrom = as.character(seqnames(p)), start = frag_start, end = frag_end,
               barcode = bc, count = 1, stringsAsFactors = FALSE)
  }

  own_marker_peaks <- all_peaks[all_peaks$marker == marker_of_type[[ct]]]
  other_types <- setdiff(names(marker_of_type), ct)
  off_marker_peaks <- all_peaks[all_peaks$marker %in% marker_of_type[other_types]]
  gapdh_peaks <- all_peaks[all_peaks$marker == 'GAPDH']
  noise_peaks_only <- all_peaks[all_peaks$marker == 'noise']

  parts <- list(
    sample_frags_from_peaks(own_marker_peaks, n_frag_marker),
    sample_frags_from_peaks(gapdh_peaks, n_frag_gapdh),
    sample_frags_from_peaks(off_marker_peaks, n_frag_offmark),
    sample_frags_from_peaks(noise_peaks_only, n_frag_noise)
  )
  frag_list[[i]] <- do.call(rbind, parts)
}
frags <- do.call(rbind, frag_list)
frags <- frags[order(frags$chrom, frags$start), ]
cat('Total synthetic fragments:', nrow(frags), '\n')
print(summary(table(frags$barcode)))

saveRDS(cell_meta, file.path(out_dir, 'cell_meta.rds'))

frag_path <- file.path(out_dir, 'fragments.tsv')
write.table(frags, frag_path, sep = '\t', quote = FALSE, row.names = FALSE, col.names = FALSE)
bgz_path <- Rsamtools::bgzip(frag_path, overwrite = TRUE)
idx <- Rsamtools::indexTabix(bgz_path, format = 'bed')
cat('Fragments written:', bgz_path, '\n')
cat('Tabix index:', idx, '\n')
cat('STAGE 1 (v2, independent seed/design) DONE\n')
