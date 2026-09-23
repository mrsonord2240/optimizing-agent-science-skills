# Final-pass Input 2 — prior AccuCor regression using its shipped real reference data.
library(accucor)
library(readxl)

infile <- "F:/OpenScience/audits/bio-metabolomics-isotope-tracing/data/accucor_real_sample_input.csv"
outbase <- "F:/OpenScience/audits/bio-metabolomics-isotope-tracing/run/finalpass2/input2_accucor_output"
extdata <- system.file("extdata", package = "accucor")
reference_file <- file.path(extdata, "C_Sample_Input_Simple_corrected.xlsx")
before_hash <- unname(tools::md5sum(reference_file))
before_count <- length(list.files(extdata, all.files = TRUE, no.. = TRUE))

# The installed example/reference is the nominal-mass branch (resolution=0).
# This re-runs the prior reference-ground-truth input while retaining the Skill's
# required output_base isolation pattern.
result <- natural_abundance_correction(path = infile, resolution = 0, purity = 0.99,
                                       output_base = outbase)
after_hash <- unname(tools::md5sum(reference_file))
after_count <- length(list.files(extdata, all.files = TRUE, no.. = TRUE))
stopifnot(identical(before_hash, after_hash), identical(before_count, after_count))
stopifnot(file.exists(paste0(outbase, "_corrected.xlsx")))

norm <- result$Normalized
g6p <- norm[norm$Compound == "glucose-6-phosphate", ]
ref <- read_excel(reference_file, sheet = "Normalized")
ref_g6p <- ref[ref$Compound == "glucose-6-phosphate", ]
cols <- c("A12_1", "A12_2", "A12_3", "D12_1", "D12_2", "D12_3", "R12_1", "R12_2", "R12_3")
max_diff <- max(abs(as.matrix(g6p[, cols]) - as.matrix(ref_g6p[, cols])))
stopifnot(max_diff < 1e-6)
cat("g6p_rows=", nrow(g6p), "\n", sep = "")
cat("max_abs_difference=", format(max_diff, scientific = TRUE), "\n", sep = "")
cat("output_exists=TRUE; extdata_unchanged=TRUE\n")
