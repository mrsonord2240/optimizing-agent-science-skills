# specialized-topics.md cell-cycle fix (regress S score from LSI embedding), real 10x PBMC Multiome 3k (RNA gives real S.Score)
suppressPackageStartupMessages({library(Signac);library(Seurat);library(magrittr)}); set.seed(1)
obj <- readRDS(file.path(Sys.getenv("SCA"),"work/multiome_wnn.rds"))
DefaultAssay(obj) <- 'RNA'
obj <- CellCycleScoring(obj, s.features=cc.genes.updated.2019$s.genes, g2m.features=cc.genes.updated.2019$g2m.genes, set.ident=FALSE)
cat("Phase counts:", paste(names(table(obj$Phase)), table(obj$Phase), collapse="; "), "\n")
DefaultAssay(obj) <- 'ATAC'
# documented old fix: does it work?
r <- tryCatch({ScaleData(obj, features=rownames(obj)[1:2000], vars.to.regress='S.Score'); "ok"}, error=function(e) conditionMessage(e)); cat("OLD ScaleData(vars.to.regress) on ATAC:", r, "\n")
# new fix
lsi <- Embeddings(obj, 'lsi')
lsi[, -1] <- resid(lm(lsi[, -1] ~ obj$S.Score))
obj[['lsi_sreg']] <- CreateDimReducObject(lsi, key='LSIS_', assay='ATAC')
cs <- function(red) max(abs(cor(Embeddings(obj, red)[,2:30], obj$S.Score)))
cat("max|cor(LSI dim, S.Score)| before", round(cs('lsi'),3), "after", round(cs('lsi_sreg'),3), "\n")
cat("LSI1 unchanged:", identical(Embeddings(obj,'lsi')[,1], lsi[,1]), " dims", dim(lsi), " finite", all(is.finite(lsi)), "\n")
obj <- RunUMAP(obj, reduction='lsi_sreg', dims=2:30, reduction.name='umap.sreg', verbose=FALSE)
u0 <- RunUMAP(obj, reduction='lsi', dims=2:30, reduction.name='umap.plain', verbose=FALSE)
g <- function(o,n) max(abs(cor(Embeddings(o,n), obj$S.Score)))
cat("max|cor(UMAP, S.Score)| plain", round(g(u0,'umap.plain'),3), "regressed", round(g(obj,'umap.sreg'),3), "\n")
obj <- FindNeighbors(obj, reduction='lsi_sreg', dims=2:30, graph.name='g_sreg', verbose=FALSE); obj <- FindClusters(obj, graph.name='g_sreg', algorithm=4, resolution=0.5, verbose=FALSE)
ari <- function(a,b){t<-table(a,b);n<-sum(t);s<-function(x)sum(choose(x,2));ex<-s(rowSums(t))*s(colSums(t))/choose(n,2);(s(t)-ex)/(0.5*(s(rowSums(t))+s(colSums(t)))-ex)}
cat("ARI(clusters after regress, wnn clusters)", round(ari(obj$seurat_clusters, obj$wsnn_res.0.5),3), " n clusters", nlevels(obj$seurat_clusters), "\n")
