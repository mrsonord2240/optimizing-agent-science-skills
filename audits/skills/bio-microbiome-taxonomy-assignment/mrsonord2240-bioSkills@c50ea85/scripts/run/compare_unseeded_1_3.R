dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax"
f1 <- as.matrix(read.csv(file.path(dir, "idtaxa_new_flat.csv"), row.names = 1))
f3 <- readRDS(file.path(dir, "idtaxa_unseeded_run3.rds"))
cat("run1 genus assigned:", sum(!is.na(f1[,"genus"])), "/770\n")
cat("run3 genus assigned:", sum(!is.na(f3[,"genus"])), "/770\n")
diff <- sum(f1[,"genus"] != f3[,"genus"], na.rm=TRUE) + sum(xor(is.na(f1[,"genus"]), is.na(f3[,"genus"])))
cat("genus differ between run1 and run3 (both unseeded, independent IdTaxa calls):", diff, "/770\n")
