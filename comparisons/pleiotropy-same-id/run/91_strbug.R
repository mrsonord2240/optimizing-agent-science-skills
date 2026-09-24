x <- readRDS("F:/OpenScience/comparisons/pleiotropy-same-id/run/out/theirs_A_balanced.rds")$res$presso_block
ot <- x$presso$`MR-PRESSO results`$`Outlier Test`; p <- ot$Pvalue
cat("class:", class(p), "\nnon-1 entries:", paste(p[p!="1"], collapse=" "), "\n")
cat("verbatim which(p<0.05):", which(p < 0.05), "\n")
pv <- suppressWarnings(as.numeric(sub("<","",p)))
cat("numeric parse which(p<0.05):", which(pv < 0.05), "\n")
