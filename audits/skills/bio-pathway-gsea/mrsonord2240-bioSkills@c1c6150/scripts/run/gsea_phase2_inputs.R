# Phase 2 regression inputs for bio-pathway-gsea at c1c6150.
# Usage: Rscript gsea_phase2_inputs.R <1..7>

input <- as.integer(commandArgs(trailingOnly = TRUE)[1])
stopifnot(!is.na(input), input %in% 1:7)

if (input == 1L) {
  source('/mnt/openscience/wt/pathway-gsea/pathway-analysis/gsea/examples/gsea_go.R')
  stopifnot(nrow(results) > 0L, 'GO:0006260' %in% rownames(results), results['GO:0006260', 'NES'] > 0)
  cat(sprintf('ASSERT input1 go_terms=%d planted_nes=%.4f\n', nrow(results), results['GO:0006260', 'NES']))
}

if (input == 2L) {
  source('/mnt/openscience/wt/pathway-gsea/pathway-analysis/gsea/examples/gsea_msigdb.R')
  hit <- results[results$ID == 'HALLMARK_OXIDATIVE_PHOSPHORYLATION', , drop = FALSE]
  stopifnot(nrow(hit) == 1L, hit$NES > 0, hit$p.adjust < 0.05)
  cat(sprintf('ASSERT input2 hallmark_terms=%d oxphos_nes=%.4f\n', nrow(results), hit$NES))
}

if (input == 3L) {
  library(clusterProfiler); library(msigdbr)
  set.seed(321)
  h <- msigdbr(species = 'Homo sapiens', collection = 'H')
  t2g <- unique(h[, c('gs_name', 'ncbi_gene')])
  ids <- unique(as.character(t2g$ncbi_gene))[1:4000]
  gl <- sort(setNames(rnorm(length(ids)), ids), decreasing = TRUE)
  warnings <- character()
  g <- withCallingHandlers(GSEA(gl, TERM2GENE = t2g, minGSSize = 10, maxGSSize = 500,
                                pvalueCutoff = 1, nPerm = 1000, seed = TRUE, verbose = FALSE),
                           warning = function(w) { warnings <<- c(warnings, conditionMessage(w)); invokeRestart('muffleWarning') })
  guarded <- tryCatch({ if ('nPerm' %in% names(g@params)) stop('nPerm forced a fgseaSimple fallback - remove it'); FALSE },
                      error = function(e) grepl('fgseaSimple', conditionMessage(e), fixed = TRUE))
  unsorted <- tryCatch({ GSEA(rev(gl), TERM2GENE = t2g, minGSSize = 10, maxGSSize = 500, verbose = FALSE); FALSE },
                       error = function(e) grepl('decreasing sorted', conditionMessage(e), fixed = TRUE))
  duplicated <- tryCatch({ x <- c(gl, gl[1]); names(x)[length(x)] <- names(gl)[1]; GSEA(sort(x, decreasing = TRUE), TERM2GENE = t2g, minGSSize = 10, maxGSSize = 500, verbose = FALSE); FALSE },
                         error = function(e) grepl('Duplicate values', conditionMessage(e), fixed = TRUE))
  stopifnot(nrow(as.data.frame(g)) > 0L, any(grepl('fgseaSimple', warnings, fixed = TRUE)), guarded, unsorted, duplicated)
  cat(sprintf('ASSERT input3 nperm_terms=%d warning_guard=TRUE validation_errors=TRUE\n', nrow(as.data.frame(g))))
}

if (input == 4L) {
  library(GSVA)
  set.seed(456)
  expr <- matrix(rnorm(300 * 16), 300, dimnames = list(sprintf('G%03d', 1:300), sprintf('S%02d', 1:16)))
  sets <- list(UP = sprintf('G%03d', 1:30), DOWN = sprintf('G%03d', 31:60), NULL = sprintf('G%03d', 61:100))
  expr[sets$UP, 9:16] <- expr[sets$UP, 9:16] + 1
  expr[sets$DOWN, 9:16] <- expr[sets$DOWN, 9:16] - 1
  gs <- gsva(gsvaParam(expr, sets, kcdf = 'Gaussian', minSize = 10, maxSize = 100))
  ss <- gsva(ssgseaParam(expr, sets, minSize = 10, maxSize = 100))
  up <- mean(gs['UP', 9:16]) - mean(gs['UP', 1:8]); down <- mean(gs['DOWN', 9:16]) - mean(gs['DOWN', 1:8])
  stopifnot(identical(dim(gs), c(3L, 16L)), identical(dim(ss), c(3L, 16L)), all(is.finite(gs)), all(is.finite(ss)), up > .3, down < -.3)
  cat(sprintf('ASSERT input4 gsva_up=%.4f gsva_down=%.4f\n', up, down))
}

