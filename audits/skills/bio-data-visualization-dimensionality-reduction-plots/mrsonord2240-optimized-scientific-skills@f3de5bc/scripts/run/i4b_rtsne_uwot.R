# Input 4b: SKILL.md R blocks (Rtsne, uwot); parameter names; seed claims; small-n perplexity
suppressPackageStartupMessages({library(Rtsne); library(uwot)})
D <- "F:/OpenScience/audits/bio-data-visualization-dimensionality-reduction-plots/data"
X <- as.matrix(read.csv(file.path(D, "sc_hier_x.csv"), header=FALSE)); lab <- read.csv(file.path(D,"sc_hier6_labels.csv"))[,1]
cat("packageVersion Rtsne", as.character(packageVersion("Rtsne")), " uwot", as.character(packageVersion("uwot")), "\n")
cat("Rtsne formals has 'seed'?", "seed" %in% names(formals(Rtsne:::Rtsne.default)), " | 'Y_init'?", "Y_init" %in% names(formals(Rtsne:::Rtsne.default)), " | 'max_iter'?", "max_iter" %in% names(formals(Rtsne:::Rtsne.default)), " | 'pca_scale'?", "pca_scale" %in% names(formals(Rtsne:::Rtsne.default)), " | 'n_iter'?", "n_iter" %in% names(formals(Rtsne:::Rtsne.default)), "\n")
cat("uwot::umap formals has 'seed'?", "seed" %in% names(formals(uwot::umap)), " | n_neighbors, min_dist, metric:", all(c("n_neighbors","min_dist","metric") %in% names(formals(uwot::umap))), "\n")
# ---- Skill Rtsne block verbatim
set.seed(42)
ts <- Rtsne(X, perplexity = 30, theta = 0.5, pca_scale = TRUE, initial_dims = 50, max_iter = 750)
cat("Rtsne dim:", dim(ts$Y), " (n rows of X =", nrow(X), ")\n")
set.seed(42); ts2 <- Rtsne(X, perplexity = 30, theta = 0.5, pca_scale = TRUE, initial_dims = 50, max_iter = 750)
cat("Rtsne set.seed(42) twice identical:", identical(ts$Y, ts2$Y), "\n")
ts3 <- Rtsne(X, perplexity = 30, theta = 0.5, pca_scale = TRUE, initial_dims = 50, max_iter = 750)
cat("Rtsne without re-seeding differs from first:", !identical(ts$Y, ts3$Y), "\n")
# seed= argument the Skill's failure-mode section recommends
r <- try(Rtsne(X, perplexity=30, seed=42), silent=TRUE); cat("Rtsne(..., seed=42):", if (inherits(r,"try-error")) paste("ERROR", substr(as.character(r),1,120)) else if (!is.null(r$Y)) "no error (arg silently absorbed)" , "\n")
# PCA-init via Y_init as Skill says
pc <- prcomp(X, center=TRUE, scale.=TRUE)$x[,1:2]; pc <- pc/sd(pc[,1])*1e-4
ts4 <- Rtsne(X, perplexity=30, theta=0.5, pca_scale=TRUE, initial_dims=50, max_iter=750, Y_init=pc); cat("Rtsne with Y_init ok:", all(dim(ts4$Y)==c(nrow(X),2)), "\n")
# small-n perplexity: Skill says perplexity > n/3 fails
Xs <- X[1:60,]
for (p in c(30, 19, 5)) { r <- try(Rtsne(Xs, perplexity=p, max_iter=250), silent=TRUE); cat("n=60 Rtsne perplexity", p, ":", if (inherits(r,"try-error")) paste("ERROR:", trimws(substr(as.character(r),1,110))) else "ran", "\n") }
# ---- Skill uwot block verbatim
set.seed(42)
um <- umap(X, n_neighbors = 30, min_dist = 0.3, metric = 'euclidean')
set.seed(42); um2 <- umap(X, n_neighbors = 30, min_dist = 0.3, metric = 'euclidean')
cat("uwot dim:", dim(um), " set.seed(42) twice identical:", identical(um, um2), " max|diff|:", max(abs(um-um2)), "\n")
set.seed(42); um3 <- umap(X, n_neighbors=30, min_dist=0.3, n_threads=1, n_sgd_threads=1); set.seed(42); um4 <- umap(X, n_neighbors=30, min_dist=0.3, n_threads=1, n_sgd_threads=1)
cat("uwot n_threads=1,n_sgd_threads=1 twice identical:", identical(um3, um4), "\n")
r <- try(umap(X, n_neighbors=30, min_dist=0.3, seed=42), silent=TRUE); cat("uwot::umap(seed=42):", if (inherits(r,"try-error")) paste("ERROR", trimws(substr(as.character(r),1,140))) else "no error", "\n")
# quality: kNN purity wrt planted labels
knn_pur <- function(E, lab, k=15){ d <- as.matrix(dist(E)); diag(d) <- Inf; mean(sapply(seq_len(nrow(E)), function(i) mean(lab[order(d[i,])[1:k]] == lab[i]))) }
cat("kNN purity Rtsne:", round(knn_pur(ts$Y, lab),3), " uwot:", round(knn_pur(um, lab),3), "\n")
png("F:/OpenScience/audits/bio-data-visualization-dimensionality-reduction-plots/figs/i4b_r_embeddings.png", 900, 450)
par(mfrow=c(1,2)); cols <- c("#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00")
plot(ts$Y, col=cols[lab+1], pch=19, cex=.4, xlab="t-SNE 1", ylab="t-SNE 2", main="Rtsne"); plot(um, col=cols[lab+1], pch=19, cex=.4, xlab="UMAP1", ylab="UMAP2", main="uwot"); dev.off()
