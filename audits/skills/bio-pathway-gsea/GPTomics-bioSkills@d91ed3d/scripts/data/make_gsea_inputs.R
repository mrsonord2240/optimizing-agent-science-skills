# ============================================================================
# SYNTHETIC data generator for the bio-pathway-gsea audit.
#
# EVERYTHING NUMERIC HERE IS SYNTHETIC. Gene identities (Entrez IDs, symbols)
# and gene-set membership come from the REAL org.Hs.eg.db 3.20.0 and
# msigdbr 26.1.0 annotation. Only the DE statistics, p-values and counts are
# simulated, with a KNOWN coordinated signal planted in real gene sets so that
# signal RECOVERY can be tested.
#
# Planted signal:
#   UP   : HALLMARK_OXIDATIVE_PHOSPHORYLATION members shifted to +1.1 mean
#          (overlaps GO:0006119 / GO:0022904 and Reactome respiratory electron
#           transport, so the same biology is recoverable in GO, MSigDB and
#           Reactome)
#   DOWN : HALLMARK_E2F_TARGETS members shifted to -1.1 mean
#          (overlaps GO cell-cycle / DNA replication terms)
#   TRAP : 25 low-count genes given huge unstable log2FC but near-zero Wald
#          stat, to test the Skill's "bare log2FC ranking" failure-mode claim.
# ============================================================================
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(org.Hs.eg.db); library(msigdbr); library(AnnotationDbi)
})
set.seed(20260916)
OUT <- 'F:/OpenScience/audits/bio-pathway-gsea/data'

# --- universe: real Entrez IDs that carry a GO BP annotation -----------------
go_map <- AnnotationDbi::select(org.Hs.eg.db, keys = keys(org.Hs.eg.db, 'ENTREZID'),
                                keytype = 'ENTREZID', columns = 'ONTOLOGY')
bp <- unique(go_map$ENTREZID[go_map$ONTOLOGY == 'BP' & !is.na(go_map$ONTOLOGY)])
bp <- sort(bp)
cat('Entrez IDs with a GO BP annotation:', length(bp), '\n')
universe <- sort(sample(bp, min(14000, length(bp))))
cat('SYNTHETIC universe size:', length(universe), '\n')

# --- real gene sets used to plant the signal --------------------------------
h <- msigdbr(species = 'Homo sapiens', collection = 'H')
cat('msigdbr columns:', paste(names(h), collapse = ', '), '\n')
oxphos <- unique(as.character(h$ncbi_gene[h$gs_name == 'HALLMARK_OXIDATIVE_PHOSPHORYLATION']))
e2f    <- unique(as.character(h$ncbi_gene[h$gs_name == 'HALLMARK_E2F_TARGETS']))
oxphos <- intersect(oxphos, universe); e2f <- intersect(e2f, universe)
# also plant the DOWN signal in a GO-coherent set so direction is testable in GO too
dnarep <- unique(AnnotationDbi::select(org.Hs.eg.db, keys = 'GO:0006260', keytype = 'GOALL',
                                       columns = 'ENTREZID')$ENTREZID)
e2f    <- setdiff(union(e2f, intersect(dnarep, universe)), oxphos)
cat('planted UP  HALLMARK_OXIDATIVE_PHOSPHORYLATION genes in universe:', length(oxphos), '\n')
cat('planted DOWN HALLMARK_E2F_TARGETS genes in universe:', length(e2f), '\n')

# --- synthetic DESeq2-style DE table ----------------------------------------
n <- length(universe)
stat <- rnorm(n, 0, 1)
names(stat) <- universe
stat[oxphos] <- rnorm(length(oxphos), 1.10, 1.0)
stat[e2f]    <- rnorm(length(e2f),   -1.10, 1.0)

baseMean <- round(exp(rnorm(n, 5.0, 1.6)), 2)
names(baseMean) <- universe
se  <- 1 / sqrt(pmax(log2(baseMean + 1), 1))         # noisier SE for low-count genes
log2FoldChange <- stat * se
pvalue <- 2 * pnorm(-abs(stat))
padj   <- p.adjust(pvalue, method = 'BH')

# TRAP genes: tiny counts, absurd LFC, no real evidence (near-zero Wald stat)
trap <- sample(setdiff(universe, c(oxphos, e2f)), 25)
baseMean[trap]       <- round(runif(25, 1.5, 6), 2)
log2FoldChange[trap] <- runif(25, 7, 12) * sample(c(-1, 1), 25, TRUE)
stat[trap]           <- rnorm(25, 0, 0.25)
pvalue[trap]         <- 2 * pnorm(-abs(stat[trap]))
padj                 <- p.adjust(pvalue, method = 'BH')
# a few exactly-zero p-values, as DESeq2/edgeR really emit for huge statistics
zeros <- sample(oxphos, 4); pvalue[zeros] <- 0; padj[zeros] <- 0

