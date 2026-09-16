# INPUT 1 (Canonical) - "Here are my full DESeq2 results for all 14,000 genes
# (Wald stat in `stat`, Entrez IDs in `entrez_id`). Build the ranked vector the
# right way and run GO biological-process GSEA with a fixed seed. Give me the
# top terms by adjusted p-value with NES and the leading-edge genes."
#
# Code below is the SKILL.md "Build the Ranked Vector" block and the
# "Run Preranked GSEA on GO" block, VERBATIM except for the input path.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
D <- 'F:/OpenScience/audits/bio-pathway-gsea/data'
R <- 'F:/OpenScience/audits/bio-pathway-gsea/runs'

# --- Version Compatibility block the SKILL.md tells the agent to run first ---
for (p in c('clusterProfiler','org.Hs.eg.db','msigdbr','fgsea'))
  cat(sprintf('%-16s installed %s\n', p, as.character(packageVersion(p))))
cat('SKILL.md claims tested with: clusterProfiler 4.18.4+, org.Hs.eg.db 3.22+, msigdbr 26+, fgsea 1.36+\n\n')

# ===================== SKILL.md block: Build the Ranked Vector ==============
library(clusterProfiler)
library(org.Hs.eg.db)

de <- read.csv(file.path(D, 'SYNTHETIC_deseq2_results.csv'))  # DE list source: differential-expression/de-results
gene_list <- de$stat                       # DESeq2 Wald stat: signed + variance-calibrated
names(gene_list) <- de$entrez_id
gene_list <- gene_list[!is.na(gene_list)]
gene_list <- gene_list[!duplicated(names(gene_list))]   # one statistic per gene; duplicates double-count hits
gene_list <- sort(gene_list, decreasing = TRUE)         # REQUIRED: unsorted input silently mis-ranks
# ===========================================================================
cat('ranked vector: n =', length(gene_list), '| max', round(max(gene_list),3),
    '| min', round(min(gene_list),3), '| strictly decreasing:',
    !is.unsorted(rev(gene_list)), '\n')

# ===================== SKILL.md block: Run Preranked GSEA on GO =============
t0 <- Sys.time()
set.seed(123)                              # fixes the multilevel Monte Carlo; any fixed seed
gse_go <- gseGO(geneList = gene_list, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID',
                ont = 'BP', exponent = 1, minGSSize = 10, maxGSSize = 500,
                eps = 0, pvalueCutoff = 0.05, pAdjustMethod = 'BH',
                seed = TRUE, by = 'fgsea', verbose = FALSE)
gse_go <- setReadable(gse_go, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID')
# ===========================================================================
cat('gseGO wall time:', round(as.numeric(difftime(Sys.time(), t0, units='secs')),1), 's\n')

res <- as.data.frame(gse_go)
cat('significant GO BP terms (p.adjust < 0.05):', nrow(res), '\n')
cat('columns returned:', paste(names(res), collapse=', '), '\n')
cat('positive NES:', sum(res$NES > 0), '| negative NES:', sum(res$NES < 0), '\n\n')

show <- function(x, k=10) print(head(x[, c('ID','Description','setSize','NES','pvalue','p.adjust')], k), row.names=FALSE)
cat('--- top 10 by p.adjust ---\n'); show(res[order(res$p.adjust), ])
cat('\n--- top 6 POSITIVE NES ---\n'); show(res[order(-res$NES), ], 6)
cat('\n--- top 6 NEGATIVE NES ---\n'); show(res[order(res$NES), ], 6)

# did the planted biology come back?
oxterm <- grep('oxidative phosphorylation|respiratory electron|electron transport chain|ATP synthesis coupled',
               res$Description, ignore.case = TRUE)
ccterm <- grep('DNA replication|cell cycle|chromosome segregation|mitotic', res$Description, ignore.case = TRUE)
cat('\nplanted-UP (OXPHOS-like) terms recovered:', length(oxterm),
    '| all NES>0:', all(res$NES[oxterm] > 0), '\n')
print(head(res[oxterm, c('Description','NES','p.adjust')], 5), row.names = FALSE)
cat('\nplanted-DOWN (cell-cycle-like) terms recovered:', length(ccterm),
    '| all NES<0:', all(res$NES[ccterm] < 0), '\n')
print(head(res[ccterm, c('Description','NES','p.adjust')], 5), row.names = FALSE)

# leading edge readability, as the SKILL.md tells the agent to read it
le <- strsplit(res$core_enrichment[order(res$p.adjust)][1], '/')[[1]]
cat('\ntop term leading edge:', length(le), 'genes;', paste(head(le, 12), collapse=', '), '\n')
cat('core_enrichment is symbols (setReadable applied):', !grepl('^[0-9]+$', le[1]), '\n')
cat('min p.adjust:', min(res$p.adjust), '| min raw pvalue:', min(res$pvalue),
    '| any pvalue == 0 (eps=0):', any(res$pvalue == 0), '\n')

# reproducibility: re-run with the same seed
set.seed(123)
gse2 <- gseGO(geneList = gene_list, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID',
              ont = 'BP', exponent = 1, minGSSize = 10, maxGSSize = 500, eps = 0,
              pvalueCutoff = 0.05, pAdjustMethod = 'BH', seed = TRUE, by = 'fgsea', verbose = FALSE)
r2 <- as.data.frame(gse2)
cat('\nreproducibility with set.seed(123): nrow identical:', nrow(r2) == nrow(res),
    '| p.adjust identical:', isTRUE(all.equal(sort(r2$p.adjust), sort(res$p.adjust))), '\n')

write.csv(res, file.path(R, 'in1_go_terms.csv'), row.names = FALSE)
saveRDS(gene_list, file.path(R, 'gene_list.rds'))
cat('\nEXIT OK\n')
