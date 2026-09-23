# Fresh Input 9: Arrow parquet to documented iq MaxLFQ.
suppressPackageStartupMessages({library(iq);library(arrow)})
r <- as.data.frame(read_parquet("/mnt/openscience/audits/bio-proteomics-data-import/data/report.parquet"))
r <- r[r$Q.Value<=.01&r$PG.Q.Value<=.01,]
p <- data.frame(protein=r$Protein.Group,ion=r$Precursor.Id,run=r$Run,intensity=r$Precursor.Normalised)
p <- p[is.finite(p$intensity)&p$intensity>0,]
o <- "/mnt/openscience/audits/bio-proteomics-quantification/run/phase2_corrective_20260923"
write.csv(p,file.path(o,"diann_peptide_long.csv"),row.names=FALSE)
n <- preprocess(p,primary_id="protein",secondary_id="ion",sample_id="run",intensity_col="intensity",median_normalization=TRUE,pdf_out=NULL)
pt <- create_protein_table(create_protein_list(n),method="maxLFQ")
stopifnot(nrow(pt$estimate)>900,ncol(pt$estimate)==8,all(is.finite(as.matrix(pt$estimate)[!is.na(pt$estimate)])))
write.csv(pt$estimate,file.path(o,"diann_maxlfq.csv"))
cat("INPUT9 rows=",nrow(p)," matrix=",paste(dim(pt$estimate),collapse="x")," disconnected=",sum(nzchar(pt$annotation)),"\n",sep="")