if (input == 5L) {
  library(clusterProfiler); library(msigdbr)
  set.seed(998)
  h <- msigdbr(species = 'Homo sapiens', collection = 'H')
  symbol_t2g <- unique(h[, c('gs_name', 'gene_symbol')])
  ids <- unique(as.character(symbol_t2g$gene_symbol)); ids <- ids[nzchar(ids)][1:4000]
  gl <- sort(setNames(rnorm(length(ids)), ids), decreasing = TRUE)
  ok <- GSEA(gl, TERM2GENE = symbol_t2g, minGSSize = 10, maxGSSize = 500, pvalueCutoff = 1, seed = TRUE, verbose = FALSE)
  mismatch <- tryCatch({ GSEA(gl, TERM2GENE = unique(h[, c('gs_name', 'ncbi_gene')]), minGSSize = 10, maxGSSize = 500, verbose = FALSE); FALSE },
                       error = function(e) grepl('No gene can be mapped|organism', conditionMessage(e)))
  stopifnot(nrow(as.data.frame(ok)) > 0L, mismatch)
  cat(sprintf('ASSERT input5 symbol_terms=%d mismatch_rejected=TRUE\n', nrow(as.data.frame(ok))))
}

if (input == 6L) {
  library(clusterProfiler); library(ReactomePA); library(org.Hs.eg.db)
  set.seed(777)
  ids <- head(keys(org.Hs.eg.db, keytype = 'ENTREZID'), 4000)
  gl <- sort(setNames(rnorm(length(ids)), ids), decreasing = TRUE)
  kegg <- gseKEGG(gl, organism = 'hsa', keyType = 'ncbi-geneid', minGSSize = 10, maxGSSize = 500, eps = 0, pvalueCutoff = 1, seed = TRUE, verbose = FALSE)
  reactome <- gsePathway(gl, organism = 'human', minGSSize = 10, maxGSSize = 500, eps = 0, pvalueCutoff = 1, seed = TRUE, verbose = FALSE)
  stopifnot(is.data.frame(as.data.frame(kegg)), is.data.frame(as.data.frame(reactome)))
  cat(sprintf('ASSERT input6 kegg_terms=%d reactome_terms=%d\n', nrow(as.data.frame(kegg)), nrow(as.data.frame(reactome))))
}

if (input == 7L) {
  library(limma)
  set.seed(901)
  expr <- matrix(rnorm(600 * 16), 600, dimnames = list(sprintf('GENE%03d', 1:600), sprintf('S%02d', 1:16)))
  sets <- list(UP = sprintf('GENE%03d', 1:30), DOWN = sprintf('GENE%03d', 31:60), NULL = sprintf('GENE%03d', 61:100))
  expr[sets$UP, 9:16] <- expr[sets$UP, 9:16] + 1.2
  expr[sets$DOWN, 9:16] <- expr[sets$DOWN, 9:16] - 1.2
  group <- factor(rep(c('Control', 'Case'), each = 8)); design <- model.matrix(~ group)
  idx <- ids2indices(sets, rownames(expr), remove.empty = TRUE)
  cam <- camera(expr, idx, design, contrast = 2, inter.gene.cor = NA)
  fr <- fry(expr, idx, design, contrast = 2)
  stopifnot(all(c('PValue', 'FDR', 'Direction') %in% names(cam)), all(c('PValue', 'FDR', 'Direction') %in% names(fr)), cam['UP', 'FDR'] < 0.05, cam['DOWN', 'FDR'] < 0.05, cam['UP', 'Direction'] != cam['DOWN', 'Direction'])
  cat(sprintf('ASSERT input7 camera_up=%s camera_down=%s up_fdr=%.3g down_fdr=%.3g fry_rows=%d\n', cam['UP', 'Direction'], cam['DOWN', 'Direction'], cam['UP', 'FDR'], cam['DOWN', 'FDR'], nrow(fr)))
}
