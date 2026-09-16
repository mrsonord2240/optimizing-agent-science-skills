# Input 4 (Variant B) -- "Now that I have a feature table from the KO/WT faahKO run,
# collapse adduct/isotope redundancy with CAMERA and show how many raw features
# collapse into unique pseudospectra." Builds on Input 1's real xdata (saved RDS).
# Follows SKILL.md's Redundancy Collapse section: groupFWHM -> groupCorr -> findIsotopes
# -> findAdducts, then coercion note (Common Errors: "as(xdata,'xcmsSet') fails or warns").

library(xcms)
library(MsExperiment)
library(CAMERA)

xdata <- readRDS("F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run/xdata_input1.rds")
cat("Loaded xdata: ", nrow(featureDefinitions(xdata)), "features x", length(xdata), "samples\n")

res <- tryCatch({
  xs <- as(xdata, "xcmsSet")
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)),
   warning = function(w) paste("WARNING:", conditionMessage(w)))
cat("as(xdata, 'xcmsSet') ->", res, "\n")

xs <- suppressWarnings(as(xdata, "xcmsSet"))
sampclass(xs) <- sampleData(xdata)$sample_group
cat("xcmsSet peaks:", nrow(xs@peaks), "\n")

xsa <- xsAnnotate(xs)
xsa <- groupFWHM(xsa, perfwhm = 0.6)
cat("After groupFWHM, pseudospectra groups:", length(xsa@pspectra), "\n")
xsa <- groupCorr(xsa)
cat("After groupCorr, pseudospectra groups:", length(xsa@pspectra), "\n")
xsa <- findIsotopes(xsa, mzabs = 0.01, ppm = 10)
xsa <- findAdducts(xsa, polarity = "positive")

peaklist <- getPeaklist(xsa)
cat("getPeaklist rows (should equal raw peak/feature count):", nrow(peaklist), "\n")
n_with_isotope <- sum(nchar(trimws(peaklist$isotopes)) > 0)
n_with_adduct <- sum(nchar(trimws(peaklist$adduct)) > 0)
cat("Features flagged with an isotope annotation:", n_with_isotope, "/", nrow(peaklist), "\n")
cat("Features flagged with an adduct annotation:", n_with_adduct, "/", nrow(peaklist), "\n")
cat("Unique pseudospectra (compound-level groups) after collapse:", length(unique(peaklist$pcgroup)), "\n")
cat("Raw features:", nrow(peaklist), "-> unique pseudospectra:", length(unique(peaklist$pcgroup)),
    "| ratio:", round(nrow(peaklist) / length(unique(peaklist$pcgroup)), 2), "features per pseudospectrum\n")
cat("DONE\n")
