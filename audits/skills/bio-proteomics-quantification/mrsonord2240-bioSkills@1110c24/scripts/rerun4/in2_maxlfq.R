# Input 2 regression: the pass-3 rewrite of the MaxLFQ block.
# The block is extracted from the fork's SKILL.md by extract_r.py and sourced
# verbatim; only `peptide_long` is prepared beforehand, which is what the
# block's own comment says it needs.
suppressPackageStartupMessages({library(iq)})
cat('iq version:', as.character(packageVersion('iq')), '\n')

QD <- 'F:/OpenScience/audits/bio-proteomics-quantification/data'
QW <- 'F:/OpenScience/audits/bio-proteomics-quantification/rerun4'

ev <- read.table(file.path(QD, 'evidence.txt'), sep = '\t', header = TRUE,
                 quote = '', comment.char = '', stringsAsFactors = FALSE)
cat('evidence rows:', nrow(ev), '| file lines:',
    length(readLines(file.path(QD, 'evidence.txt'))) - 1, '\n')

peptide_long <- data.frame(
  protein   = ev$Proteins,
  ion       = paste0(ev$Modified.sequence, '_', ev$Charge),
  run       = ev$Raw.file,
  intensity = as.numeric(ev$Intensity),
  stringsAsFactors = FALSE)
peptide_long <- peptide_long[is.finite(peptide_long$intensity) &
                             peptide_long$intensity > 0 &
                             nzchar(peptide_long$protein), ]
cat('peptide_long rows:', nrow(peptide_long), '| proteins:',
    length(unique(peptide_long$protein)), '| runs:',
    length(unique(peptide_long$run)), '\n')

source(file.path(QW, 'blocks', 'maxlfq.R'), echo = FALSE)

cat('protein_matrix dim:', dim(protein_matrix), '\n')
cat('column order as returned:', paste(colnames(protein_matrix), collapse = ','), '\n')
cat('is the column order sorted?',
    identical(colnames(protein_matrix), sort(colnames(protein_matrix))), '\n')
cat('per-run medians (centred):',
    paste(round(apply(protein_matrix, 2, median, na.rm = TRUE) -
                median(protein_matrix, na.rm = TRUE), 3), collapse = ' '), '\n')
cat('disconnected proteins:', length(disconnected), '\n')

# the named-estimate claim
r1 <- maxLFQ(protein_list[[1]])
cat('names(result$estimate) is NULL on iq', as.character(packageVersion('iq')), ':',
    is.null(names(r1$estimate)), '\n')
cat('after setNames:', paste(names(protein_estimate), collapse = ','), '\n')

# Accuracy against the fixture's ground truth
truth <- read.csv(file.path(QD, 'truth_proteins.csv'), stringsAsFactors = FALSE)
ann <- read.csv(file.path(QD, 'sample_annotation.csv'), stringsAsFactors = FALSE)
ctl <- colnames(protein_matrix)[grepl('^C', colnames(protein_matrix))]
trt <- colnames(protein_matrix)[grepl('^T', colnames(protein_matrix))]
fc <- rowMeans(protein_matrix[, trt, drop = FALSE], na.rm = TRUE) -
      rowMeans(protein_matrix[, ctl, drop = FALSE], na.rm = TRUE)
tcol <- intersect(c('true_log2fc', 'log2FC', 'log2fc'), colnames(truth))[1]
pcol <- intersect(c('protein', 'Protein', 'protein_id'), colnames(truth))[1]
m <- match(names(fc), truth[[pcol]])
ok <- !is.na(m) & is.finite(fc)
cat('proteins matched to truth:', sum(ok), '| corr(MaxLFQ FC, truth):',
    round(cor(fc[ok], truth[[tcol]][m[ok]]), 3), '\n')
cat('mean(FC - truth):', round(mean(fc[ok] - truth[[tcol]][m[ok]]), 3), '\n')

# Does the block's required run normalization actually matter?
norm_off <- preprocess(peptide_long, primary_id = 'protein', secondary_id = 'ion',
                       sample_id = 'run', intensity_col = 'intensity',
                       median_normalization = FALSE, pdf_out = NULL)
pt_off <- create_protein_table(create_protein_list(norm_off), method = 'maxLFQ')
mo <- pt_off$estimate
cat('WITHOUT median_normalization, per-run medians (centred):',
    paste(round(apply(mo, 2, median, na.rm = TRUE) - median(mo, na.rm = TRUE), 3),
          collapse = ' '), '\n')
