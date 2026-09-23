# Final-pass Phase 2 Input 1 -- regression: 12-file faahKO full feature-table pipeline.
# Usage: F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh finalpass2_input1_canonical.R
library(xcms)
library(MsExperiment)
library(BiocParallel)
register(SerialParam())

base <- "F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO"
files <- c(list.files(file.path(base, "KO"), pattern = "\\.CDF$", full.names = TRUE),
           list.files(file.path(base, "WT"), pattern = "\\.CDF$", full.names = TRUE))
pd <- data.frame(sample_name = sub("\\.CDF$", "", basename(files)),
                 sample_group = c(rep("KO", 6), rep("WT", 6)))
raw <- readMsExperiment(spectraFiles = files, sampleData = pd)
cwp <- CentWaveParam(ppm = 25, peakwidth = c(20, 80), snthresh = 10,
                     prefilter = c(3, 1000), noise = 1000, mzdiff = -0.001,
                     integrate = 1L, mzCenterFun = "wMean")
xdata <- findChromPeaks(raw, param = cwp)
cat("peaks=", nrow(chromPeaks(xdata)), "\n", sep = "")
xdata <- adjustRtime(xdata, param = ObiwarpParam(binSize = 0.6))
xdata <- groupChromPeaks(xdata, param = PeakDensityParam(
  sampleGroups = sampleData(xdata)$sample_group, bw = 30, minFraction = 0.5,
  minSamples = 1, binSize = 0.025))
xdata <- fillChromPeaks(xdata, param = ChromPeakAreaParam())
feat <- featureValues(xdata, value = "into")
filled_fraction <- mean(chromPeakData(xdata)$is_filled)
cat("features=", nrow(featureDefinitions(xdata)), " matrix=", paste(dim(feat), collapse = "x"),
    " filled_fraction=", round(filled_fraction, 4), " residual_na=", sum(is.na(feat)), "\n", sep = "")
stopifnot(nrow(chromPeaks(xdata)) > 0, nrow(featureDefinitions(xdata)) > 0,
          ncol(feat) == 12, is.finite(filled_fraction))
saveRDS(xdata, "F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run/finalpass2_xdata.rds")
write.csv(as.data.frame(feat), "F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run/finalpass2_feature_table.csv")
cat("PASS\n")
