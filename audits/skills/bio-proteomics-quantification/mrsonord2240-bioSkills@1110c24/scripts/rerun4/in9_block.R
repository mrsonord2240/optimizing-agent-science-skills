# Input 9 regression: run the SKILL.md MaxLFQ block VERBATIM on the DIA-NN
# report, to check that the pass-3 rewrite really is the table-level route the
# prior audit had to hand-write for itself.
suppressPackageStartupMessages({library(iq); library(arrow)})
QW <- 'F:/OpenScience/audits/bio-proteomics-quantification/rerun4'
QD <- 'F:/OpenScience/audits/bio-proteomics-quantification/data'

rep <- as.data.frame(read_parquet('F:/OpenScience/audits/bio-proteomics-data-import/data/report.parquet'))
rep <- rep[rep$Q.Value <= 0.01 & rep$PG.Q.Value <= 0.01, ]
peptide_long <- data.frame(protein = rep$Protein.Group, ion = rep$Precursor.Id,
                           run = rep$Run, intensity = rep$Precursor.Normalised,
                           stringsAsFactors = FALSE)
peptide_long <- peptide_long[is.finite(peptide_long$intensity) & peptide_long$intensity > 0, ]
cat('rows after q filters:', nrow(peptide_long), '\n')

source(file.path(QW, 'blocks', 'maxlfq.R'), echo = FALSE)
cat('SKILL block on DIA-NN: protein_matrix', dim(protein_matrix),
    '| disconnected', length(disconnected), '\n')
cat('per-run medians (centred):',
    paste(round(apply(protein_matrix, 2, median, na.rm = TRUE) -
                median(protein_matrix, na.rm = TRUE), 3), collapse = ' '), '\n')
cat('setNames gave named estimate:', paste(names(protein_estimate), collapse = ','), '\n')

truth <- read.csv(file.path(QD, 'truth_proteins.csv'), stringsAsFactors = FALSE)
ctl <- grep('^C', colnames(protein_matrix), value = TRUE)
trt <- grep('^T', colnames(protein_matrix), value = TRUE)
fc <- rowMeans(protein_matrix[, trt, drop = FALSE], na.rm = TRUE) -
      rowMeans(protein_matrix[, ctl, drop = FALSE], na.rm = TRUE)
m <- match(sub(';.*', '', names(fc)), truth$protein)
ok <- !is.na(m) & is.finite(fc)
cat('matched to truth:', sum(ok), '| corr(iq FC, truth):',
    round(cor(fc[ok], truth$true_log2fc[m[ok]]), 3), '\n')
