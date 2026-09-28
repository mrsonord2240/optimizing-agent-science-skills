# Regression input 2: fixed PCAtools recipe on the real Bioconductor airway data.
suppressPackageStartupMessages({library(DESeq2); library(PCAtools); library(ggplot2); library(airway)})
audit <- "F:/OpenScience/audits/bio-data-visualization-dimensionality-reduction-plots"
data(airway)
dds <- DESeqDataSet(airway, design = ~ cell + dex)
dds <- dds[rowSums(counts(dds)) > 10, ]
vsd <- vst(dds, blind = FALSE)
p <- PCAtools::pca(assay(vsd), metadata = as.data.frame(colData(dds)))

truth <- prcomp(t(assay(vsd)), center = TRUE, scale. = FALSE)
truth_variance <- 100 * truth$sdev^2 / sum(truth$sdev^2)
stopifnot(all.equal(unname(p$variance), truth_variance, tolerance = 1e-6))

b <- PCAtools::biplot(p, colby = "dex", shape = "cell", showLoadings = TRUE,
                      ntopLoadings = 5, lab = NULL, legendPosition = "right")
n_components <- min(10, ncol(assay(vsd)), ncol(p$rotated))
s <- PCAtools::screeplot(p, components = seq_len(n_components))
l <- PCAtools::plotloadings(p, components = 1, rangeRetain = 0.05)
ggsave(file.path(audit, "figs", "input2_airway_biplot.png"), b, width = 7, height = 5, dpi = 200)
ggsave(file.path(audit, "figs", "input2_airway_scree.png"), s, width = 6, height = 4, dpi = 200)
ggsave(file.path(audit, "figs", "input2_airway_loadings.png"), l, width = 6, height = 5, dpi = 200)

cat("PCAtools version:", as.character(packageVersion("PCAtools")), "\n")
cat("variance first three:", paste(round(p$variance[1:3], 2), collapse = ", "), "\n")
cat("independent first three:", paste(round(truth_variance[1:3], 2), collapse = ", "), "\n")
cat("dynamic scree component count:", n_components, "\n")
for (name in c("input2_airway_biplot.png", "input2_airway_scree.png", "input2_airway_loadings.png")) {
  bytes <- file.info(file.path(audit, "figs", name))$size
  cat(name, bytes, "bytes\n")
  stopifnot(bytes > 2000)
}
