library(GenomicSEM)
b <- deparse(body(commonfactor))
i <- grep("Model1_Results *<-", b)
cat("Lines defining Model1_Results:\n")
for (k in i) cat(k, ": ", b[k], "\n")
cat("\n--- context (30 before, 15 after) around first occurrence ---\n")
i1 <- i[1]
cat(paste(b[max(1,i1-30):min(length(b), i1+15)], collapse="\n"), "\n")
