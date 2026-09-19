.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(EnsDb.Hsapiens.v86)
  library(GenomicRanges)
  library(Rsamtools)
})

set.seed(42)

out_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data'
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

edb <- EnsDb.Hsapiens.v86
genes <- genes(edb, filter = SymbolFilter(c('CD3D','MS4A1','CD14','GAPDH')))
genes <- genes[grepl('^ENSG', names(genes))]        # drop LRG duplicate entries
genes <- keepStandardChromosomes(genes, pruning.mode = 'coarse')
genes <- genes[!duplicated(genes$symbol)]
seqlevelsStyle(genes) <- 'UCSC'                       # match the SKILL.md pattern (chrN, matches noise peaks below)
print(as.data.frame(genes)[, c('seqnames','start','end','symbol')])

# Build a "gene window" (gene body + 2kb upstream, matching Signac's GeneActivity default) for each marker
strand_sign <- as.character(strand(genes))
win_start <- ifelse(strand_sign == '-', start(genes), pmax(1, start(genes) - 2000))
win_end   <- ifelse(strand_sign == '-', end(genes) + 2000, end(genes))
gene_windows <- GRanges(seqnames(genes), IRanges(win_start, win_end), symbol = genes$symbol)
names(gene_windows) <- genes$symbol
print(gene_windows)

# 500bp tiled peaks across each marker gene window (+/- 1kb padding), plus noise peaks elsewhere on chr1/chr11/chr5
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

# Noise peaks: random 500bp windows on chr1, away from marker loci, for background/depth signal
set.seed(123)
noise_starts <- sample(seq(1e6, 5e7, by = 5000), 150)
noise_peaks <- GRanges('chr1', IRanges(noise_starts, noise_starts + 499))
noise_peaks$marker <- 'noise'

all_peaks <- sort(c(marker_peaks, noise_peaks))
all_peaks <- all_peaks[!duplicated(all_peaks)]
cat('Total peaks:', length(all_peaks), '\n')
cat('Peaks per marker:\n')
print(table(all_peaks$marker))

saveRDS(all_peaks, file.path(out_dir, 'peaks.rds'))
saveRDS(gene_windows, file.path(out_dir, 'gene_windows.rds'))

# ---- Simulate cells: 2 cell types x 2 depth strata (depth orthogonal to cell type) ----
n_per_group <- 75
cell_types <- rep(c('Tcell','Bcell'), each = 2 * n_per_group)
depth_strata <- rep(rep(c('high','low'), each = n_per_group), 2)
barcodes <- paste0('cell', seq_along(cell_types), '-1')
cell_meta <- data.frame(barcode = barcodes, cell_type = cell_types, depth_strata = depth_strata,
                         stringsAsFactors = FALSE)

marker_of_type <- c(Tcell = 'CD3D', Bcell = 'MS4A1')
depth_mult <- c(high = 3.0, low = 1.0)

frag_list <- vector('list', nrow(cell_meta))
for (i in seq_len(nrow(cell_meta))) {
  ct <- cell_meta$cell_type[i]
  ds <- cell_meta$depth_strata[i]
  bc <- cell_meta$barcode[i]
  mult <- depth_mult[[ds]]

  # Accessible peaks for this cell: its type-specific marker + housekeeping GAPDH, both boosted;
  # other markers get a low leak rate; noise peaks get uniform low background (scaled by depth)
  n_frag_marker   <- rpois(1, 40 * mult)   # fragments at the cell-type marker
  n_frag_gapdh    <- rpois(1, 35 * mult)   # housekeeping, accessible in all cells
  n_frag_offmark  <- rpois(1, 3  * mult)   # leak into the other cell type's marker
  n_frag_noise    <- rpois(1, 60 * mult)   # background across noise peaks (drives depth in LSI)

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
  other_ct <- setdiff(names(marker_of_type), ct)
  off_marker_peaks <- all_peaks[all_peaks$marker == marker_of_type[[other_ct]]]
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
cat('Fragments per cell summary:\n')
print(summary(table(frags$barcode)))

saveRDS(cell_meta, file.path(out_dir, 'cell_meta.rds'))

# ---- Write fragments.tsv, bgzip + tabix index via Rsamtools (no external CLI needed) ----
frag_path <- file.path(out_dir, 'fragments.tsv')
write.table(frags, frag_path, sep = '\t', quote = FALSE, row.names = FALSE, col.names = FALSE)
bgz_path <- Rsamtools::bgzip(frag_path, overwrite = TRUE)
idx <- Rsamtools::indexTabix(bgz_path, format = 'bed')
cat('Fragments written:', bgz_path, '\n')
cat('Tabix index:', idx, '\n')
cat('STAGE 1 DONE\n')
