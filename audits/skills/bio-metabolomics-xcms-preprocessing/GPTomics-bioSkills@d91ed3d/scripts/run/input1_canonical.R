# Input 1 (Canonical) -- "I have 12 centroided CDF files from an HPLC LC-MS run,
# 6 knockout mice and 6 wild-type, no QC samples yet. Turn these into a feature
# table: peak detection, RT alignment, correspondence, gap-filling."
# Real data: faahKO (12 CDFs, 6 KO + 6 WT), cached in audit-env public-data.
# Following SKILL.md: readMsExperiment -> findChromPeaks(CentWaveParam) ->
# adjustRtime(ObiwarpParam) -> groupChromPeaks(PeakDensityParam) -> fillChromPeaks.

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
cat("Files:", length(cdfs), "| KO:", length(ko_files), "| WT:", length(wt_files), "\n")

raw <- readMsExperiment(spectraFiles = cdfs, sampleData = pd)
cat("Loaded MsExperiment with", length(raw), "samples\n")

# faahKO is broad-peak conventional-HPLC data (per the reference example's own comment and
# the original faahKO/xcms vignette) -- peakwidth set broad accordingly, per the Skill's
# Decision Tree row "High-res centroid ... CentWaveParam" and its Quantitative Thresholds
# table row "HPLC c(10,40)" widened slightly to match this dataset's known broad peaks.
cwp <- CentWaveParam(ppm = 25, peakwidth = c(20, 80), snthresh = 10,
                     prefilter = c(3, 1000), noise = 1000, mzdiff = -0.001,
                     integrate = 1L, mzCenterFun = "wMean")
t0 <- Sys.time()
xdata <- findChromPeaks(raw, param = cwp)
cat("findChromPeaks took", round(as.numeric(Sys.time() - t0, units = "secs"), 1), "s\n")
cat("Peaks detected:", nrow(chromPeaks(xdata)), "\n")
print(table(chromPeaks(xdata)[, "sample"]))

xdata <- adjustRtime(xdata, param = ObiwarpParam(binSize = 0.6))
cat("adjustRtime (obiwarp) completed\n")

# Regroup is mandatory after adjustRtime per the Skill's Common Errors table
# ("Features defined on uncorrected RT" -> "Call groupChromPeaks again after alignment").
pdp <- PeakDensityParam(sampleGroups = sampleData(xdata)$sample_group,
                        bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025)
xdata <- groupChromPeaks(xdata, param = pdp)
cat("Features (correspondence):", nrow(featureDefinitions(xdata)), "\n")

xdata <- fillChromPeaks(xdata, param = ChromPeakAreaParam())
filled_fraction <- mean(chromPeakData(xdata)$is_filled)
cat("Fraction of filled peaks:", round(filled_fraction, 3), "\n")

feat <- featureValues(xdata, value = "into")
defs <- as.data.frame(featureDefinitions(xdata))
cat("Feature matrix dim:", paste(dim(feat), collapse = " x "), "\n")
cat("NA cells in feature matrix after fill:", sum(is.na(feat)), "\n")

out_dir <- "F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run"
saveRDS(xdata, file.path(out_dir, "xdata_input1.rds"))
result <- data.frame(feature = rownames(feat), mz = defs$mzmed, rt = defs$rtmed, feat, row.names = NULL)
write.csv(result, file.path(out_dir, "feature_table_input1.csv"), row.names = FALSE)
cat("Wrote", nrow(result), "features x", ncol(feat), "samples to feature_table_input1.csv\n")
cat("DONE\n")
