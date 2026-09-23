# Input 4 (Edge) - bio-single-cell-differential-abundance
# n = 1 per condition. SKILL.md:28 is explicit: "With n=1 per condition the donor is perfectly
# confounded with condition: the effect is unidentifiable, not merely underpowered, yet scCODA
# and sccomp will still emit confident credible_effects() that are pure donor idiosyncrasy".
# What do the R methods do? Do they refuse, or do they answer?
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(speckle); library(limma); library(miloR)
                                library(SingleCellExperiment); library(Seurat); library(dplyr)})

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', TRUE)
ss <- read.csv(file.path(D, 'sample_sheet.csv')); rownames(ss) <- ss$sample
tc <- tc[!tc$true_doublet & !tc$true_low_quality, ]
tc$condition <- ss[tc$sample, 'condition']

one <- tc[tc$sample %in% c('S1', 'S5'), ]   # one control donor, one treated donor
cat('n=1 per condition: S1 (control, D1) and S5 (treated, D5);', nrow(one), 'cells\n')
print(round(100 * prop.table(table(one$sample, one$true_cell_type), 1), 1))

cat('\n--- propeller with n=1 per group ---\n')
r <- try(propeller(clusters = one$true_cell_type, sample = one$sample, group = one$condition),
         silent = TRUE)
if (inherits(r, 'try-error')) {
  cat('REFUSED / ERRORED:\n  ', as.character(r))
} else {
  cat('propeller RETURNED A RESULT with one sample per group:\n')
  num <- intersect(c('PropMean.control', 'PropMean.treated', 'PropRatio', 'Tstatistic',
                     'P.Value', 'FDR'), colnames(r))
  print(cbind(cluster = as.character(r[[1]]), round(r[, num], 5)))
  cat('  significant at FDR < 0.05:', sum(r$FDR < 0.05), 'cell types\n')
  cat('  -> the Skill says n=1 makes the effect unidentifiable. propeller does not refuse;\n')
  cat('     whether it emits p-values at all is the thing to check, and it did.\n')
}

cat('\n--- the same test with n=4 per group, for contrast ---\n')
r4 <- propeller(clusters = tc$true_cell_type, sample = tc$sample, group = tc$condition)
cat('  n=4/group significant at FDR < 0.05:', sum(r4$FDR < 0.05), 'cell types (',
    paste(rownames(r4)[r4$FDR < 0.05], collapse = ', '), ')\n')

cat('\n--- what happens at n=2 and n=3 per group (the Skill says >=2, ideally 3-4) ---\n')
for (n in 2:4) {
  ctrl <- paste0('S', 1:n); trt <- paste0('S', 5:(4 + n))
  sub <- tc[tc$sample %in% c(ctrl, trt), ]
  rr <- try(propeller(clusters = sub$true_cell_type, sample = sub$sample,
                      group = sub$condition), silent = TRUE)
  if (inherits(rr, 'try-error')) {
    cat(sprintf('  n=%d/group: ERRORED\n', n))
  } else {
    nk <- rr[rownames(rr) == 'NK cells', ]
    cat(sprintf('  n=%d/group: %d types at FDR<0.05; NK p=%.4g FDR=%.4g (truth: NK is the only real change)\n',
                n, sum(rr$FDR < 0.05), nk$P.Value, nk$FDR))
  }
}
cat('DONE\n')
