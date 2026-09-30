# Extract the ```r blocks of references/single-cell.md verbatim and wrap them with data preamble/postamble.
import re,sys
md=open(r'F:\OpenScience\wt\atac-motif-deviation\skills\bio-atac-seq-motif-deviation\references\single-cell.md',encoding='utf-8').read()
blocks=re.findall(r'```r\n(.*?)```',md,re.S)
assert len(blocks)==2
sig_pre='''if (nzchar(Sys.getenv("SIGNAC_LIB"))) .libPaths(c(Sys.getenv("SIGNAC_LIB"), .libPaths()))
suppressPackageStartupMessages({library(Signac);library(Seurat);library(JASPAR2024);library(TFBSTools);library(BSgenome.Hsapiens.UCSC.hg38);library(RSQLite);library(GenomicRanges);library(Matrix)})
D <- Sys.getenv("ATACDATA")
cat("Signac",as.character(packageVersion("Signac")),"chromVAR",as.character(packageVersion("chromVAR")),"\n")
m <- Read10X_h5(file.path(D,"scatac/outs/filtered_peak_bc_matrix.h5"))
m <- m[grepl("^chr1:",rownames(m)),]
gr <- StringToGRanges(rownames(m), sep=c(":","-")); m <- m[end(gr)<=30e6,]; m <- m[, Matrix::colSums(m)>=500]
cat("matrix",dim(m),"\n")
ca <- CreateChromatinAssay(m, sep=c(":","-"), fragments=file.path(D,"scatac/outs/fragments.tsv.gz"), genome="hg38")
obj <- CreateSeuratObject(ca, assay="ATAC")
obj <- RunTFIDF(obj); obj <- FindTopFeatures(obj, min.cutoff=20); obj <- RunSVD(obj)
obj <- FindNeighbors(obj, reduction="lsi", dims=2:20); obj <- FindClusters(obj, algorithm=3, resolution=0.3, verbose=FALSE)
print(table(obj$seurat_clusters)); seurat_obj <- obj
'''
sig_post='''
markers$tf <- ConvertMotifID(seurat_obj[['ATAC']], id=markers$gene)
cat("markers cols:",paste(colnames(markers),collapse=","),"\n")
zz <- GetAssayData(seurat_obj,layer="data"); cat("chromvar assay",dim(zz),"NA",sum(is.na(zz)),"range",range(zz),"\n")
for (cl in levels(markers$cluster)) { s <- markers[markers$cluster==cl,]; s<-s[order(s$p_val_adj),]; cat("cluster",cl,":",paste(head(s$tf,8),collapse=" "),"\n") }
write.csv(markers,file.path(Sys.getenv("OUTD"),"markers.csv"))
'''
open('sc_signac.R','w',encoding='utf-8').write(sig_pre+blocks[0]+sig_post)
arch_pre='''suppressPackageStartupMessages({library(ArchR);library(GenomicRanges)}); setwd(file.path(Sys.getenv("MD"),"work/archr")); addArchRGenome("hg38"); addArchRThreads(2)
proj <- loadArchRProject("ArchROut"); print(table(proj$Clusters))
'''
# only the guard + marker call (lines after addDeviationsMatrix)
b=blocks[1]; i=b.index('# Sparse cells')
arch_post='''
cat("dropped cells:", length(na_cells), " remaining:", length(proj$cellNames), "\n")
mk <- getMarkers(markersMotifs, cutOff="FDR <= 0.05 & MeanDiff >= 0.5")
for (n in names(mk)) cat(n, nrow(mk[[n]]), ":", paste(head(mk[[n]]$name,8),collapse=" "), "\n")
mm2 <- getMatrixFromProject(proj, useMatrix='MotifMatrix'); cat("post-guard NA in z:", sum(is.na(assays(mm2)$z)), " dim", dim(mm2), "\n")
'''
open('sc_archr.R','w',encoding='utf-8').write(arch_pre+b[i:]+arch_post)
# also emit a control lacking the guard
j=b.index('# Per-cluster deviation summary')
open('sc_archr_noguard.R','w',encoding='utf-8').write(arch_pre+b[j:])
