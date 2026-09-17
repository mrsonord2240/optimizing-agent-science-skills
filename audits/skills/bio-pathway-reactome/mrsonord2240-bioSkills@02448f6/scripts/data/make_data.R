# Synthetic data generator for the bio-pathway-reactome audit.
# Real gene symbols and real Reactome pathway membership (both queried from installed
# Bioconductor annotation packages); the "experiment" (which genes are "significant",
# the fold-change/statistic values) is FABRICATED/SYNTHETIC for this audit only.
suppressMessages({
  library(reactome.db)
  library(org.Hs.eg.db)
  library(clusterProfiler)
})

set.seed(42)

# Planted pathway: "Interferon gamma signaling" (R-HSA-877300) -- mid-sized, well-known.
planted_id <- "R-HSA-877300"
planted_name_guess <- tryCatch(
  as.character(AnnotationDbi::select(reactome.db, keys = planted_id,
                                      columns = "PATHNAME", keytype = "PATHID")$PATHNAME),
  error = function(e) NA
)
cat("Planted pathway id:", planted_id, "\n")
cat("Planted pathway name (raw PATHNAME):", planted_name_guess, "\n")

planted_entrez <- AnnotationDbi::select(reactome.db, keys = planted_id,
                                         columns = "ENTREZID", keytype = "PATHID")$ENTREZID
planted_entrez <- unique(na.omit(planted_entrez))
cat("Planted pathway genes (Entrez):", length(planted_entrez), "\n")

planted_symbols <- AnnotationDbi::select(org.Hs.eg.db, keys = planted_entrez,
                                          columns = "SYMBOL", keytype = "ENTREZID")$SYMBOL
planted_symbols <- unique(na.omit(planted_symbols))
cat("Planted pathway genes (Symbol):", length(planted_symbols), "\n")

# Background universe: a random sample of ~3000 protein-coding genes that map to Entrez,
# guaranteed to include the planted genes plus random noise genes.
all_symbols <- keys(org.Hs.eg.db, keytype = "SYMBOL")
noise_pool <- setdiff(all_symbols, planted_symbols)
noise_bg <- sample(noise_pool, 3000 - length(planted_symbols))
background_symbols <- unique(c(planted_symbols, noise_bg))
cat("Background universe size:", length(background_symbols), "\n")

# Significant gene list: ~85% of the planted pathway genes (simulate incomplete detection)
# plus a small number of random noise "significant" genes (simulate imperfect specificity).
sig_planted <- sample(planted_symbols, size = round(0.85 * length(planted_symbols)))
sig_noise <- sample(setdiff(background_symbols, planted_symbols), 15)
sig_symbols <- unique(c(sig_planted, sig_noise))
cat("Significant gene list size:", length(sig_symbols), "\n")

write.csv(data.frame(SYMBOL = sig_symbols), "significant_genes.csv", row.names = FALSE)
write.csv(data.frame(SYMBOL = background_symbols), "background_genes.csv", row.names = FALSE)

# Ranked vector for GSEA: every background gene gets a statistic; planted-pathway genes get
# a positive shift (mean +1.5) so the planted pathway should surface at the top of GSEA too.
stat <- rnorm(length(background_symbols), mean = 0, sd = 1)
names(stat) <- background_symbols
is_planted <- background_symbols %in% planted_symbols
stat[is_planted] <- stat[is_planted] + 1.5
ranked_df <- data.frame(SYMBOL = names(stat), stat = as.numeric(stat))
ranked_df <- ranked_df[order(-ranked_df$stat), ]
write.csv(ranked_df, "ranked_genes.csv", row.names = FALSE)

cat("Wrote significant_genes.csv, background_genes.csv, ranked_genes.csv\n")
