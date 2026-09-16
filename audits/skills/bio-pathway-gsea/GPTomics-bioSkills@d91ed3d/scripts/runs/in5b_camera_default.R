# Does limma's MODERN camera default (preset inter.gene.cor = 0.01) still catch
# the correlated set, or does the Skill's CAMERA advice need the inter.gene.cor
# argument it never mentions?
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
D <- 'F:/OpenScience/audits/bio-pathway-gsea/data'
suppressPackageStartupMessages({library(limma); library(msigdbr)})
mat <- as.matrix(read.csv(file.path(D,'SYNTHETIC_logcpm_matrix.csv'), row.names=1))
meta <- read.csv(file.path(D,'SYNTHETIC_sample_metadata.csv'))
grp <- factor(meta$group[match(colnames(mat), meta$sample)], levels=c('control','treated'))
design <- model.matrix(~ grp)
h <- msigdbr(species='Homo sapiens', collection='H')
sets <- split(as.character(h$ncbi_gene), h$gs_name)
sets <- lapply(sets, function(g) intersect(unique(g), rownames(mat))); sets <- sets[lengths(sets)>=10]
idx <- limma::ids2indices(sets, rownames(mat))
rows <- c('HALLMARK_OXIDATIVE_PHOSPHORYLATION','HALLMARK_E2F_TARGETS','HALLMARK_ADIPOGENESIS')
for (lab in c('default (preset 0.01)','inter.gene.cor=NA (estimated)','inter.gene.cor=0 (naive)')) {
  a <- switch(lab,
    'default (preset 0.01)'         = camera(mat, idx, design, contrast=2),
    'inter.gene.cor=NA (estimated)' = camera(mat, idx, design, contrast=2, inter.gene.cor=NA),
    'inter.gene.cor=0 (naive)'      = camera(mat, idx, design, contrast=2, inter.gene.cor=0))
  cat(sprintf('\n%-32s  sets at FDR<0.05: %d\n', lab, sum(a$FDR<0.05)))
  print(a[rows, c('NGenes','Direction','PValue','FDR')])
}
cat('\nEXIT OK\n')
