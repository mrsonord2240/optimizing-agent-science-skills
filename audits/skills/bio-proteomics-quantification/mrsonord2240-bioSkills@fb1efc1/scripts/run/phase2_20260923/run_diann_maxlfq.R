# Input 9 regression: documented iq MaxLFQ script against a DIA-NN-style parquet report.
suppressPackageStartupMessages({library(iq); library(arrow)})
run_dir <- 'F:/OpenScience/audits/bio-proteomics-quantification/run/phase2_20260923'
report <- as.data.frame(read_parquet('F:/OpenScience/audits/bio-proteomics-data-import/data/report.parquet'))
report <- report[report$Q.Value <= 0.01 & report$PG.Q.Value <= 0.01, ]
peptide_long <- data.frame(protein=report$Protein.Group, ion=report$Precursor.Id, run=report$Run,
                            intensity=report$Precursor.Normalised, stringsAsFactors=FALSE)
peptide_long <- peptide_long[is.finite(peptide_long$intensity) & peptide_long$intensity > 0, ]
write.csv(peptide_long, file.path(run_dir, 'diann_peptide_long.csv'), row.names=FALSE)
norm <- preprocess(peptide_long, primary_id='protein', secondary_id='ion', sample_id='run',
                   intensity_col='intensity', median_normalization=TRUE, pdf_out=NULL)
pt <- create_protein_table(create_protein_list(norm), method='maxLFQ')
stopifnot(nrow(pt$estimate) > 900, ncol(pt$estimate) == 8, all(is.finite(as.matrix(pt$estimate)[!is.na(pt$estimate)])))
write.csv(pt$estimate, file.path(run_dir, 'diann_maxlfq.csv'))
cat('rows=', nrow(peptide_long), ' matrix=', paste(dim(pt$estimate), collapse='x'), ' disconnected=', sum(nzchar(pt$annotation)), '\n', sep='')
