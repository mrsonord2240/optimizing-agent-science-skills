suppressPackageStartupMessages({library(Signac);library(Seurat)})
for (tag in c("arc","atac2x","atac2x_default","atac1x_default","atac1x_relaxed")) {
 f <- file.path(Sys.getenv("SCA"),paste0("work/reaudit10x_",tag,"/scatac_signac.rds"))
 if (!file.exists(f)) { cat("==",tag,": no rds\n"); next }
 o <- readRDS(f)
 cat("==",tag,": cells",ncol(o)," assays",paste(Assays(o),collapse=","),"\n")
 cat("clusters",table(o$seurat_clusters),"\n")
 cat("passed_filters",range(o$passed_filters),"TSS",round(range(o$TSS.enrichment),2),"nucsig",round(range(o$nucleosome_signal),2),"FRiP%",round(range(o$pct_reads_in_peaks),1),"blacklist",signif(range(o$blacklist_ratio),3),"mito",if("mito_fraction"%in%colnames(o[[]])) signif(range(o$mito_fraction),3) else NA,"\n")
 cat("depth cor LSI1..3:", round(sapply(1:3,function(i) cor(Embeddings(o,"lsi")[,i],log10(o$nCount_ATAC))),2),"\n")
 u <- Embeddings(o,"umap"); cat("ACT dim",dim(o[["ACT"]]),"umap",dim(u),"finite",all(is.finite(u)),"genome",unique(genome(Annotation(o[["ATAC"]]))),"\n")
 if (tag=="arc") { md <- read.csv(file.path(Sys.getenv("ATACDATA"),"10x-multiome/arc-pbmc3k/pbmc_granulocyte_sorted_3k_per_barcode_metrics.csv"),row.names=1)
   cat("ARC: is_cell in kept", mean(md[colnames(o),"is_cell"]==1),"; passed_filters==atac_fragments:", all(o$passed_filters==md[colnames(o),"atac_fragments"]),"; raw mito/raw range", signif(range(md[colnames(o),"atac_mitochondrial_reads"]/md[colnames(o),"atac_raw_reads"]),3),"\n")
   cat("ARC QC-filtered-out reasons among matrix cells not kept: n_not_kept", 2687-ncol(o),"\n") }
}
