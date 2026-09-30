# Probes for prose claims in SKILL.md/references (one bounded script). Run in bio-atac-seq-single-cell-atac-r.
suppressPackageStartupMessages({library(Signac);library(Seurat)})
cat("== %>% availability after library(Signac); library(Seurat) only\n"); cat(exists("%>%"), "\n")
cat("== leidenbase (FindClusters algorithm=4)\n")
cat("Seurat Suggests has leidenbase:", grepl("leidenbase", packageDescription("Seurat")$Suggests), " Imports has:", grepl("leidenbase", packageDescription("Seurat")$Imports), " installed:", requireNamespace("leidenbase", quietly=TRUE), "\n")
cat("== XIST locus hg38 coordinates from EnsDb v86 vs Skill chrX:73820651-73852753\n")
suppressPackageStartupMessages({library(EnsDb.Hsapiens.v86);library(ensembldb)})
g <- genes(EnsDb.Hsapiens.v86, filter=GeneNameFilter(c("XIST","KDM6A","DDX3X","EIF1AX","UTY","DDX3Y")))
print(as.data.frame(g)[,c("seqnames","start","end","strand","gene_name")])
cat("== ScaleData(vars.to.regress) before RunSVD: does it work / change the LSI? (Skill cell-cycle Fix)
")
D <- Sys.getenv("ATACDATA"); set.seed(1)
counts <- Read10X_h5(file.path(D,"scatac/outs/filtered_peak_bc_matrix.h5"))
ca <- CreateChromatinAssay(counts, sep=c(":","-"), genome="hg38", min.cells=10, min.features=200)
o <- CreateSeuratObject(ca, assay="ATAC"); o$S.score <- rnorm(ncol(o))   # SYNTHETIC covariate (label: synthetic)
o <- RunTFIDF(o); o <- FindTopFeatures(o, min.cutoff="q0"); o1 <- RunSVD(o)
try1 <- function(lbl, expr) { r <- tryCatch(expr, error=function(e){cat(lbl, "FAILED:", conditionMessage(e), "
"); NULL}); r }
o2 <- try1("ScaleData(vars.to.regress='S.score') as documented", ScaleData(o, vars.to.regress="S.score", verbose=FALSE))
o3 <- try1("ScaleData(features=VariableFeatures, vars.to.regress)", ScaleData(o, features=VariableFeatures(o), vars.to.regress="S.score", verbose=FALSE))
o4 <- try1("ScaleData() no regression", ScaleData(o, verbose=FALSE))
for (nm in c("o2","o3","o4")) { x <- get(nm); if (!is.null(x)) { x <- RunSVD(x); a <- Embeddings(o1,"lsi"); b <- Embeddings(x,"lsi")
  cat(nm, "scale.data present:", "scale.data" %in% Layers(x[["ATAC"]]), " LSI identical to no-ScaleData LSI:", isTRUE(all.equal(a,b)), " max abs diff", signif(max(abs(a-b)),3), "
") } }
cat("== RunSVD.Assay source excerpt (which layer feeds the SVD)
")
print(grep("layer|slot|scale", deparse(Signac:::RunSVD.Assay), value=TRUE))
