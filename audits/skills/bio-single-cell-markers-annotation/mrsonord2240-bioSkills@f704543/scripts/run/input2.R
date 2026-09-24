# Input 2 (Variant A) - bio-single-cell-markers-annotation
# Seurat marker detection as SKILL.md:79-92, and the three Seurat rows of the
# "Defaults that bite" table checked against the installed Seurat 5.5.0.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(dplyr); library(presto)})
cat('Seurat', as.character(packageVersion('Seurat')), '| presto',
    as.character(packageVersion('presto')), '\n')

cat('\n--- "Defaults that bite", Seurat rows ---\n')
f <- formals(Seurat:::FindMarkers.default)
cat('  FindMarkers logfc.threshold default:', deparse(f$logfc.threshold),
    ' (Skill says 0.1 in v5, folklore 0.25)\n')
cat('  FindMarkers min.pct default        :', deparse(f$min.pct),
    ' (Skill says 0.01 in v5, folklore 0.1)\n')
cat('  test.use default                   :', deparse(f$test.use), '\n')
cat('  presto installed (so wilcox is fast):', requireNamespace('presto', quietly = TRUE), '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True','TRUE',TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True','TRUE',TRUE)
rownames(tc) <- tc$cell_id
mats <- list()
for (s in paste0('S', 1:8)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m)); mats[[s]] <- m
}
cm <- do.call(cbind, mats)
cm <- cm[, !tc[colnames(cm),'true_doublet'] & !tc[colnames(cm),'true_low_quality']]
so <- CreateSeuratObject(cm, min.cells = 3, min.features = 200)
so$true_cell_type <- tc[colnames(so), 'true_cell_type']
set.seed(20260916)
so <- NormalizeData(so, verbose = FALSE); so <- FindVariableFeatures(so, verbose = FALSE)
so <- ScaleData(so, verbose = FALSE); so <- RunPCA(so, npcs = 50, verbose = FALSE)
so <- FindNeighbors(so, dims = 1:30, verbose = FALSE)
so <- FindClusters(so, resolution = 0.3, verbose = FALSE)
cat('\n', ncol(so), 'cells,', length(unique(Idents(so))), 'clusters\n')

t0 <- Sys.time()
all_markers <- FindAllMarkers(so, only.pos = TRUE, logfc.threshold = 0.25, min.pct = 0.1,
                              verbose = FALSE)
cat('FindAllMarkers (logfc 0.25 / min.pct 0.1) took',
    round(as.numeric(difftime(Sys.time(), t0, units='secs')), 1), 's ->', nrow(all_markers), 'rows\n')
t0 <- Sys.time()
permissive <- FindAllMarkers(so, only.pos = TRUE, verbose = FALSE)
cat('FindAllMarkers at the v5 DEFAULTS took',
    round(as.numeric(difftime(Sys.time(), t0, units='secs')), 1), 's ->', nrow(permissive), 'rows\n')
cat('  -> the Skill says the v5 defaults are "permissive, returns more hits":',
    nrow(permissive) > nrow(all_markers), sprintf('(%.1fx)\n', nrow(permissive)/nrow(all_markers)))

specific <- all_markers %>%
  filter(p_val_adj < 0.05, avg_log2FC > 1, (pct.1 - pct.2) > 0.2) %>%
  group_by(cluster) %>% slice_max(n = 10, order_by = avg_log2FC)
cat('after the Skill\'s specificity filter:', nrow(specific), 'rows,',
    length(unique(specific$cluster)), 'of', length(unique(Idents(so))), 'clusters retain markers\n')
print(as.data.frame(specific %>% group_by(cluster) %>% slice_max(n = 3, order_by = avg_log2FC) %>%
      select(cluster, gene, avg_log2FC, pct.1, pct.2, p_val_adj)), row.names = FALSE)

cat('\n--- cell-cycle scoring (SKILL.md:122) ---\n')
cc <- try({
  s2 <- CellCycleScoring(so, s.features = cc.genes.updated.2019$s.genes,
                         g2m.features = cc.genes.updated.2019$g2m.genes)
  table(s2$Phase)
}, silent = TRUE)
if (inherits(cc, 'try-error')) cat('  FAILED:', as.character(cc)) else print(cc)
cat('  cc.genes.updated.2019 available with both lists:',
    all(c('s.genes','g2m.genes') %in% names(cc.genes.updated.2019)), '\n')

cat('\n--- AddModuleScore control-bin default (SKILL.md:109 says Seurat uses 24) ---\n')
cat('  AddModuleScore nbin default:', deparse(formals(AddModuleScore)$nbin),
    '| ctrl default:', deparse(formals(AddModuleScore)$ctrl), '\n')
cat('DONE\n')
