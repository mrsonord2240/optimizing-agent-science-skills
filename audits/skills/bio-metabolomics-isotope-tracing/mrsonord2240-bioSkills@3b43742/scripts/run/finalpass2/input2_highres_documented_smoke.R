# Supporting smoke test for the documented high-resolution AccuCor call pattern.
library(accucor)
infile <- "F:/OpenScience/audits/bio-metabolomics-isotope-tracing/data/accucor_real_sample_input.csv"
outbase <- "F:/OpenScience/audits/bio-metabolomics-isotope-tracing/run/finalpass2/input2_highres_documented"
result <- natural_abundance_correction(path = infile, resolution = 100000, purity = 0.99,
                                       output_base = outbase)
stopifnot(file.exists(paste0(outbase, "_corrected.xlsx")))
stopifnot("Normalized" %in% names(result))
stopifnot(nrow(result$Normalized) > 0)
cat("normalized_rows=", nrow(result$Normalized), "\n", sep = "")
cat("documented_high_resolution_call_completed=TRUE\n")
