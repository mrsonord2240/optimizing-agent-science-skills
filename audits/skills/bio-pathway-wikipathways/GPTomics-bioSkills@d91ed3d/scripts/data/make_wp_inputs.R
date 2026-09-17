# SYNTHETIC DATA GENERATOR for bio-pathway-wikipathways audit.
# Builds a synthetic DE results table over REAL human gene identities (org.Hs.eg.db) with a
# planted enrichment signal drawn from REAL WikiPathways pathway membership (queried live from
# WikiPathways via rWikiPathways::getXrefList). Only the differential-expression call (padj,
# log2FoldChange, up/down group assignment) is synthetic/fabricated; gene identities and pathway
# membership are real.
#
# Planted signal:
#   - WP554 "ACE inhibitor pathway" (17 genes, real WikiPathways Entrez xrefs) -> UP-regulated
#   - WP430 "Statin inhibition of cholesterol production" (31 genes, real WikiPathways Entrez
#     xrefs) -> DOWN-regulated
# Background: ~3000 additional real human Entrez/SYMBOL pairs sampled from org.Hs.eg.db, values
# drawn from a null-ish distribution (small noise, mostly non-significant).

suppressMessages({
  library(rWikiPathways)
  library(org.Hs.eg.db)
  library(AnnotationDbi)
})

set.seed(42)

wp_up   <- getXrefList('WP554', 'L')   # ACE inhibitor pathway
wp_down <- getXrefList('WP430', 'L')   # Statin inhibition of cholesterol production
cat("WP554 (up-planted) genes:", length(wp_up), "\n")
cat("WP430 (down-planted) genes:", length(wp_down), "\n")
stopifnot(length(wp_up) > 0, length(wp_down) > 0)

all_ids <- keys(org.Hs.eg.db, keytype = "ENTREZID")
bg_pool <- setdiff(all_ids, union(wp_up, wp_down))
bg_sample <- sample(bg_pool, 3000)

entrez_all <- unique(c(wp_up, wp_down, bg_sample))
sym_map <- suppressWarnings(AnnotationDbi::select(org.Hs.eg.db, keys = entrez_all,
                                                   keytype = "ENTREZID", columns = "SYMBOL"))
sym_map <- sym_map[!is.na(sym_map$SYMBOL) & !duplicated(sym_map$ENTREZID), ]
cat("Entrez with a resolvable SYMBOL:", nrow(sym_map), "/", length(entrez_all), "\n")

n <- nrow(sym_map)
log2FC <- rnorm(n, mean = 0, sd = 0.4)
padj   <- runif(n, min = 0.1, max = 1)

is_up   <- sym_map$ENTREZID %in% wp_up
is_down <- sym_map$ENTREZID %in% wp_down

log2FC[is_up]   <- runif(sum(is_up), 2, 4)
padj[is_up]     <- runif(sum(is_up), 1e-6, 1e-3)
log2FC[is_down] <- runif(sum(is_down), -4, -2)
padj[is_down]   <- runif(sum(is_down), 1e-6, 1e-3)

# a small number of background genes cross the significance threshold by chance, as real data would
noise_hits <- sample(which(!is_up & !is_down), 15)
padj[noise_hits] <- runif(15, 0.001, 0.049)
log2FC[noise_hits] <- sample(c(-1, 1), 15, replace = TRUE) * runif(15, 1.1, 1.8)

de_results <- data.frame(
  gene_symbol    = sym_map$SYMBOL,
  entrez         = sym_map$ENTREZID,
  log2FoldChange = round(log2FC, 4),
  padj           = signif(padj, 4),
  planted_group  = ifelse(is_up, "WP554_up", ifelse(is_down, "WP430_down", "background")),
  stringsAsFactors = FALSE
)
de_results <- de_results[sample(nrow(de_results)), ]  # shuffle row order

out_path <- "de_results_synthetic.csv"
write.csv(de_results, out_path, row.names = FALSE)
cat("Wrote", nrow(de_results), "rows to", out_path, "\n")
cat("Significant (padj<0.05 & |log2FC|>1):", sum(de_results$padj < 0.05 & abs(de_results$log2FoldChange) > 1), "\n")
cat("  of which planted WP554 up:", sum(de_results$planted_group == "WP554_up" & de_results$padj < 0.05 & abs(de_results$log2FoldChange) > 1), "/", sum(de_results$planted_group=="WP554_up"), "\n")
cat("  of which planted WP430 down:", sum(de_results$planted_group == "WP430_down" & de_results$padj < 0.05 & abs(de_results$log2FoldChange) > 1), "/", sum(de_results$planted_group=="WP430_down"), "\n")
