# SYNTHETIC input (planted structure) supplied for heatmap_phd.R, which assumes mat/metadata/gene_info exist.
set.seed(7)
ng <- 120; ns <- 24
mat <- matrix(rnorm(ng*ns, 6, 0.4), ng)
grp <- rep(c("Control","Treatment"), each = 12)
mat[1:40, grp=="Treatment"]  <- mat[1:40, grp=="Treatment"] + 1.5     # up in Treatment
mat[41:80, grp=="Treatment"] <- mat[41:80, grp=="Treatment"] - 1.2    # down in Treatment
rownames(mat) <- paste0("G", 1:ng); colnames(mat) <- paste0("S", 1:ns)
metadata <- data.frame(condition = grp, batch = rep(c("A","B","C"), 8), age = round(runif(ns, 30, 70)), row.names = colnames(mat))
gene_info <- data.frame(pathway = rep(c("Metabolism","Signaling"), length.out = ng), log2FC = c(rep(1.5,40), rep(-1.2,40), rnorm(40,0,.2)), row.names = rownames(mat))
