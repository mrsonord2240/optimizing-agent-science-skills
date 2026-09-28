args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 2L) stop("usage: prepare_stress.R <input-clinical> <output-clinical>")
x <- read.delim(args[1], check.names=FALSE)
names(x)[names(x)=="subtype"] <- "Subtype"
names(x)[names(x)=="stage"] <- "Stage"
stopifnot(all(c("Tumor_Sample_Barcode","Subtype","Stage","tmb") %in% names(x)))
write.table(x, args[2], sep="\t", quote=FALSE, row.names=FALSE)
cat("prepared",nrow(x),"stress clinical rows\n")
