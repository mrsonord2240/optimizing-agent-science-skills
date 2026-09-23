# Final-pass Phase 2 Input 4 -- regression: fresh-session CAMERA redundancy collapse.
# Usage: F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh finalpass2_input4_camera.R
library(xcms)
library(MsExperiment)
library(CAMERA)
library(BiocParallel)
register(SerialParam())

xdata <- readRDS("F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run/finalpass2_xdata.rds")
xs <- suppressWarnings(as(xdata, "xcmsSet"))
sampclass(xs) <- sampleData(xdata)$sample_group
xsa <- xsAnnotate(xs)
xsa <- groupFWHM(xsa, perfwhm = 0.6)
xsa <- groupCorr(xsa)
xsa <- findIsotopes(xsa, mzabs = 0.01, ppm = 10)
xsa <- findAdducts(xsa, polarity = "positive")
peaklist <- getPeaklist(xsa)
isotopes <- sum(nchar(trimws(peaklist$isotopes)) > 0)
adducts <- sum(nchar(trimws(peaklist$adduct)) > 0)
pseudospectra <- length(unique(peaklist$pcgroup))
cat("features=", nrow(peaklist), " pseudospectra=", pseudospectra, " isotopes=", isotopes,
    " adducts=", adducts, "\n", sep = "")
stopifnot(nrow(peaklist) > 0, pseudospectra > 0, pseudospectra <= nrow(peaklist))
cat("PASS\n")
