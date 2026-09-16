# Diagnostic follow-up to input2_variantA.R: is the PeakGroupsParam(subset=...) error
# specific to too-strict minFraction=0.85 on a 6-sample anchor subset with only 183
# pre-alignment features, or a general break in the SKILL.md-documented pattern?
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
                           prefilter = c(3, 1000), noise = 1000)
xdata2 <- findChromPeaks(raw, param = cwp_uhplc)
pdp0 <- PeakDensityParam(sampleGroups = sampleData(xdata2)$sample_group,
                         bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025)
xdata2 <- groupChromPeaks(xdata2, param = pdp0)
cat("Pre-alignment features:", nrow(featureDefinitions(xdata2)), "\n")

anchor_idx <- which(sampleData(xdata2)$sample_group == "WT")

for (mf in c(0.5, 0.7, 0.85, 1.0)) {
  res <- tryCatch({
    xd <- adjustRtime(xdata2, param = PeakGroupsParam(minFraction = mf, span = 0.4,
                        subset = anchor_idx, subsetAdjust = "average"))
    paste("OK -- adjusted")
  }, error = function(e) paste("ERROR:", conditionMessage(e)))
  cat("minFraction =", mf, "->", res, "\n")
}

# Also test PeakGroupsParam with NO subset (using all 12 samples as their own anchors) --
# isolates whether the failure is specific to the 'subset' argument path.
res_nosub <- tryCatch({
  xd <- adjustRtime(xdata2, param = PeakGroupsParam(minFraction = 0.85, span = 0.4))
  "OK -- adjusted, no subset"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("No subset, minFraction=0.85 ->", res_nosub, "\n")
cat("DONE\n")
