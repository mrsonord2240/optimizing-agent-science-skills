# Input 2 (Variant A) -- "My run is UHPLC on a Q-Exactive Orbitrap with sharp peaks
# (FWHM ~3-8s) and pooled QC injections. Set CentWave params for this instrument,
# align with PeakGroupsParam using the QC injections as anchors, then group into
# features."
#
# Honesty note: faahKO has no pooled-QC samples (only KO/WT biological samples), so the
# QC-anchor part of this request cannot be demonstrated with a real QC group. To still
# execute real code against real data, the WT group is used as a stand-in "anchor" group
# for PeakGroupsParam(subset=...) -- this is flagged explicitly, not hidden, and is NOT
# how a real analyst would do it (a real analyst needs true pooled QC injections).
# The UHPLC-tight peakwidth on this genuinely broad-peak HPLC dataset is intentional: it
# exercises the Skill's own documented "peakwidth mismatch" failure mode (peakwidth c(2,20)
# copied onto non-UHPLC data -> real peaks silently absent) to check whether that claim holds.

library(xcms)
library(MsExperiment)

base <- "F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO"
ko_files <- list.files(file.path(base, "KO"), pattern = "\\.CDF$", full.names = TRUE)
wt_files <- list.files(file.path(base, "WT"), pattern = "\\.CDF$", full.names = TRUE)
cdfs <- c(ko_files, wt_files)
pd <- data.frame(
  sample_name = sub("\\.CDF$", "", basename(cdfs)),
  sample_group = c(rep("KO", length(ko_files)), rep("WT", length(wt_files)))
)

raw <- readMsExperiment(spectraFiles = cdfs, sampleData = pd)

# UHPLC-appropriate CentWave per the Skill's Quantitative Thresholds ("UHPLC c(2,20)").
# ppm 10 is mid-range for Orbitrap/Q-Exactive per the same table (5-10).
cwp_uhplc <- CentWaveParam(ppm = 10, peakwidth = c(2, 20), snthresh = 10,
                           prefilter = c(3, 1000), noise = 1000, mzdiff = -0.001,
                           integrate = 1L, mzCenterFun = "wMean")
t0 <- Sys.time()
xdata2 <- findChromPeaks(raw, param = cwp_uhplc)
cat("findChromPeaks (tight UHPLC peakwidth on broad-peak HPLC data) took",
    round(as.numeric(Sys.time() - t0, units = "secs"), 1), "s\n")
cat("Peaks detected with tight peakwidth c(2,20):", nrow(chromPeaks(xdata2)), "\n")
cat("(Input 1's correctly-scoped broad peakwidth c(20,80) on the same 12 files found 10826 peaks)\n")

# Initial correspondence needed before PeakGroupsParam per SKILL.md's own commented-out example.
pdp0 <- PeakDensityParam(sampleGroups = sampleData(xdata2)$sample_group,
                         bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025)
xdata2 <- groupChromPeaks(xdata2, param = pdp0)
cat("Initial correspondence features (pre-alignment):", nrow(featureDefinitions(xdata2)), "\n")

anchor_idx <- which(sampleData(xdata2)$sample_group == "WT")
cat("Using WT samples as pooled-QC-anchor stand-in, indices:", paste(anchor_idx, collapse = ","), "\n")

res <- tryCatch({
  xdata2b <- adjustRtime(xdata2, param = PeakGroupsParam(minFraction = 0.85, span = 0.4,
                          subset = anchor_idx, subsetAdjust = "average"))
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("PeakGroupsParam(subset=WT-as-anchor) result:", res, "\n")

if (identical(res, "OK")) {
  xdata2 <- xdata2b
  pdp1 <- PeakDensityParam(sampleGroups = sampleData(xdata2)$sample_group,
                           bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025)
  xdata2 <- groupChromPeaks(xdata2, param = pdp1)
  cat("Post-alignment regrouped features:", nrow(featureDefinitions(xdata2)), "\n")
}
cat("DONE\n")
