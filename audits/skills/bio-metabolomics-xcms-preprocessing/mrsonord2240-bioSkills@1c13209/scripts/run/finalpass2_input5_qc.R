# Final-pass Phase 2 Input 5 -- regression: RSD and D-ratio filters on disclosed QC stand-in.
# Usage: F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh finalpass2_input5_qc.R
library(xcms)
library(MsExperiment)
library(BiocParallel)
register(SerialParam())

xdata <- readRDS("F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run/finalpass2_xdata.rds")
qc <- sampleData(xdata)$sample_group == "WT" # stand-in only; not genuine pooled QCs
study <- sampleData(xdata)$sample_group == "KO"
n0 <- nrow(featureDefinitions(xdata))
x_rsd <- filterFeatures(xdata, filter = RsdFilter(threshold = 0.3, qcIndex = qc))
n1 <- nrow(featureDefinitions(x_rsd))
x_dratio <- filterFeatures(x_rsd, filter = DratioFilter(threshold = 0.5, qcIndex = qc, studyIndex = study))
n2 <- nrow(featureDefinitions(x_dratio))
cat("before=", n0, " after_rsd=", n1, " after_dratio=", n2, "\n", sep = "")
stopifnot(n0 > 0, n1 <= n0, n2 <= n1)
cat("PASS\n")
