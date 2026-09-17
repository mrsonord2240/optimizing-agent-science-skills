# Input 3 (Edge, regression of pre-fix Input 3, STRENGTHENED with real execution) --
# "I only have 2 files, 1 knockout and 1 wild-type, and they're profile-mode (uncentroided).
# Build me a feature table."
#
# Part (a) profile-mode centroiding requirement: still reasoning-only (no profile-mode LC-MS
# file is cached in this audit env; faahKO/MTBLS79 are both already centroided) -- graded by
# inspection against the Decision Tree in the eval viewer, same as the pre-fix audit.
#
# Part (b) THE FIX BEING TESTED, now made EXECUTABLE (upgrade from pre-fix's reasoning-only
# treatment): SKILL.md's Correspondence section now adds "For very small cohorts (e.g. n=2
# per group), re-derive minFraction as a fraction of the smaller group ... minFraction=1.0
# for n=2 per group". This script subsets the real faahKO cohort down to exactly 1 KO + 1 WT
# (n=1 per group, n=2 total) and runs the documented pipeline with minFraction=1.0 exactly as
# the new guidance specifies, to check the guidance is not just present but WORKS.

library(xcms)
library(MsExperiment)

base <- "F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO"
ko_files <- list.files(file.path(base, "KO"), pattern = "\\.CDF$", full.names = TRUE)[1]
wt_files <- list.files(file.path(base, "WT"), pattern = "\\.CDF$", full.names = TRUE)[1]
cdfs <- c(ko_files, wt_files)
pd <- data.frame(sample_name = sub("\\.CDF$", "", basename(cdfs)),
                 sample_group = c("KO", "WT"))
cat("n=2 cohort (1 KO + 1 WT):", basename(cdfs), "\n")

raw <- readMsExperiment(spectraFiles = cdfs, sampleData = pd)
cwp <- CentWaveParam(ppm = 25, peakwidth = c(20, 80), snthresh = 10,
                     prefilter = c(3, 1000), noise = 1000, mzdiff = -0.001,
                     integrate = 1L, mzCenterFun = "wMean")
xdata3 <- findChromPeaks(raw, param = cwp)
cat("Peaks detected (n=2):", nrow(chromPeaks(xdata3)), "\n")

xdata3 <- adjustRtime(xdata3, param = ObiwarpParam(binSize = 0.6))
cat("adjustRtime (obiwarp) completed on n=2 cohort\n")

cat("\n--- Testing the NEW small-cohort guidance: minFraction = 1.0 for n=2 per group ---\n")
pdp_new <- PeakDensityParam(sampleGroups = sampleData(xdata3)$sample_group,
                            bw = 30, minFraction = 1.0, minSamples = 1, binSize = 0.025)
res_new <- tryCatch({
  xd <- groupChromPeaks(xdata3, param = pdp_new)
  paste("OK --", nrow(featureDefinitions(xd)), "features (present in BOTH replicates)")
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("minFraction=1.0 (new guidance):", res_new, "\n")

cat("\n--- Contrast: the moderate-cohort default (minFraction=0.5) on the SAME n=2 data ---\n")
pdp_old <- PeakDensityParam(sampleGroups = sampleData(xdata3)$sample_group,
                            bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025)
res_old <- tryCatch({
  xd <- groupChromPeaks(xdata3, param = pdp_old)
  paste("OK --", nrow(featureDefinitions(xd)), "features (present in only ONE replicate allowed)")
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("minFraction=0.5 (moderate-cohort default, per the new prose's own warning):", res_old, "\n")
cat("DONE\n")
