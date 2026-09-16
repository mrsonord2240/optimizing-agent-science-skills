# Input 4 (Variant B) - bio-single-cell-batch-integration
# Seurat v5 layer-based integration exactly as SKILL.md:126-141, plus the Skill's claim at
# SKILL.md:143 that methods are passed as BARE SYMBOLS (CCAIntegration, RPCAIntegration,
# HarmonyIntegration, FastMNNIntegration, scVIIntegration). SYNTHETIC 8-sample PBMC set.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(SeuratObject)})
cat('Seurat', as.character(packageVersion('Seurat')), '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', TRUE)
rownames(tc) <- tc$cell_id
ss <- read.csv(file.path(D, 'sample_sheet.csv')); rownames(ss) <- ss$sample

mats <- list()
for (s in paste0('S', 1:8)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m)); mats[[s]] <- m
}
counts <- do.call(cbind, mats)
keep <- !tc[colnames(counts), 'true_doublet'] & !tc[colnames(counts), 'true_low_quality']
counts <- counts[, keep]
merged <- CreateSeuratObject(counts, min.cells = 3, min.features = 200)
merged$sample <- sub('_.*', '', colnames(merged))
merged$batch <- ss[merged$sample, 'batch']
truth <- tc[colnames(merged), 'true_cell_type']
cat(ncol(merged), 'cells;', length(unique(merged$batch)), 'batches\n')

ari <- function(x, y) {
  t <- table(x, y); n <- sum(t)
  s <- sum(choose(t, 2)); a <- sum(choose(rowSums(t), 2)); b <- sum(choose(colSums(t), 2))
  e <- a * b / choose(n, 2); (s - e) / ((a + b) / 2 - e)
}

set.seed(20260916)
merged[['RNA']] <- split(merged[['RNA']], f = merged$batch)
cat('layers after split:', paste(Layers(merged[['RNA']]), collapse = ', '), '\n')
merged <- NormalizeData(merged, verbose = FALSE)
merged <- FindVariableFeatures(merged, verbose = FALSE)
merged <- ScaleData(merged, verbose = FALSE)
merged <- RunPCA(merged, npcs = 50, verbose = FALSE)

# uncorrected baseline
u <- FindNeighbors(merged, reduction = 'pca', dims = 1:30, verbose = FALSE)
u <- FindClusters(u, resolution = 0.5, verbose = FALSE)
cat(sprintf('uncorrected: %d clusters, ARI vs true type %.3f\n',
            length(unique(Idents(u))), ari(as.character(Idents(u)), truth)))

# --- bare-symbol methods, exactly as SKILL.md:143 lists them ---
for (nm in c('CCAIntegration', 'RPCAIntegration', 'HarmonyIntegration')) {
  f <- try(get(nm), silent = TRUE)
  cat(sprintf('  symbol %-20s exists: %s\n', nm, !inherits(f, 'try-error')))
}
for (nm in c('FastMNNIntegration', 'scVIIntegration')) {
  f <- try(get(nm), silent = TRUE)
  cat(sprintf('  symbol %-20s exists: %s %s\n', nm, !inherits(f, 'try-error'),
              if (inherits(f, 'try-error')) '(SeuratWrappers-only; not installed here)' else ''))
}

res <- list()
for (m in c('RPCAIntegration', 'CCAIntegration', 'HarmonyIntegration')) {
  t0 <- Sys.time()
  r <- try({
    o <- IntegrateLayers(merged, method = get(m), orig.reduction = 'pca',
                         new.reduction = paste0('int.', m), verbose = FALSE)
    o <- JoinLayers(o)
    o <- FindNeighbors(o, reduction = paste0('int.', m), dims = 1:30, verbose = FALSE)
    o <- FindClusters(o, resolution = 0.5, verbose = FALSE)
    o
  }, silent = TRUE)
  dt <- round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1)
  if (inherits(r, 'try-error')) {
    cat(sprintf('%s FAILED after %ss: %s', m, dt, as.character(r)))
  } else {
    cat(sprintf('%-20s %5ss: %d clusters, ARI vs true type %.3f\n', m, dt,
                length(unique(Idents(r))), ari(as.character(Idents(r)), truth)))
    res[[m]] <- r
  }
}
cat('DONE\n')
