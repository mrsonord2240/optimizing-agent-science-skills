# INPUT 5 (Stress / multi-part) - "Before I write this up I want it stress-tested.
# (a) Run Reactome GSEA offline as a second, reproducible database.
# (b) Show me how the answer changes if I rank by the DESeq2 Wald stat vs raw
#     -log10(p) vs bare log2FoldChange.
# (c) My oxidative-phosphorylation genes are co-regulated - is the preranked FDR
#     trustworthy there? I also have the logCPM matrix and the two-group design."
#
# Follows SKILL.md: gsePathway routing, the ranking-metric table, the
# "Preranked p-values treated as correlation-honest" failure mode, and the
# CAMERA recommendation in the decision tree.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
D <- 'F:/OpenScience/audits/bio-pathway-gsea/data'; R <- 'F:/OpenScience/audits/bio-pathway-gsea/runs'
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)
  library(ReactomePA); library(limma); library(msigdbr)})
de <- read.csv(file.path(D, 'SYNTHETIC_deseq2_results.csv'))
gl <- readRDS(file.path(R, 'gene_list.rds'))

# ============ (a) Reactome, local reactome.db, as the SKILL.md routes =======
cat('=== (a) gsePathway (ReactomePA', as.character(packageVersion('ReactomePA')),
    '/ reactome.db', as.character(packageVersion('reactome.db')), ', local) ===\n')
set.seed(123)
gse_re <- gsePathway(gl, organism = 'human', minGSSize = 10, maxGSSize = 500,
                     eps = 0, pvalueCutoff = 0.05, pAdjustMethod = 'BH',
                     seed = TRUE, verbose = FALSE)
