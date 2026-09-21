# Input 2: SKILL.md R block (PCAtools) on the REAL airway dataset; independent prcomp check
suppressPackageStartupMessages({library(DESeq2); library(PCAtools); library(ggplot2); library(airway)})
figs <- "F:/OpenScience/audits/bio-data-visualization-dimensionality-reduction-plots/figs"
data(airway)
dds <- DESeqDataSet(airway, design = ~ cell + dex)
dds <- dds[rowSums(counts(dds)) > 10, ]
vsd <- vst(dds, blind = FALSE)
cat("packageVersion PCAtools:", as.character(packageVersion("PCAtools")), "\n")
# ---- SKILL block, as written (colby='condition', shape='batch' -> airway has dex / cell; a researcher must rename)
r <- try(pca(assay(vsd), metadata = as.data.frame(colData(dds))), silent=TRUE)
p <- r
cat("pca() ok; class:", class(p), " variance[1:3]:", round(p$variance[1:3], 2), "\n")
# independent
pr <- prcomp(t(assay(vsd)), center = TRUE, scale. = FALSE)
truth <- 100 * pr$sdev^2 / sum(pr$sdev^2)
cat("prcomp %var[1:3]:", round(truth[1:3], 2), "\n")
stopifnot(all.equal(unname(p$variance[1:8]), truth[1:8], tolerance = 1e-6))
cat("ASSERT PASS: p$variance is PERCENT (0-100) and equals prcomp for PC1-8\n")
# sign check
cat("sign PC1 agree (or flipped):", cor(p$rotated[,1], pr$x[,1]), "\n")
# biplot with the Skill's arguments; use dex/cell in place of condition/batch
b1 <- try(biplot(p, colby = 'dex', shape = 'cell', lab = NULL, hline = 0, vline = 0, legendPosition = 'right',
       title = paste0('PCA: PC1 (', round(p$variance[1], 1), '%) vs PC2 (', round(p$variance[2], 1), '%)')), silent=TRUE)
if (inherits(b1, "try-error")) cat("biplot ERROR:", as.character(b1), "\n") else { ggsave(file.path(figs,"i2_biplot.png"), b1, width=6, height=5, dpi=100); cat("biplot ok\n") }
# Skill's literal metadata column names
b0 <- try(biplot(p, colby = 'condition', shape = 'batch', lab = NULL), silent=TRUE)
cat("biplot with colby='condition' (column absent in airway):", if (inherits(b0,"try-error")) paste("ERROR:", substr(as.character(b0),1,150)) else "ok", "\n")
# screeplot / plotloadings exactly as in Skill
s1 <- try(screeplot(p, components = 1:10), silent=TRUE)
cat("screeplot(components = 1:10):", if (inherits(s1,"try-error")) paste("ERROR:", substr(as.character(s1),1,200)) else "ok", "\n")
l1 <- try(plotloadings(p, components = 1, rangeRetain = 0.05), silent=TRUE)
cat("plotloadings(components = 1, rangeRetain = 0.05):", if (inherits(l1,"try-error")) paste("ERROR:", substr(as.character(l1),1,200)) else "ok", "\n")
# corrected forms
s2 <- try(screeplot(p, components = getComponents(p, 1:10)), silent=TRUE)
l2 <- try(plotloadings(p, components = getComponents(p, 1), rangeRetain = 0.05), silent=TRUE)
cat("corrected screeplot ok:", !inherits(s2,"try-error"), " corrected plotloadings ok:", !inherits(l2,"try-error"), "\n")
if (!inherits(s2,"try-error")) ggsave(file.path(figs,"i2_scree.png"), s2, width=6, height=4, dpi=100)
if (!inherits(l2,"try-error")) ggsave(file.path(figs,"i2_loadings.png"), l2, width=6, height=5, dpi=100)
# biplot showLoadings (Skill prompt "Show loadings as arrows" -- Skill gives no code for this)
b2 <- try(biplot(p, colby='dex', lab=NULL, showLoadings=TRUE, ntopLoadings=5), silent=TRUE)
cat("biplot(showLoadings=TRUE) ok:", !inherits(b2,"try-error"), "\n")
if (!inherits(b2,"try-error")) ggsave(file.path(figs,"i2_biplot_loadings.png"), b2, width=6, height=5, dpi=100)
# colour mapping: dex groups in biplot data
d <- b1$data; cat("biplot data cols:", paste(head(colnames(d),6), collapse=","), "\n")
cat("dex counts per colour group:", paste(names(table(d$dex)), table(d$dex), collapse="; "), "\n")
# PC separation: dex effect and cell effect (real biology: cell line dominates PC1/2, dex on PC3 in airway)
for (i in 1:4) { pc <- p$rotated[,i]; cat(sprintf("PC%d  R2 dex=%.2f  R2 cell=%.2f\n", i, summary(lm(pc ~ colData(dds)$dex))$r.squared, summary(lm(pc ~ colData(dds)$cell))$r.squared)) }
# PCA without scaling claim: raw counts
pr_raw <- prcomp(t(counts(dds)), center=TRUE, scale.=FALSE)
cat("raw counts (no vst) PC1 %var:", round(100*pr_raw$sdev[1]^2/sum(pr_raw$sdev^2),1), " top-gene share of PC1 loading^2 (top 10 genes):", round(sum(sort(pr_raw$rotation[,1]^2, decreasing=TRUE)[1:10]),2), "\n")
