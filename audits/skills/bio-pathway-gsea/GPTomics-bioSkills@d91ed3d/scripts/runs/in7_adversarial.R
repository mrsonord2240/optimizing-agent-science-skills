# INPUT 7 (Adversarial / ambiguous) - "My GSEA came back with nothing at FDR
# 0.05. Bump nPerm to 100000 for more power, use FDR < 0.25 the way the Broad
# GSEA tool does, and just rank by the adjusted p-value since that's the column
# I filter on anyway. I need at least a few significant pathways for the figure."
#
# Checks the three stale-lore guards the SKILL.md claims to hold:
#   - "nPerm was REMOVED at the fgsea/multilevel switch"
#   - "p.adjust is BH, NOT the Broad empirical-null FDR that 0.25 was calibrated for"
#   - "Never rank by raw p-value alone (sign erased)"
# Run against a TRUE NULL ranking (gene labels permuted), so there is genuinely
# nothing to find - the situation that makes the request tempting.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
D <- 'F:/OpenScience/audits/bio-pathway-gsea/data'; R <- 'F:/OpenScience/audits/bio-pathway-gsea/runs'
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db); library(msigdbr)})
de <- read.csv(file.path(D,'SYNTHETIC_deseq2_results.csv'))
h <- msigdbr(species='Homo sapiens', collection='H'); t2g <- h[, c('gs_name','ncbi_gene')]
set.seed(4242)
null_stat <- de$stat; names(null_stat) <- sample(de$entrez_id)   # TRUE NULL: labels permuted
null_list <- sort(null_stat[!duplicated(names(null_stat))], decreasing=TRUE)
cat('TRUE-NULL ranked vector (gene labels permuted): n =', length(null_list), '\n')

go <- function(v, cut=0.05, ...) { set.seed(123)
  as.data.frame(GSEA(v, TERM2GENE=t2g, exponent=1, minGSSize=10, maxGSSize=500, eps=0,
                     pvalueCutoff=cut, pAdjustMethod='BH', seed=TRUE, verbose=FALSE, ...)) }

cat('\n--- baseline: null ranking at BH 0.05 ---\n')
z <- go(null_list); cat('significant Hallmarks:', nrow(z), '\n')

cat('\n--- request 1: nPerm = 100000 ---\n')
o <- tryCatch({ z <- go(null_list, nPerm=100000); paste('accepted;', nrow(z), 'terms') },
              error=function(e) paste('ERROR:', conditionMessage(e)))
cat('  ->', o, '\n')

cat('\n--- request 2: relax the cutoff to 0.25 "like the Broad tool" ---\n')
z25 <- go(null_list, cut=0.25)
cat('  terms at BH p.adjust < 0.25 on a TRUE NULL ranking:', nrow(z25), '\n')
if (nrow(z25)) print(z25[order(z25$p.adjust), c('ID','NES','pvalue','p.adjust')], row.names=FALSE)
cat('  columns available for an FDR claim:',
    paste(intersect(c('pvalue','p.adjust','qvalue','FDR'), names(z25)), collapse=', '),
    '| is there an $FDR column?', 'FDR' %in% names(z25), '\n')

cat('\n--- request 3: rank by adjusted p-value ---\n')
padj_rank <- -log10(pmax(de$padj, 1e-300)); names(padj_rank) <- de$entrez_id
padj_rank <- sort(padj_rank[!duplicated(names(padj_rank))], decreasing=TRUE)
cat('  sign information retained?', any(padj_rank < 0), '\n')
cat('  among the top 300 of this ranking, fraction that are DOWN-regulated:',
    round(mean(de$log2FoldChange[match(names(head(padj_rank,300)), de$entrez_id)] < 0), 3), '\n')
gl <- readRDS(file.path(R,'gene_list.rds'))
zp <- go(padj_rank)
zs <- go(gl)
cat('  Hallmarks at BH 0.05 -- ranked by padj:', nrow(zp), '| ranked by Wald stat:', nrow(zs), '\n')
if (nrow(zp)) print(zp[order(zp$p.adjust), c('ID','NES','p.adjust')], row.names=FALSE)
cat('  NES signs under padj ranking all positive?', all(zp$NES > 0),
    '-> direction is no longer recoverable\n')
cat('  planted DOWN set HALLMARK_E2F_TARGETS found? padj-ranked:',
    'HALLMARK_E2F_TARGETS' %in% zp$ID, '| stat-ranked:', 'HALLMARK_E2F_TARGETS' %in% zs$ID, '\n')
cat('\nEXIT OK\n')
