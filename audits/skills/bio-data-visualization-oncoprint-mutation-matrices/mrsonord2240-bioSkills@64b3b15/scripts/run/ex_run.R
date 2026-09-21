# Run the shipped example verbatim from a copy, after defining what it leaves undefined (mat, clinical)
obj <- readRDS("out/i5_objects.rds"); clin <- read.delim("data/synth_cohort_clin.tsv", stringsAsFactors=FALSE)
mat <- obj$matS
clinical <- data.frame(Tumor_Sample_Barcode=clin$Tumor_Sample_Barcode, subtype=clin$subtype, stage=clin$stage, tmb=clin$tmb)
rownames(clinical) <- clinical$Tumor_Sample_Barcode; clinical <- clinical[colnames(mat),]
setwd("ex")
source("oncoprint_phd.R", echo=FALSE)
cat("pdf exists:", file.exists("oncoprint.pdf"), "size:", file.size("oncoprint.pdf"), "\n")
cat("class(si):", paste(class(si), collapse="/"), " dim:", paste(dim(si), collapse="x"), "\n")
