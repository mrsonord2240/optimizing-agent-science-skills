# Input 4 (Variant B) - bio-single-cell-preprocessing
# "Which normalization?" - the Skill's Normalization decision table (SKILL.md:149-156) and its
# Governing Principle about composition-divergent cell types, tested empirically.
# Data: SYNTHETIC 8-sample PBMC set (megakaryocytes are the composition-divergent, PPBP-dominant
# population here, standing in for the plasma/secretory cells the Skill names).
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Seurat); library(scran); library(scuttle); library(SingleCellExperiment); library(Matrix)
})
cat('Seurat', as.character(packageVersion('Seurat')), '| scran', as.character(packageVersion('scran')),
    '| sctransform', as.character(packageVersion('sctransform')), '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
counts <- Read10X(file.path(D, 'S2/outs/filtered_feature_bc_matrix'))
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc <- tc[tc$sample == 'S2', ]
rownames(tc) <- tc$barcode
lab <- tc[colnames(counts), 'true_cell_type']
cat('cells:', ncol(counts), '| types:\n'); print(table(lab))

libsize <- colSums(counts)
cat('\nmedian library size by true type:\n')
print(round(tapply(libsize, lab, median)))

## --- Route 1: shifted-log (Skill default, SKILL.md:145) ---
so <- CreateSeuratObject(counts)
so <- NormalizeData(so, normalization.method = 'LogNormalize', scale.factor = 10000, verbose = FALSE)

## --- Route 2: scran deconvolution (Skill: "low-depth, high-dropout"; needs quickCluster) ---
sce <- SingleCellExperiment(list(counts = counts))
set.seed(20260916)
cl <- quickCluster(sce)
sce <- computeSumFactors(sce, clusters = cl)
sf <- sizeFactors(sce)
cat('\nscran size factors: min', round(min(sf), 4), 'max', round(max(sf), 3),
    '| any negative?', any(sf <= 0), '\n')
libsf <- libsize / mean(libsize)
cat('cor(scran sf, library-size sf) =', round(cor(sf, libsf), 4), '\n')
cat('ratio scran_sf / libsize_sf by true type (1 = the two agree):\n')
print(round(tapply(sf / libsf, lab, median), 3))
sce <- logNormCounts(sce)

## --- Route 3: sctransform v2 (Skill: Seurat depth removal for HVG/viz) ---
t0 <- Sys.time()
so_sct <- SCTransform(so, verbose = FALSE, seed.use = 20260916)
cat('\nSCTransform: ', round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1), 's, ',
    length(VariableFeatures(so_sct)), ' variable features, vst.flavor = ',
    so_sct@assays$SCT@SCTModel.list[[1]]@arguments$vst.flavor, '\n', sep = '')

## --- The compositional see-saw the Governing Principle warns about ---
# PPBP is the dominant transcript of megakaryocytes/platelets.
mk <- which(lab == 'Megakaryocytes'); other <- which(lab != 'Megakaryocytes')
cat('\nPPBP share of the megakaryocyte transcriptome:',
    round(100 * mean(counts['PPBP', mk] / libsize[mk]), 1), '%\n')
ln <- GetAssayData(so, layer = 'data')
hk <- c('ACTB', 'GAPDH', 'B2M', 'TMSB4X')
hk <- intersect(hk, rownames(counts))
cat('housekeeping genes, mean shifted-log expression (Mk vs rest):\n')
for (g in hk) {
  cat(sprintf('  %-7s Mk=%.3f  rest=%.3f  delta=%+.3f | raw CPM Mk=%.0f rest=%.0f\n', g,
              mean(ln[g, mk]), mean(ln[g, other]), mean(ln[g, mk]) - mean(ln[g, other]),
              1e6 * mean(counts[g, mk] / libsize[mk]), 1e6 * mean(counts[g, other] / libsize[other])))
}
cat('-> read together with the size-factor ratios above: library-size (shifted-log) and scran size\n')
cat('   factors disagree systematically BY CELL TYPE (Mk 0.89, NK 1.36). That type-dependent gap is\n')
cat('   the composition dependence the Governing Principle warns about, so the shifted-log deltas\n')
cat('   above are part biology and part size-factor choice and cannot be read as absolute amounts.\n')

## --- exclude_highly_expressed, the Skill's named remedy (SKILL.md Common Errors) ---
# Seurat has no such flag; scanpy does. Check the R-side equivalent the Skill implies: scran.
cat('\nscran-normalized housekeeping delta (Mk vs rest):\n')
lc <- logcounts(sce)
for (g in hk) cat(sprintf('  %-7s delta=%+.3f\n', g, mean(lc[g, mk]) - mean(lc[g, other])))
cat('DONE\n')
