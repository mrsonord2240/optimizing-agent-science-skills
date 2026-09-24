# Input 2 (Variant A) - bio-single-cell-preprocessing
# SoupX ambient-RNA removal exactly as SKILL.md:123-128 prescribes, on Cell Ranger v3
# raw+filtered output. Data: SYNTHETIC 8-sample PBMC set (known per-sample ambient rho)
# plus the real public 10x PBMC 1k v3 run for a real-soup sanity check.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(SoupX); library(Seurat); library(Matrix)})
cat('SoupX', as.character(packageVersion('SoupX')), '| Seurat', as.character(packageVersion('Seurat')), '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
truth_rho <- c(S1=0.0492, S2=NA, S3=NA, S4=NA, S5=NA, S6=NA, S7=NA, S8=NA)  # filled from truth_cells.csv below
tc <- read.csv(file.path(D, 'truth_cells.csv'))
truth_rho <- tapply(tc$sample_ambient_rho, tc$sample, function(x) x[1])
cat('TRUE ambient rho per sample (synthetic ground truth):\n'); print(round(truth_rho, 4))

## ---- Step 1: the SKILL.md snippet, run verbatim ----
cat('\n=== SKILL.md:123-128 verbatim on S1 ===\n')
res <- try({
  sc <- load10X(file.path(D, 'S1/outs'))
  sc <- autoEstCont(sc)
  counts_adj <- adjustCounts(sc, roundToInt = TRUE)
  cat('rho =', mean(sc$metaData$rho), '\n')
}, silent = TRUE)
if (inherits(res, 'try-error')) cat('VERBATIM SNIPPET FAILED:\n', as.character(res), '\n')

## ---- Step 2: adapted route (agent supplies the clustering autoEstCont needs) ----
cat('\n=== Adapted: build SoupChannel, cluster with Seurat, then autoEstCont ===\n')
est <- setNames(rep(NA_real_, 8), paste0('S', 1:8))
for (s in paste0('S', 1:8)) {
  tod <- Read10X(file.path(D, s, 'outs/raw_feature_bc_matrix'))
  toc <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  sc <- SoupChannel(tod, toc)
  so <- CreateSeuratObject(toc)
  so <- NormalizeData(so, verbose = FALSE)
  so <- FindVariableFeatures(so, verbose = FALSE)
  so <- ScaleData(so, verbose = FALSE)
  so <- RunPCA(so, npcs = 30, verbose = FALSE)
  so <- FindNeighbors(so, dims = 1:20, verbose = FALSE)
  so <- FindClusters(so, resolution = 0.8, verbose = FALSE)
  sc <- setClusters(sc, setNames(as.character(Idents(so)), colnames(so)))
  sc <- autoEstCont(sc, doPlot = FALSE, forceAccept = TRUE)
  est[s] <- mean(sc$metaData$rho)
  adj <- adjustCounts(sc, roundToInt = TRUE)
  if (s == 'S1') {
    # SKILL.md: "validate that a known-specific marker survives"
    hb <- intersect(c('HBB', 'HBA1', 'HBA2'), rownames(toc))
    cd3 <- intersect(c('CD3D', 'CD3E'), rownames(toc))
    cat('  S1 HBB soup gene: pre =', sum(toc[hb, ]), ' post =', sum(adj[hb, ]), '\n')
    cat('  S1 CD3D/E lineage marker: pre =', sum(toc[cd3, ]), ' post =', sum(adj[cd3, ]),
        ' cells expressing pre/post =', sum(colSums(toc[cd3, , drop = FALSE]) > 0), '/',
        sum(colSums(adj[cd3, , drop = FALSE]) > 0), '\n')
    cat('  total counts removed:', round(100 * (1 - sum(adj) / sum(toc)), 2), '%\n')
  }
}
cmp <- data.frame(sample = names(est), estimated_rho = round(est, 4),
                  true_rho = round(as.numeric(truth_rho[names(est)]), 4))
cmp$abs_err <- round(abs(cmp$estimated_rho - cmp$true_rho), 4)
print(cmp)
cat('mean |error| =', round(mean(cmp$abs_err), 4), '\n')

## ---- Step 3: the same snippet on REAL 10x PBMC 1k v3 (genuine soup) ----
cat('\n=== REAL 10x PBMC 1k v3 (public data) ===\n')
P <- 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data'
tod <- Read10X_h5(file.path(P, 'pbmc_1k_v3_raw_feature_bc_matrix.h5'))
toc <- Read10X_h5(file.path(P, 'pbmc_1k_v3_filtered_feature_bc_matrix.h5'))
sc <- SoupChannel(tod, toc)
so <- CreateSeuratObject(toc)
so <- NormalizeData(so, verbose = FALSE); so <- FindVariableFeatures(so, verbose = FALSE)
so <- ScaleData(so, verbose = FALSE); so <- RunPCA(so, npcs = 30, verbose = FALSE)
so <- FindNeighbors(so, dims = 1:20, verbose = FALSE); so <- FindClusters(so, resolution = 0.8, verbose = FALSE)
sc <- setClusters(sc, setNames(as.character(Idents(so)), colnames(so)))
sc <- autoEstCont(sc, doPlot = FALSE)
cat('real PBMC 1k rho =', round(mean(sc$metaData$rho), 4), '\n')
adj <- adjustCounts(sc, roundToInt = TRUE)
cat('counts removed:', round(100 * (1 - sum(adj) / sum(toc)), 2), '%\n')
cat('DONE\n')
