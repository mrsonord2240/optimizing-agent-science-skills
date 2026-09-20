suppressPackageStartupMessages(library(DRIMSeq))
m <- methods::getMethod("dmFilter", "dmDSdata")
cat("dmFilter defaults (from installed DRIMSeq 1.34.0):\n"); print(formals(methods::slot(m, ".Data"))); 
f <- body(m)[[2]]  # .local
print(formals(eval(f[[3]])))[c("min_samps_gene_expr","min_gene_expr","min_samps_feature_expr","min_feature_expr","min_samps_feature_prop","min_feature_prop")]
