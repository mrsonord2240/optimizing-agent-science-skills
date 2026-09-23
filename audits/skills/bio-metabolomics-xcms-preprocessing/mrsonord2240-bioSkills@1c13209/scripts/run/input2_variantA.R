# Input 2 (Variant A, regression of pre-fix Input 2) -- "My run is UHPLC on a Q-Exactive
# Orbitrap with sharp peaks (FWHM ~3-8s) and pooled QC injections. Set CentWave params for
# this instrument, align with PeakGroupsParam using the QC injections as anchors, then
# group into features."
#
# Honesty note: faahKO has no pooled-QC samples; WT is used as an explicitly-disclosed
# anchor stand-in, as in the pre-fix audit.
#
# THE FIX BEING TESTED: SKILL.md's Retention-Time Alignment section now (a) changes its
# own commented example from minFraction=0.85 to minFraction=0.5, (b) adds a paragraph
# explaining minFraction/anchor-count fragility and naming BOTH failure modes to expect
# ("Not enough peak groups..." and the cryptic colnames error), and (c) a matching Common
# Errors row. This script (i) runs the now-documented default minFraction=0.5 and checks it
# succeeds, and (ii) re-runs the pre-fix minFraction sweep to confirm the failure modes the
# new prose describes still occur as described (0.7 informative failure, 0.85/1.0 cryptic
# failure) -- i.e. checks the new guidance is not just present but ACCURATE.

library(xcms)
library(MsExperiment)

base <- "F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO"
ko_files <- list.files(file.path(base, "KO"), pattern = "\\.CDF$", full.names = TRUE)
wt_files <- list.files(file.path(base, "WT"), pattern = "\\.CDF$", full.names = TRUE)
cdfs <- c(ko_files, wt_files)
pd <- data.frame(sample_name = sub("\\.CDF$", "", basename(cdfs)),
                 sample_group = c(rep("KO", length(ko_files)), rep("WT", length(wt_files))))

raw <- readMsExperiment(spectraFiles = cdfs, sampleData = pd)

cwp_uhplc <- CentWaveParam(ppm = 10, peakwidth = c(2, 20), snthresh = 10,
                           prefilter = c(3, 1000), noise = 1000, mzdiff = -0.001,
                           integrate = 1L, mzCenterFun = "wMean")
t0 <- Sys.time()
xdata2 <- findChromPeaks(raw, param = cwp_uhplc)
cat("findChromPeaks (tight UHPLC peakwidth on broad-peak HPLC data) took",
    round(as.numeric(Sys.time() - t0, units = "secs"), 1), "s\n")
cat("Peaks detected with tight peakwidth c(2,20):", nrow(chromPeaks(xdata2)), "\n")
cat("(Input 1's correctly-scoped broad peakwidth on the same 12 files finds far more peaks)\n")

pdp0 <- PeakDensityParam(sampleGroups = sampleData(xdata2)$sample_group,
                         bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025)
xdata2 <- groupChromPeaks(xdata2, param = pdp0)
n_pre <- nrow(featureDefinitions(xdata2))
cat("Initial correspondence features (pre-alignment):", n_pre, "\n")

anchor_idx <- which(sampleData(xdata2)$sample_group == "WT")
cat("Using WT samples as pooled-QC-anchor stand-in, indices:", paste(anchor_idx, collapse = ","), "\n")

cat("\n--- (i) Running the FIXED SKILL.md's now-documented default: minFraction = 0.5 ---\n")
res_default <- tryCatch({
  xdata2b <- adjustRtime(xdata2, param = PeakGroupsParam(minFraction = 0.5, span = 0.4,
                          subset = anchor_idx, subsetAdjust = "average"))
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("PeakGroupsParam(minFraction=0.5, subset=WT-as-anchor) result:", res_default, "\n")

if (identical(res_default, "OK")) {
  xdata2 <- xdata2b
  pdp1 <- PeakDensityParam(sampleGroups = sampleData(xdata2)$sample_group,
                           bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025)
  xdata2 <- groupChromPeaks(xdata2, param = pdp1)
  cat("Post-alignment regrouped features:", nrow(featureDefinitions(xdata2)), "\n")
}

cat("\n--- (ii) Re-running the minFraction sweep to check the new prose's claims ---\n")
for (mf in c(0.5, 0.7, 0.85, 1.0)) {
  res <- tryCatch({
    xd <- adjustRtime(xdata2, param = PeakGroupsParam(minFraction = mf, span = 0.4,
                        subset = anchor_idx, subsetAdjust = "average"))
    "OK -- adjusted"
  }, error = function(e) paste("ERROR:", conditionMessage(e)))
  cat("minFraction =", mf, "->", res, "\n")
}
cat("DONE\n")
