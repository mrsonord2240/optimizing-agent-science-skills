# Runs the Skill's own bundled examples/run_crispr_cleanr.R pipeline (as fixed in the
# mrsonord2240/bioSkills fork, commit 6847328) against REAL data:
#   - Counts: CRISPRcleanR's own bundled real screen, HT-29_counts.tsv (colorectal cancer
#     line HT-29, KY library v1.0, plasmid + 3 late-timepoint replicates; 90,709 sgRNAs).
#   - Copy number: CRISPRcleanR's own bundled GDSC.geneLevCNA, real GISTIC-derived CN calls
#     for HT-29 (COSMIC ID 905939). MYC/FAM84B/POU5F1B are a real co-amplified 3-gene block
#     at chr8:~128.6-128.9Mb, CN=8 in HT-29 -- matches the Skill's own textbook claim
#     ("Colon panel | MYC ~10 copies | MYC", usage-guide.md).
# Nothing here is synthetic or planted; this is CRISPRcleanR's own canonical example dataset.

suppressMessages(library(CRISPRcleanR))

counts_file <- paste0(system.file('extdata', package = 'CRISPRcleanR'), '/HT-29_counts.tsv')
data(KY_Library_v1.0)
data(GDSC.geneLevCNA)

cat("=== STEP 1: ccr.NormfoldChanges ===\n")
norm <- ccr.NormfoldChanges(counts_file,
                             min_reads = 30,
                             EXPname   = 'HT29',
                             libraryAnnotation = KY_Library_v1.0)
cat("norm_counts dim:", dim(norm$norm_counts), "  logFCs dim:", dim(norm$logFCs), "\n")

cat("\n=== STEP 2: ccr.logFCs2chromPos ===\n")
gw_lfc <- ccr.logFCs2chromPos(norm$logFCs, KY_Library_v1.0)
cat("gw_lfc columns:", paste(colnames(gw_lfc), collapse=", "), "\n")
cat("gw_lfc rows:", nrow(gw_lfc), "\n")

cat("\n=== STEP 3: ccr.GWclean ===\n")
cleaned <- ccr.GWclean(gw_lfc, display = FALSE, label = 'HT29')
cat("cleaned$corrected_logFCs columns:", paste(colnames(cleaned$corrected_logFCs), collapse=", "), "\n")
cat("n segments:", nrow(cleaned$segments), "\n")

cat("\n=== STEP 4: ccr.correctCounts ===\n")
corrected_counts <- ccr.correctCounts('HT29',
                                       norm$norm_counts,
                                       cleaned,
                                       KY_Library_v1.0,
                                       OutDir = '/tmp/ccr_out/')
cat("corrected_counts dim:", dim(corrected_counts), "\n")

cat("\n=== STEP 5: diagnostic tail (fixed version, real columns genes/avgFC/correctedFC) ===\n")
cn_parse <- function(x) as.numeric(sapply(strsplit(as.character(x), ","), `[`, 1))
all_genes <- rownames(GDSC.geneLevCNA)
cn <- data.frame(gene = all_genes, copy_number = cn_parse(GDSC.geneLevCNA[, "905939"]))
cn <- cn[!is.na(cn$copy_number), ]

pre  <- data.frame(gene = gw_lfc$genes,                 avgFC = gw_lfc$avgFC)
post <- data.frame(gene = cleaned$corrected_logFCs$genes,
                    avgFC = cleaned$corrected_logFCs$correctedFC)

pre  <- merge(pre,  cn, by = 'gene')
post <- merge(post, cn, by = 'gene')

amp_pre  <- pre$copy_number  > 4
amp_post <- post$copy_number > 4
stopifnot(sum(amp_pre) > 0)

cat("n genes merged with real CN:", nrow(pre), " n amplified (CN>4):", sum(amp_pre), "\n")
cat('Pre-correction logFC mean (amplified):',  mean(pre$avgFC[amp_pre]),   '\n')
cat('Post-correction logFC mean (amplified):', mean(post$avgFC[amp_post]), '\n')
cat('Correction effectiveness: difference =',
    mean(post$avgFC[amp_post]) - mean(pre$avgFC[amp_pre]), '\n')
cat('Spearman rho with CN, pre  =', cor(pre$avgFC,  pre$copy_number,  method = 'spearman'), '\n')
cat('Spearman rho with CN, post =', cor(post$avgFC, post$copy_number, method = 'spearman'), '\n')

cat("\n=== Focused: real MYC amplicon block (FAM84B, MYC, POU5F1B; CN=8, HT-29) ===\n")
block <- c("FAM84B", "MYC", "POU5F1B")
cat("Pre-correction:\n"); print(pre[pre$gene %in% block, ])
cat("Post-correction:\n"); print(post[post$gene %in% block, ])

cat("\n=== Known core-essential genes: check they remain depleted post-correction ===\n")
data(BAGEL_essential)
ess_block <- intersect(BAGEL_essential, pre$gene)[1:10]
cat("Sample essentials pre:\n"); print(pre[pre$gene %in% ess_block, ])
cat("Sample essentials post:\n"); print(post[post$gene %in% ess_block, ])

cat("\nDONE\n")

cat("\n=== Exporting gene-level mean pre/post LFC with CN for Python diagnostic cross-check ===\n")
pre_gene <- aggregate(avgFC ~ gene, data = pre, FUN = mean)
post_gene <- aggregate(avgFC ~ gene, data = post, FUN = mean)
colnames(pre_gene)[2] <- "lfc"
colnames(post_gene)[2] <- "lfc"
cn_gene <- unique(cn)
write.csv(merge(pre_gene, cn_gene, by = "gene"), "/tmp/ccr_out/ht29_pre_gene_lfc_cn.csv", row.names = FALSE)
write.csv(merge(post_gene, cn_gene, by = "gene"), "/tmp/ccr_out/ht29_post_gene_lfc_cn.csv", row.names = FALSE)
cat("Wrote CSVs.\n")