gse_re <- setReadable(gse_re, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID')
rr <- as.data.frame(gse_re)
cat('significant Reactome pathways:', nrow(rr), '| pos', sum(rr$NES>0), '| neg', sum(rr$NES<0), '\n')
print(head(rr[order(rr$p.adjust), c('ID','Description','setSize','NES','p.adjust')], 8), row.names=FALSE)
write.csv(rr, file.path(R, 'in5_reactome_terms.csv'), row.names = FALSE)

# ============ (b) three ranking metrics, same data, same sets ==============
cat('\n=== (b) ranking-metric comparison on the MSigDB Hallmark collection ===\n')
h <- msigdbr(species='Homo sapiens', collection='H'); t2g <- h[, c('gs_name','ncbi_gene')]
mk <- function(v) { names(v) <- de$entrez_id; v <- v[!is.na(v)]
                    v <- v[!duplicated(names(v))]; sort(v, decreasing = TRUE) }
metrics <- list(
  `DESeq2 stat (SKILL.md recommends)` = mk(de$stat),
  `raw -log10(p), unsigned (SKILL.md forbids)` = mk(-log10(pmax(de$pvalue, 1e-300))),
  `bare log2FoldChange (SKILL.md: last resort)` = mk(de$log2FoldChange))
for (nm in names(metrics)) {
  set.seed(123)
  z <- as.data.frame(GSEA(metrics[[nm]], TERM2GENE=t2g, exponent=1, minGSSize=10,
        maxGSSize=500, eps=0, pvalueCutoff=0.05, pAdjustMethod='BH', seed=TRUE, verbose=FALSE))
  ox <- z[z$ID=='HALLMARK_OXIDATIVE_PHOSPHORYLATION', ]; e2 <- z[z$ID=='HALLMARK_E2F_TARGETS', ]
  cat(sprintf('\n%-44s -> %2d sets | pos %2d neg %2d\n', nm, nrow(z), sum(z$NES>0), sum(z$NES<0)))
  cat(sprintf('   planted UP  OXPHOS : %s\n', if(nrow(ox)) sprintf('NES %+.3f  padj %.2e', ox$NES, ox$p.adjust) else 'NOT SIGNIFICANT'))
  cat(sprintf('   planted DOWN E2F   : %s\n', if(nrow(e2)) sprintf('NES %+.3f  padj %.2e', e2$NES, e2$p.adjust) else 'NOT SIGNIFICANT'))
  if (nrow(z)) cat('   top set:', z$ID[which.min(z$p.adjust)], '\n')
}

# ============ (c) is the preranked (gene-permutation) FDR honest? ===========
cat('\n=== (c) gene-permutation preranked vs CAMERA on the same data ===\n')
mat <- as.matrix(read.csv(file.path(D,'SYNTHETIC_logcpm_matrix.csv'), row.names=1))
meta <- read.csv(file.path(D,'SYNTHETIC_sample_metadata.csv'))
grp <- factor(meta$group[match(colnames(mat), meta$sample)], levels=c('control','treated'))
design <- model.matrix(~ grp)
sets <- split(as.character(h$ncbi_gene), h$gs_name)
sets <- lapply(sets, function(g) intersect(unique(g), rownames(mat)))
sets <- sets[lengths(sets) >= 10]
idx <- limma::ids2indices(sets, rownames(mat))

cam_def <- limma::camera(mat, idx, design, contrast = 2)                      # limma default: PRESET inter.gene.cor = 0.01
cam     <- limma::camera(mat, idx, design, contrast = 2, inter.gene.cor = NA) # estimate the correlation per set
cat('CAMERA (limma', as.character(packageVersion('limma')), '):\n')
cat('  default call returns   :', paste(names(cam_def), collapse=', '), '\n')
cat('  inter.gene.cor=NA adds :', paste(names(cam), collapse=', '), '\n')
print(head(cam[order(cam$PValue), ], 6))
cat('\nmeasured inter-gene correlation inside the planted OXPHOS set:',
    round(cam['HALLMARK_OXIDATIVE_PHOSPHORYLATION','Correlation'], 4),
    '| inside E2F targets:', round(cam['HALLMARK_E2F_TARGETS','Correlation'], 4), '\n')

# same matrix -> limma t -> preranked GSEA (gene permutation)
fit <- eBayes(lmFit(mat, design))
tt  <- topTable(fit, coef=2, number=Inf, sort.by='none')
glm <- sort(setNames(tt$t, rownames(tt)), decreasing=TRUE)
set.seed(123)
pr <- as.data.frame(GSEA(glm, TERM2GENE=t2g, exponent=1, minGSSize=10, maxGSSize=500,
        eps=0, pvalueCutoff=1, pAdjustMethod='BH', seed=TRUE, verbose=FALSE))
cmp <- merge(pr[,c('ID','NES','pvalue','p.adjust')],
             data.frame(ID=rownames(cam), cam[,c('Correlation','Direction','PValue','FDR')]), by='ID')
names(cmp) <- c('set','NES','gseP','gseFDR','interGeneCor','camDir','camP','camFDR')
cat('\nsets significant at FDR 0.05 -- preranked gene permutation:', sum(cmp$gseFDR<0.05),
    '| CAMERA:', sum(cmp$camFDR<0.05), '\n')
cat('median gseFDR / camFDR ratio:', signif(median(cmp$gseFDR/pmax(cmp$camFDR,1e-300)),3), '\n')
cat('\nthe two planted sets and the 4 with the highest inter-gene correlation:\n')
sel <- unique(c(match(c('HALLMARK_OXIDATIVE_PHOSPHORYLATION','HALLMARK_E2F_TARGETS'), cmp$set),
                order(-cmp$interGeneCor)[1:4]))
print(format(cmp[sel, c('set','interGeneCor','NES','gseFDR','camFDR')], digits=3), row.names=FALSE)
cat('\nsets called significant by gene-permutation GSEA but NOT by CAMERA:',
    sum(cmp$gseFDR<0.05 & cmp$camFDR>=0.05), 'of', sum(cmp$gseFDR<0.05), '\n')
print(cmp[cmp$gseFDR<0.05 & cmp$camFDR>=0.05, c('set','interGeneCor','gseFDR','camFDR')], row.names=FALSE)
write.csv(cmp, file.path(R,'in5_camera_vs_preranked.csv'), row.names=FALSE)

# ROAST/fry, the other route in the decision tree
fr <- limma::fry(mat, idx, design, contrast=2)
cat('\nfry (self-contained rotation test) top 4:\n')
print(head(fr[order(fr$PValue), c('NGenes','Direction','PValue','FDR')], 4))

# --- (b2) does bare log2FC let low-count outliers hijack the leading edge? --
cat('\n=== (b2) the bare-log2FC trap: where do the low-count huge-LFC genes land? ===\n')
lfc  <- mk(de$log2FoldChange)
trap <- as.character(de$entrez_id[de$baseMean < 7 & abs(de$log2FoldChange) > 6])
cat('planted trap genes (baseMean < 7, |log2FC| > 6):', length(trap), '\n')
cat('  rank under bare-log2FC ranking:', paste(head(sort(match(trap, names(lfc))), 8), collapse=', '), '...\n')
cat('  rank under DESeq2-stat ranking:', paste(head(sort(match(trap, names(gl))), 8), collapse=', '), '...\n')
set.seed(123)
zl <- as.data.frame(GSEA(lfc, TERM2GENE=t2g, exponent=1, minGSSize=10, maxGSSize=500,
        eps=0, pvalueCutoff=0.05, seed=TRUE, verbose=FALSE))
if (nrow(zl)) { le <- strsplit(zl$core_enrichment[which.min(zl$p.adjust)], '/')[[1]]
  cat('top set under log2FC :', zl$ID[which.min(zl$p.adjust)], '| leading edge', length(le),
      'genes | trap genes inside:', sum(le %in% trap), '\n') }
set.seed(123)
zs <- as.data.frame(GSEA(gl, TERM2GENE=t2g, exponent=1, minGSSize=10, maxGSSize=500,
        eps=0, pvalueCutoff=0.05, seed=TRUE, verbose=FALSE))
le2 <- strsplit(zs$core_enrichment[which.min(zs$p.adjust)], '/')[[1]]
cat('top set under Wald stat:', zs$ID[which.min(zs$p.adjust)], '| leading edge', length(le2),
    'genes | trap genes inside:', sum(le2 %in% trap), '\n')

cat('\nEXIT OK\n')
