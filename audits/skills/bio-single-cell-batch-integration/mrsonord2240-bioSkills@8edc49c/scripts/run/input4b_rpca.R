# Follow-up to input 4: does RPCAIntegration (the method SKILL.md:135 actually prints) run
# once the future globals limit is raised? This is the standard Seurat workaround; the Skill
# never mentions it.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(future)})
cat('future.globals.maxSize default:', getOption('future.globals.maxSize'), '(NULL = 500 MiB)\n')
options(future.globals.maxSize = 4 * 1024^3)
D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D,'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True','TRUE',TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True','TRUE',TRUE)
rownames(tc) <- tc$cell_id
ss <- read.csv(file.path(D,'sample_sheet.csv')); rownames(ss) <- ss$sample
mats <- list()
for (s in paste0('S',1:8)) { m <- Read10X(file.path(D,s,'outs/filtered_feature_bc_matrix')); colnames(m) <- paste0(s,'_',colnames(m)); mats[[s]] <- m }
counts <- do.call(cbind, mats)
counts <- counts[, !tc[colnames(counts),'true_doublet'] & !tc[colnames(counts),'true_low_quality']]
o <- CreateSeuratObject(counts, min.cells=3, min.features=200)
o$batch <- ss[sub('_.*','',colnames(o)),'batch']
truth <- tc[colnames(o),'true_cell_type']
ari <- function(x,y){t<-table(x,y);n<-sum(t);s<-sum(choose(t,2));a<-sum(choose(rowSums(t),2));b<-sum(choose(colSums(t),2));e<-a*b/choose(n,2);(s-e)/((a+b)/2-e)}
set.seed(20260916)
o[['RNA']] <- split(o[['RNA']], f=o$batch)
o <- NormalizeData(o,verbose=FALSE); o <- FindVariableFeatures(o,verbose=FALSE)
o <- ScaleData(o,verbose=FALSE); o <- RunPCA(o,npcs=50,verbose=FALSE)
t0 <- Sys.time()
r <- try({o <- IntegrateLayers(o, method=RPCAIntegration, orig.reduction='pca', new.reduction='int.rpca', verbose=FALSE); o <- JoinLayers(o); o <- FindNeighbors(o, reduction='int.rpca', dims=1:30, verbose=FALSE); FindClusters(o, resolution=0.5, verbose=FALSE)}, silent=TRUE)
if (inherits(r,'try-error')) cat('STILL FAILED:', as.character(r)) else
  cat(sprintf('RPCAIntegration with future.globals.maxSize=4GB: %ss, %d clusters, ARI %.3f\n',
      round(as.numeric(difftime(Sys.time(),t0,units='secs')),1), length(unique(Idents(r))), ari(as.character(Idents(r)), truth)))
cat('DONE\n')
