suppressPackageStartupMessages({library(Rtsne); library(uwot)})
X <- as.matrix(read.csv("F:/OpenScience/audits/bio-data-visualization-dimensionality-reduction-plots/data/sc_hier_x.csv", header=FALSE))[1:500,]
a <- Rtsne(X, perplexity=30, seed=42, max_iter=300); b <- Rtsne(X, perplexity=30, seed=42, max_iter=300)
cat("Rtsne(seed=42) twice (no set.seed) identical:", identical(a$Y,b$Y), "\n")
u1 <- umap(X, n_neighbors=30, seed=42, n_threads=1); u2 <- umap(X, n_neighbors=30, seed=42, n_threads=1)
cat("uwot umap(seed=42) twice (no set.seed) identical:", identical(u1,u2), "\n")
cat("uwot seed doc:\n"); print(head(grep("seed", capture.output(tools::Rd2txt(utils:::.getHelpFile(help("umap", package="uwot")), options=list(underline_titles=FALSE))), value=TRUE, ignore.case=TRUE), 6))
