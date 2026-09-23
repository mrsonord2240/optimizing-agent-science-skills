args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L)
out <- args[[1]]
dir.create(out, recursive = TRUE, showWarnings = FALSE)
set.seed(20260923)

# Synthetic 240-gene, 4-vs-4 bulk pilot for the PROPER wrapper.
genes <- paste0("gene", seq_len(240))
condition <- rep(c("A", "B"), each = 4)
mu <- rgamma(length(genes), shape = 5, rate = 0.025)
disp <- 0.12
counts <- sapply(seq_along(condition), function(i) {
  de <- seq_len(length(genes)) <= 24L & condition[i] == "B"
  rnbinom(length(genes), mu = mu * ifelse(de, 1.5, 1), size = 1 / disp)
})
colnames(counts) <- paste0(condition, seq_len(ncol(counts)))
rownames(counts) <- genes
write.csv(counts, file.path(out, "pilot_counts.csv"), quote = FALSE)

# Synthetic single-cell count lists for eight donor-level pseudobulks.
donors <- paste0("D", seq_len(8))
donor_condition <- rep(c("control", "treated"), each = 4)
cell_counts <- setNames(lapply(seq_along(donors), function(i) {
  de <- seq_len(180) <= 18L & donor_condition[i] == "treated"
  donor_mu <- rgamma(180, shape = 5, rate = 0.04) * ifelse(de, 1.5, 1)
  matrix(rnbinom(180 * 60, mu = rep(donor_mu, 60), size = 1 / 0.10),
         nrow = 180, dimnames = list(paste0("g", seq_len(180)), paste0("cell", seq_len(60))))
}), donors)
saveRDS(cell_counts, file.path(out, "cell_counts.rds"))
write.csv(data.frame(donor = donors, condition = donor_condition),
          file.path(out, "donor_condition.csv"), row.names = FALSE, quote = FALSE)
cat("OK synthetic fixtures: 240 genes x 8 bulk samples; 180 genes x 8 donors x 60 cells\n")
