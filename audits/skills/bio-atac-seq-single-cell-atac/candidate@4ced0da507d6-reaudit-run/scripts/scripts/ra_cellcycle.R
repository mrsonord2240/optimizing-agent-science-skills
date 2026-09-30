# Re-audit: cell-cycle LSI regression block extracted VERBATIM from live specialized-topics.md, on the Multiome object produced by ra_wnn.R.
suppressPackageStartupMessages({library(Signac);library(Seurat)}); set.seed(1)
SKILL<-Sys.getenv("SKILL")
md<-paste(readLines(file.path(SKILL,"references/specialized-topics.md"),encoding="UTF-8"),collapse="\n")
blk<-regmatches(md,gregexpr("(?s)```r\n(.*?)```",md,perl=TRUE))[[1]]; blk<-blk[grepl("lsi_sreg",blk)][1]
blk<-sub("^```r\n","",blk); blk<-sub("```$","",blk); cat(blk,"\n")
obj<-readRDS(file.path(Sys.getenv("SCA"),"work/ra_multiome_wnn.rds"))
DefaultAssay(obj)<-"RNA"
obj<-CellCycleScoring(obj,s.features=cc.genes.updated.2019$s.genes,g2m.features=cc.genes.updated.2019$g2m.genes,set.ident=FALSE)
cat("Phase:",paste(names(table(obj$Phase)),table(obj$Phase),collapse="; "),"\n")
DefaultAssay(obj)<-"ATAC"
l0<-Embeddings(obj,"lsi")
eval(parse(text=blk))
cs<-function(red) max(abs(cor(Embeddings(obj,red)[,2:30],obj$S.Score)))
cat("max|cor(LSI2:30,S.Score)| before",round(cs("lsi"),3),"after",round(cs("lsi_sreg"),3),"\n")
cat("LSI1 unchanged:",identical(unname(l0[,1]),unname(Embeddings(obj,"lsi_sreg")[,1])),"dim",dim(Embeddings(obj,"lsi_sreg")),"finite",all(is.finite(Embeddings(obj,"lsi_sreg"))),"\n")
cat("reductions:",names(obj@reductions),"\n"); u<-Embeddings(obj,"umap"); cat("umap",dim(u),"finite",all(is.finite(u)),"\n")
