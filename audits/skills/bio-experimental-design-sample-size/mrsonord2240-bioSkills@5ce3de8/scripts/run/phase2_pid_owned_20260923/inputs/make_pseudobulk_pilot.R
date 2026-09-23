set.seed(20260923)
ngenes <- 160L
ncells <- 24L
donors <- sprintf("D%02d", 1:8)
conditions <- rep(c("control", "case"), each = 4)
base_mu <- exp(rnorm(ngenes, log(4), 0.5))
cell_counts <- setNames(lapply(seq_along(donors), function(j) {
  fc <- if (conditions[j] == "case") c(rep(1.5, 16L), rep(1, ngenes - 16L)) else rep(1, ngenes)
  m <- sapply(seq_len(ncells), function(k) rnbinom(ngenes, mu = base_mu * fc, size = 1 / 0.3))
  rownames(m) <- sprintf("Gene%03d", seq_len(ngenes))
  colnames(m) <- paste0(donors[j], "_Cell", seq_len(ncells))
  m
}), donors)
args <- commandArgs(trailingOnly = TRUE)
saveRDS(cell_counts, args[1])
write.csv(data.frame(donor = donors, condition = conditions), args[2], row.names = FALSE, quote = FALSE)
stopifnot(length(readRDS(args[1])) == 8L, nrow(read.csv(args[2])) == 8L)
cat("OK synthetic pseudobulk pilot: 8 donors x 160 genes x 24 cells written\n")
