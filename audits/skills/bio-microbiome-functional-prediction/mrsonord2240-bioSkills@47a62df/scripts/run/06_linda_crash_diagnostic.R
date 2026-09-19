# Diagnostic: why does MicrobiomeStat::linda() crash on gut vs left palm predicted-pathway
# data with "contrasts can be applied only to factors with 2 or more levels", when the same
# code pattern worked (mechanically, if uninformatively) on left palm vs right palm?
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressMessages(library(MicrobiomeStat))

setwd("F:/OpenScience/audits/bio-microbiome-functional-prediction/work")
paths <- read.delim(gzfile("picrust2_out_reaudit/pathways_out/path_abun_unstrat.tsv.gz"),
                     row.names = 1, check.names = FALSE)
meta <- read.delim("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/public-data/moving-pictures/sample_metadata.tsv")
meta <- meta[-1, ]
colnames(meta)[1] <- "sample_id"
rownames(meta) <- meta$sample_id
samples_in_table <- colnames(paths)
meta_sub <- meta[samples_in_table, ]
groups <- meta_sub$body.site
keep <- groups %in% c("gut", "left palm")
paths_sub <- as.matrix(paths[, keep])
storage.mode(paths_sub) <- "numeric"
groups_sub <- factor(groups[keep])

feature_df <- as.data.frame(paths_sub)
meta_df <- data.frame(body_site = as.character(groups_sub), row.names = colnames(paths_sub))
cat("class(meta_df$body_site):", class(meta_df$body_site), "\n")
cat("table(meta_df$body_site):\n"); print(table(meta_df$body_site))
cat("any NA in feature_df:", any(is.na(feature_df)), "\n")
cat("any row all-zero:", any(rowSums(feature_df) == 0), "\n")
cat("any row with <2 nonzero values:", sum(rowSums(feature_df > 0) < 2), "of", nrow(feature_df), "rows\n")

# Try explicit factor
meta_df2 <- meta_df
meta_df2$body_site <- factor(meta_df2$body_site)
cat("\nRetry with explicit factor() on body_site:\n")
r2 <- tryCatch({
  fit <- linda(feature.dat = feature_df, meta.dat = meta_df2, formula = "~body_site",
               feature.dat.type = "proportion", prev.filter = 0.0)
  "OK"
}, error = function(e) paste("STILL CRASHES:", conditionMessage(e)))
cat(r2, "\n")

# Try with prev.filter > 0 (drop the near-all-zero rows that triggered the 17 warnings)
cat("\nRetry with prev.filter = 0.1 (drop near-all-zero features):\n")
r3 <- tryCatch({
  fit <- linda(feature.dat = feature_df, meta.dat = meta_df, formula = "~body_site",
               feature.dat.type = "proportion", prev.filter = 0.1)
  paste("OK -- output rows:", nrow(fit$output[[1]]))
}, error = function(e) paste("STILL CRASHES:", conditionMessage(e)))
cat(r3, "\n")
