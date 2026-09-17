# Input 5 (Stress, regression -- load-bearing CAMERA claim) -- prompt:
# "My HALLMARK_INTERFERON_GAMMA_RESPONSE genes look co-regulated in the logCPM matrix and I want a
# competitive test that will not be fooled by that correlation. Run CAMERA the way the Skill
# documents it, and also run it the naive/bare way people usually copy from old tutorials, so I
# can see whether it actually matters. Also give me Reactome GSEA offline as a second database."

suppressMessages({
  library(limma)
  library(clusterProfiler)
  library(org.Hs.eg.db)
  library(ReactomePA)
})

expr <- read.csv("F:/OpenScience/audits/bio-pathway-gsea/data/SYNTHETIC_logcpm_matrix.csv", row.names = 1)
mat <- as.matrix(expr)
meta <- read.csv("F:/OpenScience/audits/bio-pathway-gsea/data/SYNTHETIC_sample_metadata.csv")
meta$group <- factor(meta$group, levels = c("control", "treated"))
design <- model.matrix(~ group, data = meta)

corr_genes <- readLines("F:/OpenScience/audits/bio-pathway-gsea/data/planted_corr_entrez.txt")
idx <- rownames(mat) %in% corr_genes
measured_cor <- mean(cor(t(mat[idx, ]))[upper.tri(diag(sum(idx)))])
cat("measured inter-gene correlation inside the planted correlated set:", round(measured_cor, 4), "\n")

idx_list <- list(HALLMARK_INTERFERON_GAMMA_RESPONSE = which(idx))

cat("\n--- CAMERA as the CURRENT SKILL.md documents it: limma::camera(..., inter.gene.cor = NA) ---\n")
cam_fixed <- camera(mat, idx_list, design, contrast = 2, inter.gene.cor = NA)
print(cam_fixed)

cat("\n--- CAMERA the naive/bare way (no inter.gene.cor argument -- what pre-fix SKILL.md wrote) ---\n")
cam_bare <- camera(mat, idx_list, design, contrast = 2)
print(cam_bare)

cat("\nColumns returned -- bare call has Correlation:", "Correlation" %in% colnames(cam_bare),
    "| inter.gene.cor=NA call has Correlation:", "Correlation" %in% colnames(cam_fixed), "\n")
cat("bare-call PValue:", signif(cam_bare$PValue[1], 3), " | inter.gene.cor=NA PValue:", signif(cam_fixed$PValue[1], 3), "\n")
cat("PValue ratio (bare / corrected):", signif(cam_bare$PValue[1] / cam_fixed$PValue[1], 3), "\n")

cat("\n--- gene-permutation preranked GSEA on the same contrast, for comparison ---\n")
library(msigdbr)
# derive a per-gene t-stat from this design via limma for a preranked comparison
fit <- lmFit(mat, design)
fit <- eBayes(fit)
tstat <- fit$t[, 2]
gl <- sort(tstat, decreasing = TRUE)
h <- msigdbr(species = "Homo sapiens", collection = "H")
t2g <- h[h$gs_name == "HALLMARK_INTERFERON_GAMMA_RESPONSE", c("gs_name", "ncbi_gene")]
set.seed(123)
gse <- GSEA(geneList = gl, TERM2GENE = t2g, exponent = 1, minGSSize = 10, maxGSSize = 500,
            eps = 0, pvalueCutoff = 1, seed = TRUE, verbose = FALSE)
res <- as.data.frame(gse)
cat("preranked gene-permutation FDR for the correlated set:", if (nrow(res) > 0) signif(res$p.adjust[1], 3) else "not returned (p too high)", "\n")

cat("\n--- gsePathway (ReactomePA, offline from local reactome.db) ---\n")
set.seed(123)
gse_re <- gsePathway(gl, organism = "human", minGSSize = 10, maxGSSize = 500,
                      eps = 0, pvalueCutoff = 0.05, pAdjustMethod = "BH",
                      seed = TRUE, verbose = FALSE)
res_re <- as.data.frame(gse_re)
cat("significant Reactome pathways:", nrow(res_re), "| pos", sum(res_re$NES>0), "| neg", sum(res_re$NES<0), "\n")
print(head(res_re[order(res_re$p.adjust), c("Description","NES","p.adjust")], 5))

write.csv(data.frame(call = c("inter.gene.cor=NA (fixed)", "bare/default (pre-fix)"),
                      PValue = c(cam_fixed$PValue[1], cam_bare$PValue[1]),
                      has_Correlation_col = c("Correlation" %in% colnames(cam_fixed), "Correlation" %in% colnames(cam_bare))),
          "F:/OpenScience/audits/bio-pathway-gsea/run/in5_camera_comparison.csv", row.names = FALSE)
cat("\nDONE\n")
