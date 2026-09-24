# Shared synthetic dataset: 24 samples (12 Case / 12 Control), ~8k human symbols, planted pathway signals.
suppressMessages({library(msigdbr)})
set.seed(20260921)
T <- "F:/OpenScience/comparisons/_theirs/"
D <- "F:/OpenScience/comparisons/gsva-vs-gsea/data/"
kegg <- msigdbr(species="Homo sapiens", collection="C2", subcollection="CP:KEGG_LEGACY")
reac <- msigdbr(species="Homo sapiens", collection="C2", subcollection="CP:REACTOME")
hall <- msigdbr(species="Homo sapiens", collection="H")
ic <- read.csv(paste0(T,"ssgsea-immune-infiltration-analysis/tests/data/immune_gene_sets.csv"), check.names=FALSE)
names(ic) <- sub("^\ufeff","",names(ic))
ip <- read.csv(paste0(T,"immune-pathway-analysis/tests/data/immune_genesets.csv"), check.names=FALSE)
K <- split(kegg$gene_symbol, kegg$gs_name); K <- lapply(K, unique)
R <- split(reac$gene_symbol, reac$gs_name); R <- lapply(R, unique)
C <- split(toupper(ic$gene), ic$cell_type); C <- lapply(C, unique)
ipS <- split(ip$gene_symbol, ip$gs_name); ipS <- lapply(ipS, unique)
universe <- sort(unique(c(unlist(K), unlist(ipS), unlist(C), hall$gene_symbol)))
cat("universe genes:", length(universe), "\n")
planted <- list(
  KEGG_CELL_CYCLE = list(genes=K[["KEGG_CELL_CYCLE"]], eff=+1.2),
  KEGG_OXIDATIVE_PHOSPHORYLATION = list(genes=K[["KEGG_OXIDATIVE_PHOSPHORYLATION"]], eff=-1.0),
  REACTOME_INTERFERON_GAMMA_SIGNALING = list(genes=R[["REACTOME_INTERFERON_GAMMA_SIGNALING"]], eff=+1.2),
  `Activated CD8 T cell` = list(genes=C[["Activated CD8 T cell"]], eff=+1.2))
pg <- lapply(planted, function(p) intersect(p$genes, universe))
cat("planted set sizes in matrix:", paste(names(pg), lengths(pg), collapse="; "), "\n")
ov <- outer(names(pg), names(pg), Vectorize(function(a,b) length(intersect(pg[[a]], pg[[b]]))))
dimnames(ov) <- list(names(pg), names(pg)); print(ov)
n <- 24; grp <- rep(c("Case","Control"), each=12); samp <- sprintf("S%02d", 1:n)
mu <- rnorm(length(universe), 7, 1.5); names(mu) <- universe
sd_g <- runif(length(universe), 0.5, 1.0)
E <- matrix(rnorm(length(universe)*n, 0, 1), length(universe), n, dimnames=list(universe, samp)) * sd_g
E <- E + mu
for (nm in names(planted)) { g <- pg[[nm]]; eff <- planted[[nm]]$eff * runif(length(g), 0.5, 1.5)
  E[g, grp=="Case"] <- E[g, grp=="Case"] + eff }
# correlated NULL sets: shared latent per-sample factor, NO group effect
used <- unique(unlist(pg))
cand <- names(K)[sapply(K, function(x) { x <- intersect(x, universe); length(x)>=30 && length(x)<=120 && length(intersect(x, used))==0 })]
nullsets <- sample(cand, 20); cat("correlated null sets:", length(nullsets), "\n")
for (nm in nullsets) { g <- setdiff(intersect(K[[nm]], universe), used); lat <- rnorm(n, 0, 1); E[g,] <- E[g,] + rep(lat, each=length(g)) * 1.0 }
E <- round(E, 4)
write.csv(data.frame(gene=rownames(E), E, check.names=FALSE), paste0(D,"expr.csv"), row.names=FALSE, quote=FALSE)
write.csv(data.frame(sample=samp, group=grp), paste0(D,"group.csv"), row.names=FALSE, quote=FALSE)
write.csv(data.frame(gs_name=rep(names(K), lengths(K)), gene_symbol=unlist(K, use.names=FALSE)), paste0(D,"kegg_table.csv"), row.names=FALSE)
write.csv(data.frame(gene=unlist(K,use.names=FALSE), cell_type=rep(names(K), lengths(K))), paste0(D,"kegg_as_celltype.csv"), row.names=FALSE)
writeLines(jsonlite::toJSON(list(planted=lapply(planted, function(p) p$eff), correlated_null_sets=nullsets, n_genes=nrow(E), n_case=12, n_control=12), auto_unbox=TRUE, pretty=TRUE), paste0(D,"truth.json"))
cat("done", dim(E), "\n")
