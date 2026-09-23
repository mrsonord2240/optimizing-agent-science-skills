# Input 1 (Canonical, regression of pre-fix Input 1) -- "I have 12 centroided CDF files
# from an HPLC LC-MS run, 6 knockout mice and 6 wild-type, no QC samples yet. Turn these
# into a feature table: peak detection, RT alignment, correspondence, gap-filling."
# Real data: faahKO (12 CDFs, 6 KO + 6 WT). Re-audit against the FIXED SKILL.md
# (mrsonord2240/bioSkills@68473287), which now adds explicit residual-NA guidance to the
# Gap-Filling section. This run follows that guidance literally (sum(is.na(feat)) line
# now shown in the Skill's own code block) rather than just noting NAs exist.

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

# faahKO is broad-peak conventional-HPLC data -- peakwidth set broad accordingly, per the
# Skill's Decision Tree row "High-res centroid ... CentWaveParam" and Quantitative
# Thresholds "HPLC c(10,40)" widened slightly to match this dataset's known broad peaks
# (same parameterization used in the pre-fix audit, for a clean regression comparison).
cwp <- CentWaveParam(ppm = 25, peakwidth = c(20, 80), snthresh = 10,
                     prefilter = c(3, 1000), noise = 1000, mzdiff = -0.001,
                     integrate = 1L, mzCenterFun = "wMean")
t0 <- Sys.time()
xdata <- findChromPeaks(raw, param = cwp)
cat("findChromPeaks took", round(as.numeric(Sys.time() - t0, units = "secs"), 1), "s\n")
cat("Peaks detected:", nrow(chromPeaks(xdata)), "\n")

xdata <- adjustRtime(xdata, param = ObiwarpParam(binSize = 0.6))
cat("adjustRtime (obiwarp) completed\n")

pdp <- PeakDensityParam(sampleGroups = sampleData(xdata)$sample_group,
                        bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025)
xdata <- groupChromPeaks(xdata, param = pdp)
cat("Features (correspondence):", nrow(featureDefinitions(xdata)), "\n")

xdata <- fillChromPeaks(xdata, param = ChromPeakAreaParam())
filled <- chromPeakData(xdata)$is_filled
filled_fraction <- mean(filled)
cat("Fraction of filled peaks:", round(filled_fraction, 3), "\n")

feat <- featureValues(xdata, value = "into")
defs <- as.data.frame(featureDefinitions(xdata))
cat("Feature matrix dim:", paste(dim(feat), collapse = " x "), "\n")

# Following the FIXED SKILL.md's Gap-Filling code block literally:
#   sum(is.na(feat))    # residual NAs = below-detection in that sample, not a fill error
n_na <- sum(is.na(feat))
cat("Residual NA cells in feature matrix after fillChromPeaks:", n_na, "\n")
cat("Per SKILL.md's Gap-Filling section: these are genuine non-detections (no signal",
    "anywhere in the fill window for that sample), NOT fill failures -- do not silently",
    "drop or zero-fill them.\n")

out_dir <- "F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run"
saveRDS(xdata, file.path(out_dir, "xdata_input1.rds"))
result <- data.frame(feature = rownames(feat), mz = defs$mzmed, rt = defs$rtmed, feat, row.names = NULL)
write.csv(result, file.path(out_dir, "feature_table_input1.csv"), row.names = FALSE)
cat("Wrote", nrow(result), "features x", ncol(feat), "samples to feature_table_input1.csv\n")
cat("DONE\n")
