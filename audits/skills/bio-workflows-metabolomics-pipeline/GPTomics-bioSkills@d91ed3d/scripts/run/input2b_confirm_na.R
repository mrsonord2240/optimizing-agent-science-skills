suppressMessages({library(pmp); library(ropls)})
pm <- as.matrix(read.csv("F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/MTBLS79/MTBLS79_peak_matrix.csv",
                         row.names = 1, check.names = FALSE))
meta <- read.csv("F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/MTBLS79/MTBLS79_sample_metadata.csv",
                  row.names = 1, check.names = FALSE)
meta <- meta[colnames(pm), ]
sample_class <- meta$Class
batch_id <- meta$Batch
injection_order <- seq_len(ncol(pm))

filtered <- filter_peaks_by_fraction(pm, classes = sample_class, min_frac = 0.5, qc_label = "QC")
corrected <- QCRSC(df = filtered, order = injection_order, batch = batch_id,
        classes = sample_class, spar = 0, minQC = 5, qc_label = "QC")
rsd_filtered <- filter_peaks_by_rsd(corrected, max_rsd = 30, classes = sample_class, qc_label = "QC")
normalized <- suppressWarnings(pqn_normalisation(rsd_filtered, classes = sample_class, qc_label = "QC"))

nm <- as.matrix(normalized)
cat("normalized matrix:", nrow(nm), "x", ncol(nm), "\n")
cat("Total NA cells:", sum(is.na(nm)), "of", length(nm), "(", round(100*sum(is.na(nm))/length(nm),2), "%)\n")
cat("Samples with >=1 NA:", sum(colSums(is.na(nm)) > 0), "of", ncol(nm), "\n")
cat("Features with >=1 NA:", sum(rowSums(is.na(nm)) > 0), "of", nrow(nm), "\n")

# Confirm this is exactly why opls() throws "missing value where TRUE/FALSE needed"
x <- t(nm)[sample_class != "QC", ]
cat("\nStudy matrix (samples x features) fed to opls():", nrow(x), "x", ncol(x), "-- NAs present:", any(is.na(x)), "\n")
cat("SKILL.md's Stage-2 comment says 'Impute only the sparse residual holes... (see normalization-qc)'\n")
cat("but the Stage-4 code block feeds `normalized` straight into opls() with no imputation call in between.\n")
