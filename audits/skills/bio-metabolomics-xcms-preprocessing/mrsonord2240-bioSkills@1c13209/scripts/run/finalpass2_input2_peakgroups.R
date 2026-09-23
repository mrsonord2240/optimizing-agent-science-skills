# Final-pass Phase 2 Input 2 -- regression: QC-subset PeakGroups alignment at minFraction 0.5.
# Usage: F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh finalpass2_input2_peakgroups.R
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
xdata <- findChromPeaks(raw, param = CentWaveParam(ppm = 10, peakwidth = c(2, 20), snthresh = 10,
  prefilter = c(3, 1000), noise = 1000, mzdiff = -0.001, integrate = 1L, mzCenterFun = "wMean"))
xdata <- groupChromPeaks(xdata, param = PeakDensityParam(
  sampleGroups = sampleData(xdata)$sample_group, bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025))
qc_idx <- which(sampleData(xdata)$sample_group == "WT") # disclosed QC stand-in; faahKO has no pooled QCs
before <- nrow(featureDefinitions(xdata))
xdata <- adjustRtime(xdata, param = PeakGroupsParam(minFraction = 0.5, span = 0.4,
  subset = qc_idx, subsetAdjust = "average"))
xdata <- groupChromPeaks(xdata, param = PeakDensityParam(
  sampleGroups = sampleData(xdata)$sample_group, bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025))
after <- nrow(featureDefinitions(xdata))
cat("peaks=", nrow(chromPeaks(xdata)), " initial_features=", before, " regrouped_features=", after,
    " qc_anchor_n=", length(qc_idx), "\n", sep = "")
stopifnot(nrow(chromPeaks(xdata)) > 0, before > 0, after > 0, length(qc_idx) == 6)
cat("PASS\n")