sym <- AnnotationDbi::mapIds(org.Hs.eg.db, keys = universe, keytype = 'ENTREZID',
                             column = 'SYMBOL', multiVals = 'first')

de <- data.frame(entrez_id = universe, symbol = unname(sym), baseMean = unname(baseMean),
                 log2FoldChange = unname(log2FoldChange), lfcSE = unname(se),
                 stat = unname(stat), pvalue = unname(pvalue),   # FULL precision: real DESeq2 stat does not tie
                 padj = unname(padj), stringsAsFactors = FALSE)
de <- de[order(de$pvalue), ]
write.csv(de, file.path(OUT, 'SYNTHETIC_deseq2_results.csv'), row.names = FALSE)
cat('wrote SYNTHETIC_deseq2_results.csv rows =', nrow(de), '\n')

# --- edgeR-flavoured variant: no stat column, symbols not Entrez, duplicates -
edg <- de[, c('symbol', 'log2FoldChange', 'pvalue', 'padj')]
names(edg) <- c('gene', 'logFC', 'PValue', 'FDR')
edg <- edg[!is.na(edg$gene), ]
edg$logCPM <- round(log2(de$baseMean[match(edg$gene, de$symbol)] + 1), 3)
dup <- edg[sample(nrow(edg), 300), ]; dup$PValue <- dup$PValue * runif(300, 0.5, 1.5)
edg <- rbind(edg, dup)                                  # 300 duplicate gene rows
edg <- edg[sample(nrow(edg)), ]                         # deliberately UNSORTED
write.csv(edg, file.path(OUT, 'SYNTHETIC_edger_qlf.csv'), row.names = FALSE)
cat('wrote SYNTHETIC_edger_qlf.csv rows =', nrow(edg),
    ' duplicate gene names =', sum(duplicated(edg$gene)),
    ' exact-zero PValue =', sum(edg$PValue == 0), '\n')

# --- expression matrix + design for CAMERA / ROAST / GSVA -------------------
# 2 groups x 10 samples. OXPHOS genes carry a SHARED latent factor, so the set
# is genuinely inter-gene correlated - the condition under which the Skill says
# gene-permutation preranked p-values are anti-conservative.
gm  <- sort(union(sample(universe, 4000), c(oxphos, e2f)))  # keep every planted gene in the matrix
ns  <- 20; grp <- factor(rep(c('control', 'treated'), each = 10))
mat <- matrix(rnorm(length(gm) * ns, 8, 1.2), nrow = length(gm),
              dimnames = list(gm, paste0('S', sprintf('%02d', 1:ns))))
ox_in <- intersect(oxphos, gm); e2_in <- intersect(e2f, gm)
latent <- rnorm(ns, 0, 0.9)                              # shared technical/biological factor
mat[ox_in, ] <- mat[ox_in, ] + rep(latent, each = length(ox_in))   # inter-gene correlation
mat[ox_in, grp == 'treated'] <- mat[ox_in, grp == 'treated'] + 0.55
mat[e2_in, grp == 'treated'] <- mat[e2_in, grp == 'treated'] - 0.55
mat <- round(mat, 4)
write.csv(mat, file.path(OUT, 'SYNTHETIC_logcpm_matrix.csv'))
write.csv(data.frame(sample = colnames(mat), group = as.character(grp)),
          file.path(OUT, 'SYNTHETIC_sample_metadata.csv'), row.names = FALSE)
cat('wrote SYNTHETIC_logcpm_matrix.csv', nrow(mat), 'x', ncol(mat),
    '| OXPHOS genes in matrix =', length(ox_in), '| E2F =', length(e2_in), '\n')

# --- a pre-selected unranked gene list (for the scope-boundary input) -------
up <- de[order(-de$stat), ]
hits <- head(up$symbol[!is.na(up$symbol)], 180)   # top 180 by Wald stat, statistics DISCARDED on purpose
writeLines(hits, file.path(OUT, 'SYNTHETIC_screen_hits.txt'))
cat('wrote SYNTHETIC_screen_hits.txt n =', length(hits), '\n')

writeLines(c(oxphos), file.path(OUT, 'planted_up_entrez.txt'))
writeLines(c(e2f),    file.path(OUT, 'planted_down_entrez.txt'))
cat('DONE\n')
