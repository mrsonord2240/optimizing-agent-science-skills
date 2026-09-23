# Final-pass Phase 2 Input 3 -- regression: one sample per group correspondence semantics.
# Usage: F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh finalpass2_input3_edge.R
library(xcms)
library(MsExperiment)
library(BiocParallel)
register(SerialParam())

base <- "F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO"
files <- c(list.files(file.path(base, "KO"), pattern = "\\.CDF$", full.names = TRUE)[1],
           list.files(file.path(base, "WT"), pattern = "\\.CDF$", full.names = TRUE)[1])
raw <- readMsExperiment(spectraFiles = files, sampleData = data.frame(sample_group = c("KO", "WT")))
xdata <- findChromPeaks(raw, param = CentWaveParam(ppm = 25, peakwidth = c(20, 80), snthresh = 10,
  prefilter = c(3, 1000), noise = 1000, mzdiff = -0.001, integrate = 1L, mzCenterFun = "wMean"))
xdata <- adjustRtime(xdata, param = ObiwarpParam(binSize = 0.6))
count_grouped <- function(groups, mf) nrow(featureDefinitions(groupChromPeaks(xdata,
  param = PeakDensityParam(sampleGroups = groups, bw = 30, minFraction = mf, minSamples = 1, binSize = 0.025))))
by_group_05 <- count_grouped(c("KO", "WT"), 0.5)
by_group_10 <- count_grouped(c("KO", "WT"), 1.0)
all_group_10 <- count_grouped(c("all", "all"), 1.0)
cat("peaks=", nrow(chromPeaks(xdata)), " one_per_group_0.5=", by_group_05,
    " one_per_group_1.0=", by_group_10, " combined_group_1.0=", all_group_10, "\n", sep = "")
stopifnot(nrow(chromPeaks(xdata)) > 0, by_group_05 == by_group_10, all_group_10 > 0)
cat("PASS\n")
