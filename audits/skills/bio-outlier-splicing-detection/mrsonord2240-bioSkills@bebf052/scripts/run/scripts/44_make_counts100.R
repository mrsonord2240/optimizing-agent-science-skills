# NEW synthetic count matrix (audit's own input): 3000 genes x 100 samples, NB + hidden batch + 20 planted outliers (seed 5150).
set.seed(5150)
G <- 3000; N <- 100
mu <- exp(rnorm(G, log(300), 1.2)); sf <- exp(rnorm(N, 0, 0.25)); batch <- rep(c(0, 1), length.out = N)
bfx <- ifelse(runif(G) < 0.25, exp(rnorm(G, 0, 0.5)), 1); disp <- 0.05 + runif(G) * 0.15
M <- outer(mu, sf) * ifelse(outer(rep(1, G), batch) == 1, bfx, 1)
gi <- sample(1:G, 20); si <- sample(1:N, 20, replace = TRUE); fold <- rep(c(0.05, 0.1, 0.2, 5, 8), 4)
truth <- data.frame(gene = paste0("gene", gi), sample = paste0("S", sprintf("%03d", si)), fold = fold, stringsAsFactors = FALSE)
for (i in 1:20) M[gi[i], si[i]] <- M[gi[i], si[i]] * fold[i]
cnt <- matrix(rnbinom(G * N, mu = M, size = 1 / disp), nrow = G)
rownames(cnt) <- paste0("gene", seq_len(G)); colnames(cnt) <- paste0("S", sprintf("%03d", seq_len(N)))
out <- commandArgs(TRUE)[1]; dir.create(out, showWarnings = FALSE, recursive = TRUE)
write.table(cnt, file.path(out, "counts.tsv"), sep = "\t", quote = FALSE)
write.table(truth, file.path(out, "outrider_truth.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
writeLines("SYNTHETIC counts (44_make_counts100.R, seed 5150)", file.path(out, "README_SYNTHETIC.txt"))
cat("wrote", dim(cnt), "\n")
