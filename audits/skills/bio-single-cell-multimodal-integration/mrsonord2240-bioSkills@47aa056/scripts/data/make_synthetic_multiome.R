# Synthetic 10x Multiome (RNA + ATAC, same cells) generator, reusing the 3-population
# structure from the CITE-seq synthetic set (RNA reused) and adding a synthetic ATAC
# peak matrix with cluster-specific accessible peaks plus a depth confound so DepthCor
# has something real to detect.
set.seed(7)
d <- readRDS("data/synthetic_cite_seq.rds")
n_cells <- ncol(d$rna_cells)
truth <- d$truth

n_peaks <- 800
peak_names <- paste0("chr1-", seq(1, n_peaks * 1000, by = 1000), "-", seq(500, n_peaks * 1000, by = 1000))
peak_markers <- list(Tcell = paste0("chr1-", seq(1, 3000, by = 1000), "-", seq(500, 3000, by = 1000)),
                      Bcell = peak_names[101:103],
                      Mono  = peak_names[201:203])

# per-cell depth factor (varies 0.3x-3x) -- this is what should show up as a depth-correlated
# LSI component
depth_factor <- runif(n_cells, 0.3, 3)

atac <- matrix(rpois(n_peaks * n_cells, lambda = matrix(rep(0.3 * depth_factor, each = n_peaks), nrow = n_peaks)),
                nrow = n_peaks, ncol = n_cells)
rownames(atac) <- peak_names
colnames(atac) <- colnames(d$rna_cells)
for (ct in names(peak_markers)) {
  idx <- which(truth == ct)
  for (p in peak_markers[[ct]]) {
    atac[p, idx] <- atac[p, idx] + rpois(length(idx), lambda = 8 * depth_factor[idx])
  }
}

saveRDS(list(rna_cells = d$rna_cells, atac_cells = atac, truth = truth, depth_factor = depth_factor),
        "data/synthetic_multiome.rds")
cat("Synthetic multiome written:", nrow(atac), "peaks x", ncol(atac), "cells\n")
