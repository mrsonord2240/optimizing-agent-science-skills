# Synthetic data generator for the bio-pathway-gsea re-audit (post-fix).
# Independent of the pre-fix audit's data: different planted gene sets, different seed structure.
# Every DE statistic / p-value / expression count below is SYNTHETIC. Gene identities and gene-set
# membership are real (org.Hs.eg.db 3.20.0, msigdbr 26.1.1).

suppressMessages({
  library(org.Hs.eg.db)
  library(msigdbr)
})

set.seed(4471)

out_dir <- "F:/OpenScience/audits/bio-pathway-gsea/data"

h <- msigdbr(species = "Homo sapiens", collection = "H")

up_set   <- "HALLMARK_TNFA_SIGNALING_VIA_NFKB"
down_set <- "HALLMARK_G2M_CHECKPOINT"
corr_set <- "HALLMARK_INTERFERON_GAMMA_RESPONSE"   # used only in the logCPM/CAMERA matrix

up_genes   <- unique(as.character(h$ncbi_gene[h$gs_name == up_set]))
down_genes <- unique(as.character(h$ncbi_gene[h$gs_name == down_set]))
corr_genes_full <- unique(as.character(h$ncbi_gene[h$gs_name == corr_set]))

# ---- universe: 14,000 real Entrez IDs, guaranteed to contain the full planted sets ----
all_ids <- keys(org.Hs.eg.db, keytype = "ENTREZID")
core <- unique(c(up_genes, down_genes, corr_genes_full))
background <- sample(setdiff(all_ids, core), 14000 - length(core))
entrez_ids <- unique(c(core, background))
cat("planted UP  (", up_set, "):", length(up_genes), "genes\n")
cat("planted DOWN(", down_set, "):", length(down_genes), "genes\n")

sym2entrez <- AnnotationDbi::select(org.Hs.eg.db, keys = entrez_ids, keytype = "ENTREZID",
                                     columns = "SYMBOL")

# ---- 1. DESeq2-style table (Input 1: canonical) ----
stat <- rnorm(length(entrez_ids), mean = 0, sd = 1)
names(stat) <- entrez_ids
stat[up_genes]   <- stat[up_genes]   + rnorm(length(up_genes),   mean = 1.15, sd = 1)
stat[down_genes] <- stat[down_genes] - rnorm(length(down_genes), mean = 1.15, sd = 1)

pvalue <- 2 * pnorm(-abs(stat))
# plant a handful of exact-zero p-values (double precision underflow), same mechanism the fix
# targets, but on genes NOT already in the planted sets so the clamp-distortion test is clean
zero_p_genes <- sample(setdiff(entrez_ids, c(up_genes, down_genes)), 5)
pvalue[zero_p_genes] <- 0
stat[zero_p_genes] <- sign(rnorm(5)) * 2   # modest, non-extreme true effect

log2fc <- stat / 4 + rnorm(length(entrez_ids), 0, 0.3)
basemean <- round(exp(rnorm(length(entrez_ids), mean = 6, sd = 2)), 1)
basemean[basemean < 1] <- 1

deseq2 <- data.frame(entrez_id = entrez_ids, baseMean = basemean, log2FoldChange = log2fc,
                      stat = stat, pvalue = pvalue,
                      padj = p.adjust(pvalue, method = "BH"))
write.csv(deseq2, file.path(out_dir, "SYNTHETIC_deseq2_results.csv"), row.names = FALSE)

# ---- 2. edgeR-style messy table (Input 3: edge) ----
# SYMBOL-keyed, unsorted, ~250 duplicate rows, no signed statistic column, 4 exact-zero PValues
symtab <- sym2entrez[!is.na(sym2entrez$SYMBOL) & !duplicated(sym2entrez$ENTREZID), ]
symtab <- symtab[match(entrez_ids, symtab$ENTREZID), ]
symtab <- symtab[!is.na(symtab$SYMBOL), ]

edger <- data.frame(gene = symtab$SYMBOL, logFC = log2fc[symtab$ENTREZID],
                     PValue = pvalue[symtab$ENTREZID])
dup_rows <- edger[sample(seq_len(nrow(edger)), 250), ]
edger <- rbind(edger, dup_rows)
edger <- edger[sample(seq_len(nrow(edger))), ]          # unsorted
zero_syms <- symtab$SYMBOL[match(zero_p_genes, symtab$ENTREZID)]
zero_syms <- zero_syms[!is.na(zero_syms)]
edger$PValue[edger$gene %in% zero_syms] <- 0
write.csv(edger, file.path(out_dir, "SYNTHETIC_edger_qlf.csv"), row.names = FALSE)

# ---- 3. logCPM matrix with a genuinely correlated block (Input 5: CAMERA) ----
n_genes_mat <- 5200
corr_genes <- corr_genes_full
mat_genes <- unique(c(corr_genes, sample(setdiff(entrez_ids, corr_genes), n_genes_mat - length(corr_genes))))
n_samples <- 24
group <- rep(c("control", "treated"), each = n_samples / 2)

baseline <- matrix(rnorm(n_genes_mat * n_samples, mean = 6, sd = 1.2),
                    nrow = n_genes_mat, dimnames = list(mat_genes, paste0("S", seq_len(n_samples))))
# shared latent factor loaded onto corr_genes only -> genuine inter-gene correlation inside that set
latent <- rnorm(n_samples, 0, 1)
for (g in corr_genes) baseline[g, ] <- baseline[g, ] + 0.9 * latent
# treatment effect on the corr_set (down in treated) so it is also DE, not just correlated
trt_idx <- which(group == "treated")
baseline[corr_genes, trt_idx] <- baseline[corr_genes, trt_idx] - 1.0

logcpm <- as.data.frame(baseline)
logcpm <- cbind(entrez_id = rownames(logcpm), logcpm)
write.csv(logcpm, file.path(out_dir, "SYNTHETIC_logcpm_matrix.csv"), row.names = FALSE)
write.csv(data.frame(sample = paste0("S", seq_len(n_samples)), group = group),
          file.path(out_dir, "SYNTHETIC_sample_metadata.csv"), row.names = FALSE)

# ---- save planted-gene manifests for the run scripts to check against ----
writeLines(as.character(up_genes),   file.path(out_dir, "planted_up_entrez.txt"))
writeLines(as.character(down_genes), file.path(out_dir, "planted_down_entrez.txt"))
writeLines(as.character(corr_genes), file.path(out_dir, "planted_corr_entrez.txt"))
writeLines(as.character(zero_p_genes), file.path(out_dir, "zero_p_entrez.txt"))

cat("\nsummary:\n")
cat("  deseq2 table:", nrow(deseq2), "rows,", sum(deseq2$pvalue == 0), "exact-zero p-values\n")
cat("  edgeR table :", nrow(edger), "rows,", sum(duplicated(edger$gene)), "duplicate gene names,",
    "sorted:", !is.unsorted(-match(edger$gene, edger$gene)), "\n")
cat("  logCPM matrix:", nrow(logcpm), "genes x", n_samples, "samples,",
    length(corr_genes), "genes in the planted-correlation set\n")
cat("done.\n")
