# Input 4 (Variant B, regression) -- prompt:
# "Convert my expression matrix into a per-sample pathway-activity matrix with GSVA so I can
# cluster samples and correlate scores with treatment group."
# SKILL.md "Per-Sample Scores" block, verbatim.

suppressMessages(library(GSVA))
suppressMessages(library(msigdbr))

expr <- read.csv("F:/OpenScience/audits/bio-pathway-gsea/data/SYNTHETIC_logcpm_matrix.csv", row.names = 1)
expr_matrix <- as.matrix(expr)
meta <- read.csv("F:/OpenScience/audits/bio-pathway-gsea/data/SYNTHETIC_sample_metadata.csv")

h <- msigdbr(species = "Homo sapiens", collection = "H")
gene_sets <- split(as.character(h$ncbi_gene), h$gs_name)

cat("GSVA installed version:", as.character(packageVersion("GSVA")), "\n")
cat("SYNTHETIC logCPM matrix:", nrow(expr_matrix), "genes x", ncol(expr_matrix), "samples\n")

gsva_scores  <- gsva(gsvaParam(expr_matrix, gene_sets))
ssgsea_scores <- gsva(ssgseaParam(expr_matrix, gene_sets))
cat("gsva_scores  :", nrow(gsva_scores), "sets x", ncol(gsva_scores), "samples | class", class(gsva_scores)[1], "\n")
cat("ssgsea_scores:", nrow(ssgsea_scores), "sets x", ncol(ssgsea_scores), "samples\n")

# claim check: pre-1.50 signature is defunct
old_sig <- tryCatch({ gsva(expr_matrix, gene_sets, method = "ssgsea"); "no error" },
                     error = function(e) conditionMessage(e))
cat("\n[claim check] old signature:", old_sig, "\n")

# planted set: HALLMARK_INTERFERON_GAMMA_RESPONSE, down in 'treated'
set_name <- "HALLMARK_INTERFERON_GAMMA_RESPONSE"
ctrl <- meta$sample[meta$group == "control"]
trt  <- meta$sample[meta$group == "treated"]
cat("\n", set_name, "\n")
cat("  GSVA   control", round(mean(gsva_scores[set_name, ctrl]),3),
    "| treated", round(mean(gsva_scores[set_name, trt]),3),
    "| delta", round(mean(gsva_scores[set_name, trt]) - mean(gsva_scores[set_name, ctrl]),3), "\n")
cat("  ssGSEA control", round(mean(ssgsea_scores[set_name, ctrl]),3),
    "| treated", round(mean(ssgsea_scores[set_name, trt]),3),
    "| delta", round(mean(ssgsea_scores[set_name, trt]) - mean(ssgsea_scores[set_name, ctrl]),3), "\n")

# hierarchical clustering check
hc <- hclust(dist(t(gsva_scores)))
cut <- cutree(hc, k = 2)
tab <- table(cut, meta$group[match(names(cut), meta$sample)])
cat("\nhierarchical clustering on GSVA scores, 2-group cut vs truth:\n")
print(tab)

write.csv(gsva_scores, "F:/OpenScience/audits/bio-pathway-gsea/run/in4_gsva_scores.csv")
write.csv(ssgsea_scores, "F:/OpenScience/audits/bio-pathway-gsea/run/in4_ssgsea_scores.csv")
cat("\nDONE\n")
