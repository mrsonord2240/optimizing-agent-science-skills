# Input 2 (Variant A) -- real accucor shipped example data (ground truth), NOT synthetic.
# User request: "I have an El-MAVEN-style isotopologue CSV export for TCA-cycle intermediates
# from a 13C6-glucose experiment on an Orbitrap (resolution 100000, 99% tracer purity). Run
# AccuCor natural-abundance correction and give me the corrected/normalized MID for
# glucose-6-phosphate."
#
# Follows the SKILL.md pattern: accucor::natural_abundance_correction(path=..., resolution=...,
# purity=...). Output is redirected with output_base to our own run/ dir -- NEVER write into the
# shared R-lib package's extdata/ (a first attempt without output_base overwrote the package's
# own shipped reference file; see eval_viewer note).

library(accucor)
library(readxl)

infile <- "F:/OpenScience/audits/bio-metabolomics-isotope-tracing/data/accucor_real_sample_input.csv"
outbase <- "F:/OpenScience/audits/bio-metabolomics-isotope-tracing/run/input2_accucor_output"

result <- natural_abundance_correction(path = infile, resolution = 0, purity = 0.99,
                                        output_base = outbase)

norm <- result$Normalized
g6p <- norm[norm$Compound == "glucose-6-phosphate", ]
cat("Normalized MID for glucose-6-phosphate (our run):\n")
print(g6p)

ref <- read_excel(
  "F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/R-lib/accucor/extdata/C_Sample_Input_Simple_corrected.xlsx",
  sheet = "Normalized")
ref_g6p <- ref[ref$Compound == "glucose-6-phosphate", ]
cat("\nShipped reference (ground truth) MID for glucose-6-phosphate:\n")
print(ref_g6p)

cols <- c("A12_1","A12_2","A12_3","D12_1","D12_2","D12_3","R12_1","R12_2","R12_3")
diffs <- abs(as.matrix(g6p[, cols]) - as.matrix(ref_g6p[, cols]))
cat("\nMax abs difference vs ground truth:", max(diffs), "\n")
cat("Matches ground truth (tol 1e-6):", all(diffs < 1e-6), "\n")
