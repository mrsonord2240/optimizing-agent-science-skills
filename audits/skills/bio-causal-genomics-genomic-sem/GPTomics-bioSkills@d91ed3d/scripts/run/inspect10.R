library(GenomicSEM)
b <- deparse(body(usermodel))
idx <- grep("ReorderModel", b)
cat("Lines mentioning ReorderModel:\n")
for (i in idx) cat(i, ": ", b[i], "\n")
cat("\n--- context around first assignment ---\n")
i1 <- grep("ReorderModel *<-", b)[1]
cat(paste(b[max(1,i1-20):min(length(b), i1+10)], collapse="\n"), "\n")
