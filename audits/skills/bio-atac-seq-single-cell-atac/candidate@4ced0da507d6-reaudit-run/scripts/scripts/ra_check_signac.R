suppressPackageStartupMessages({library(Signac);library(Seurat)})
for (tag in c("doc","relaxed")) {
 f <- file.path(Sys.getenv("SCA"),paste0("work/ra_signac_",tag,"/scatac_signac.rds")); o <- readRDS(f)
 cat("==",tag,": cells",ncol(o)," assays",paste(Assays(o),collapse=","),"\n")
 cat("clusters",table(o$seurat_clusters),"\n")
 cat("passed_filters range",range(o$passed_filters),"TSS",round(range(o$TSS.enrichment),2),"nucsig",round(range(o$nucleosome_signal),2),"FRiP%",round(range(o$pct_reads_in_peaks),1),"blacklist",round(range(o$blacklist_ratio),3),"mito",round(range(o$mito_fraction),4),"\n")
 cat("rule check: all passed_filters in [1000,80000]:",all(o$passed_filters>=ifelse(tag=="doc",1000,1000)&o$passed_filters<=80000),
     " nuc<=4:",all(o$nucleosome_signal<=4)," FRiP>=15:",all(o$pct_reads_in_peaks>=15)," bl<0.05:",all(o$blacklist_ratio<0.05)," mito<0.05:",all(o$mito_fraction<0.05),
     " TSS>=",ifelse(tag=="doc",4,1),":",all(o$TSS.enrichment>=ifelse(tag=="doc",4,1)),"\n")
 cat("depth cor LSI1..3:", round(sapply(1:3,function(i) cor(Embeddings(o,"lsi")[,i],log10(o$nCount_ATAC))),2),"\n")
 a <- GetAssayData(o,assay="ACT",layer="data")
 cat("ACT dim",dim(o[["ACT"]]),"finite",all(is.finite(a@x)),"umap",dim(Embeddings(o,"umap")),"umap finite",all(is.finite(Embeddings(o,"umap"))),"\n")
 cat("annotation seqlevels",head(seqlevels(Annotation(o[["ATAC"]])),3),"genome",unique(genome(Annotation(o[["ATAC"]]))),"\n")
 # gene activity sanity: known genes present and non-trivial on chr1 slice
 g <- intersect(c("CD3E","MS4A1","CD14","NKG7","GNLY"), rownames(a)); cat("chr1-slice marker genes in ACT:",g,"\n")
}
