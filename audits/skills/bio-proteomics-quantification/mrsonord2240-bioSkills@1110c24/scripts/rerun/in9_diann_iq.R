# Quant Input 9 (NEW): DIA-NN 1.9 report.parquet -> recompute MaxLFQ with iq for ALL proteins in R. SYNTHETIC data
# (shared report.parquet; truth_proteins.csv). The Skill shows maxLFQ for ONE protein and names iq::preprocess.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages({library(arrow); library(iq)})
rep <- as.data.frame(read_parquet('F:/OpenScience/audits/bio-proteomics-data-import/data/report.parquet'))
cat('columns:', paste(names(rep), collapse = ','), '\n')
icol <- intersect(c('Precursor.Normalised', 'Precursor.Quantity'), names(rep))[1]
f <- rep[rep$Q.Value <= 0.01 & rep$PG.Q.Value <= 0.01 & rep$Global.PG.Q.Value <= 0.01 & rep[[icol]] > 0, ]
cat('rows after q filters:', nrow(f), '| intensity column:', icol, '\n')
norm <- preprocess(f, primary_id = 'Protein.Group', secondary_id = 'Precursor.Id', sample_id = 'Run',
                   intensity_col = icol, median_normalization = TRUE, pdf_out = NULL)
plist <- create_protein_list(norm)
res <- create_protein_table(plist, method = 'maxLFQ')
M <- res$estimate
cat('iq protein table:', dim(M), '| per-run median (centred):', round(apply(M, 2, median, na.rm = TRUE) - median(M, na.rm = TRUE), 3), '\n')
d <- tapply(log2(f$PG.MaxLFQ[f$PG.MaxLFQ > 0]), list(f$Protein.Group[f$PG.MaxLFQ > 0], f$Run[f$PG.MaxLFQ > 0]), mean)
pp <- intersect(rownames(M), rownames(d)); cc <- intersect(colnames(M), colnames(d))
fc <- function(m) rowMeans(m[, grep('^T', colnames(m)), drop = FALSE], na.rm = TRUE) - rowMeans(m[, grep('^C', colnames(m)), drop = FALSE], na.rm = TRUE)
truth <- read.csv('F:/OpenScience/audits/bio-proteomics-quantification/data/truth_proteins.csv'); rownames(truth) <- truth$protein
a <- fc(M[pp, cc]); b <- fc(d[pp, cc]); ok <- pp[is.finite(a) & is.finite(b) & pp %in% truth$protein & truth[pp, 'class'] != 'on_off']
cat(sprintf('proteins compared: %d | corr(iq FC, DIA-NN PG.MaxLFQ FC) %.3f | corr with truth: iq %.3f, DIA-NN %.3f\n', length(ok), cor(a[ok], b[ok]),
            cor(a[ok], truth[ok, 'true_log2fc']), cor(b[ok], truth[ok, 'true_log2fc'])))
