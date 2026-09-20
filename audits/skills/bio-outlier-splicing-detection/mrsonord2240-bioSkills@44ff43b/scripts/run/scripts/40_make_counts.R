# SYNTHETIC gene-level count matrix for the OUTRIDER test (3000 genes x 30 samples, NB + latent batch + planted outliers).
set.seed(20260920)
G <- 3000; N <- 30
mu <- exp(rnorm(G, log(300), 1.2))
sf <- exp(rnorm(N, 0, 0.25))
batch <- rep(c(0, 1), length.out = N)
bfx <- ifelse(runif(G) < 0.25, exp(rnorm(G, 0, 0.5)), 1)      # 25% of genes respond to a hidden batch
disp <- 0.05 + runif(G) * 0.15
M <- outer(mu, sf) * ifelse(outer(rep(1, G), batch) == 1, bfx, 1)
truth <- data.frame(gene = paste0("gene", c(101, 202, 303, 404, 505, 606, 707, 808)),
                    sample = paste0("S", sprintf("%02d", c(3, 9, 14, 21, 6, 17, 25, 28))),
                    fold = c(0.05, 0.1, 0.1, 0.2, 6, 5, 8, 5), stringsAsFactors = FALSE)
for (i in seq_len(nrow(truth))) { gi <- as.integer(sub("gene", "", truth$gene[i])); si <- as.integer(sub("S", "", truth$sample[i])); M[gi, si] <- M[gi, si] * truth$fold[i] }
size <- 1 / disp
cnt <- matrix(rnbinom(G * N, mu = M, size = size), nrow = G)
rownames(cnt) <- paste0("gene", seq_len(G)); colnames(cnt) <- paste0("S", sprintf("%02d", seq_len(N)))
out <- commandArgs(TRUE)[1]; dir.create(out, showWarnings = FALSE, recursive = TRUE)
write.table(cnt, file.path(out, "counts.tsv"), sep = "\t", quote = FALSE)
write.table(truth, file.path(out, "outrider_truth.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
writeLines("SYNTHETIC counts (40_make_counts.R, seed 20260920); truth in outrider_truth.tsv", file.path(out, "README_SYNTHETIC.txt"))
cat("wrote", dim(cnt), "\n")
