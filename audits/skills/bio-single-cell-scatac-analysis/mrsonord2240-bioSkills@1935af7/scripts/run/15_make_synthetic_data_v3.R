.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(EnsDb.Hsapiens.v86)
  library(GenomicRanges)
  library(Rsamtools)
})

# 4th independent re-audit -- deliberately different from every dataset used so far:
#   - pre-fix re-audit used seed=42/123/7 (per its own comments) with 2 cell types
#   - the T3-veto-finding re-audit used seed=99 with 3 cell types (Tcell/Bcell/Monocyte)
#   - the fixer's own verification reused that re-audit's obj_qc.rds directly (no new data)
# This run uses a fresh seed and a 4th cell type (NK, marker gene KLRB1) neither prior run had.
set.seed(20260919)

out_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit4_20260919'
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

edb <- EnsDb.Hsapiens.v86
genes <- genes(edb, filter = SymbolFilter(c('CD3D', 'MS4A1', 'CD14', 'KLRB1', 'GAPDH')))
genes <- genes[grepl('^ENSG', names(genes))]
genes <- keepStandardChromosomes(genes, pruning.mode = 'coarse')
genes <- genes[!duplicated(genes$symbol)]
seqlevelsStyle(genes) <- 'UCSC'
print(as.data.frame(genes)[, c('seqnames', 'start', 'end', 'symbol')])

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

noise_starts <- sample(seq(1e6, 5e7, by = 5000), 260)
noise_peaks <- GRanges('chr1', IRanges(noise_starts, noise_starts + 499))
noise_peaks$marker <- 'noise'

all_peaks <- sort(c(marker_peaks, noise_peaks))
all_peaks <- all_peaks[!duplicated(all_peaks)]
cat('Total peaks:', length(all_peaks), '\n')
print(table(all_peaks$marker))

saveRDS(all_peaks, file.path(out_dir, 'peaks.rds'))
saveRDS(gene_windows, file.path(out_dir, 'gene_windows.rds'))

# 4 cell types x 2 depth strata, yet another proportion/ratio mix
n_t <- 55; n_b <- 45; n_m <- 50; n_nk <- 40
cell_types <- c(rep('Tcell', n_t), rep('Bcell', n_b), rep('Monocyte', n_m), rep('NK', n_nk))
mk_strata <- function(n) rep(c('high', 'low'), c(round(n * 0.5), n - round(n * 0.5)))
depth_strata <- c(mk_strata(n_t), mk_strata(n_b), mk_strata(n_m), mk_strata(n_nk))
barcodes <- paste0('cellv3_', seq_along(cell_types), '-1')
cell_meta <- data.frame(barcode = barcodes, cell_type = cell_types, depth_strata = depth_strata,
                         stringsAsFactors = FALSE)

marker_of_type <- c(Tcell = 'CD3D', Bcell = 'MS4A1', Monocyte = 'CD14', NK = 'KLRB1')
depth_mult <- c(high = 3.5, low = 1.5)

frag_list <- vector('list', nrow(cell_meta))
for (i in seq_len(nrow(cell_meta))) {
  ct <- cell_meta$cell_type[i]
  ds <- cell_meta$depth_strata[i]
  bc <- cell_meta$barcode[i]
  mult <- depth_mult[[ds]]

  n_frag_marker  <- rpois(1, 42 * mult)
  n_frag_gapdh   <- rpois(1, 28 * mult)
  n_frag_offmark <- rpois(1, 2  * mult)
  n_frag_noise   <- rpois(1, 50 * mult)

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
cat('STAGE 1 (v3, 4th independent dataset) DONE\n')
