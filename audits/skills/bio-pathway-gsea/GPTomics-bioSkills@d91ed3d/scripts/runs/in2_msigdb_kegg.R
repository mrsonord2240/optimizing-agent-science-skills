# INPUT 2 (Variant A) - "Run GSEA against the MSigDB Hallmark collection on my
# ranked human gene list, then also run gseKEGG and note that KEGG queries the
# live database." (verbatim from the Skill's own usage-guide Example Prompts)
#
# Code = SKILL.md "Run GSEA on KEGG, Reactome, or MSigDB" block, VERBATIM.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
R <- 'F:/OpenScience/audits/bio-pathway-gsea/runs'
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
gene_list <- readRDS(file.path(R, 'gene_list.rds'))
cat('ranked vector n =', length(gene_list), '\n')

# --------- SKILL.md block, MSigDB half, verbatim ---------------------------
library(msigdbr)
h <- msigdbr(species = 'Homo sapiens', collection = 'H')    # 26.x: collection= (was category=); gs_collection (was gs_cat)
t2g <- h[, c('gs_name', 'ncbi_gene')]                       # 26.x Entrez column is ncbi_gene; older releases used entrez_gene
set.seed(123)
gse_h <- GSEA(geneList = gene_list, TERM2GENE = t2g, exponent = 1,
              minGSSize = 10, maxGSSize = 500, eps = 0,
              pvalueCutoff = 0.05, seed = TRUE, verbose = FALSE)
# ---------------------------------------------------------------------------
cat("msigdbr collection= accepted:", 'gs_collection' %in% names(h),
    '| ncbi_gene column present:', 'ncbi_gene' %in% names(h),
    '| t2g class:', class(t2g)[1], '| t2g rows:', nrow(t2g), '\n')
rh <- as.data.frame(gse_h)
cat('significant Hallmarks:', nrow(rh), '\n')
print(head(rh[order(rh$p.adjust), c('ID','setSize','NES','p.adjust')], 12), row.names = FALSE)
cat('\nplanted UP  HALLMARK_OXIDATIVE_PHOSPHORYLATION -> ')
print(rh[rh$ID == 'HALLMARK_OXIDATIVE_PHOSPHORYLATION', c('NES','p.adjust','setSize')], row.names = FALSE)
cat('planted DOWN HALLMARK_E2F_TARGETS -> ')
print(rh[rh$ID == 'HALLMARK_E2F_TARGETS', c('NES','p.adjust','setSize')], row.names = FALSE)
write.csv(rh, file.path(R, 'in2_hallmark_terms.csv'), row.names = FALSE)

# setReadable on a GSEA() result (SKILL.md Common Errors says apply it)
rd <- tryCatch({ x <- setReadable(gse_h, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID')
                 substr(as.data.frame(x)$core_enrichment[1], 1, 60) },
               error = function(e) paste('ERROR:', conditionMessage(e)))
cat('\nsetReadable on GSEA() result ->', rd, '\n')

# --------- SKILL.md block, KEGG half, verbatim (live REST API) --------------
cat('\n--- gseKEGG (live KEGG REST API; run date', format(Sys.Date()), ') ---\n')
kres <- tryCatch({
  set.seed(123)
  gse_kegg <- gseKEGG(geneList = gene_list, organism = 'hsa', keyType = 'ncbi-geneid',
                      minGSSize = 10, maxGSSize = 500, eps = 0,
                      pvalueCutoff = 0.05, seed = TRUE, verbose = FALSE)
  as.data.frame(gse_kegg)
}, error = function(e) {cat('gseKEGG FAILED:', conditionMessage(e), '\n'); NULL})
if (!is.null(kres)) {
  cat('significant KEGG pathways:', nrow(kres), '\n')
  print(head(kres[order(kres$p.adjust), c('ID','Description','NES','p.adjust')], 8), row.names = FALSE)
  write.csv(kres, file.path(R, 'in2_kegg_terms.csv'), row.names = FALSE)
}
cat('\nEXIT OK\n')
