# Build SYNTHETIC DE data with genes planted in real KEGG pathways, so enrichment can be checked
# against ground truth. All values below are synthetic/fabricated; only the gene membership (which
# genes belong to which real KEGG pathway) is real, queried live from rest.kegg.jp.
suppressMessages(library(org.Hs.eg.db))
suppressMessages(library(clusterProfiler))

set.seed(42)

# --- 1. Real KEGG pathway gene membership (live REST call, light: 2 pathways) ---
get_pathway_genes <- function(pid) {
  url <- paste0("https://rest.kegg.jp/link/hsa/", pid)
  txt <- readLines(url, warn = FALSE)
  entrez <- sub(".*hsa:", "", sapply(strsplit(txt, "\t"), `[`, 2))
  unique(entrez)
}

up_pathway   <- "hsa04110"  # Cell cycle -- planted UP
down_pathway <- "hsa04910"  # Insulin signaling pathway -- planted DOWN
up_entrez_all   <- get_pathway_genes(up_pathway)
down_entrez_all <- get_pathway_genes(down_pathway)
cat("Cell cycle (hsa04110) genes:", length(up_entrez_all), "\n")
cat("Insulin signaling (hsa04910) genes:", length(down_entrez_all), "\n")

# drop overlap so the two planted sets are disjoint
overlap <- intersect(up_entrez_all, down_entrez_all)
up_entrez_all   <- setdiff(up_entrez_all, overlap)
down_entrez_all <- setdiff(down_entrez_all, overlap)

# --- 2. Background universe: random human Entrez genes (org.Hs.eg.db), excluding planted sets ---
all_entrez <- keys(org.Hs.eg.db, keytype = "ENTREZID")
background <- setdiff(all_entrez, union(up_entrez_all, down_entrez_all))
bg_sample  <- sample(background, 3000)

# --- 3. Assemble synthetic DE table (mimics a DESeq2 results data.frame) ---
n_up   <- length(up_entrez_all)
n_down <- length(down_entrez_all)
n_bg   <- length(bg_sample)

entrez_col <- c(up_entrez_all, down_entrez_all, bg_sample)
log2fc     <- c(rnorm(n_up,   mean =  3.0, sd = 0.6),
                 rnorm(n_down, mean = -3.0, sd = 0.6),
                 rnorm(n_bg,   mean =  0.0, sd = 0.5))
pval       <- c(runif(n_up,   min = 1e-8, max = 1e-3),
                 runif(n_down, min = 1e-8, max = 1e-3),
                 runif(n_bg,   min = 0.05, max = 0.99))
padj       <- p.adjust(pval, method = "BH")

symbol_map <- suppressMessages(bitr(entrez_col, fromType = "ENTREZID", toType = "SYMBOL", OrgDb = org.Hs.eg.db))
df <- data.frame(entrez = entrez_col, log2FoldChange = log2fc, pvalue = pval, padj = padj)
df <- merge(df, symbol_map, by.x = "entrez", by.y = "ENTREZID")
names(df)[names(df) == "SYMBOL"] <- "gene"
df <- df[, c("gene", "entrez", "log2FoldChange", "pvalue", "padj")]
df <- df[!duplicated(df$gene), ]

write.csv(df, "SYNTHETIC_de_results.csv", row.names = FALSE)
writeLines(up_entrez_all,   "planted_up_hsa04110_entrez.txt")
writeLines(down_entrez_all, "planted_down_hsa04910_entrez.txt")
cat("Wrote", nrow(df), "rows. sig up:", sum(df$padj<0.05 & df$log2FoldChange>1),
    "sig down:", sum(df$padj<0.05 & df$log2FoldChange < -1), "\n")

# --- 4. Prokaryotic synthetic data: E. coli glycolysis (eco00010), real locus tags ---
eco_url <- "https://rest.kegg.jp/link/eco/eco00010"
eco_txt <- readLines(eco_url, warn = FALSE)
eco_locus <- unique(sub(".*eco:", "", sapply(strsplit(eco_txt, "\t"), `[`, 2)))
cat("E. coli glycolysis (eco00010) genes:", length(eco_locus), "\n")

# universe: fetch full eco gene list (locus tags) from KEGG, light call
eco_all_url <- "https://rest.kegg.jp/list/eco"
eco_all_txt <- readLines(eco_all_url, warn = FALSE)
eco_all_locus <- unique(sub("eco:", "", sapply(strsplit(eco_all_txt, "\t"), `[`, 1)))
cat("Total eco genome genes:", length(eco_all_locus), "\n")
eco_bg <- sample(setdiff(eco_all_locus, eco_locus), 1500)

eco_log2fc <- c(rnorm(length(eco_locus), mean = 2.5, sd = 0.5), rnorm(length(eco_bg), mean = 0, sd = 0.4))
eco_pval   <- c(runif(length(eco_locus), 1e-8, 1e-3), runif(length(eco_bg), 0.05, 0.99))
eco_padj   <- p.adjust(eco_pval, method = "BH")
eco_df <- data.frame(locus_tag = c(eco_locus, eco_bg), log2FoldChange = eco_log2fc, pvalue = eco_pval, padj = eco_padj)
write.csv(eco_df, "SYNTHETIC_eco_de_results.csv", row.names = FALSE)
cat("Wrote", nrow(eco_df), "eco rows. sig:", sum(eco_df$padj<0.05 & eco_df$log2FoldChange>1), "\n")
