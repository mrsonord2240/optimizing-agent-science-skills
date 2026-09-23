# Final-pass Phase 2 Input 9 (new) -- direct pooled-QC subset Obiwarp path.
# Usage: F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh finalpass2_input9_obiqc.R
library(xcms)
library(MsExperiment)
library(BiocParallel)
register(SerialParam())

base <- "F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO"
ko <- list.files(file.path(base, "KO"), pattern = "\\.CDF$", full.names = TRUE)[1:2]
wt <- list.files(file.path(base, "WT"), pattern = "\\.CDF$", full.names = TRUE)[1:4]
files <- c(ko, wt)
pd <- data.frame(sample_group = c("KO", "KO", "QC", "QC", "WT", "WT"),
                 sample_type = c("Study", "Study", "QC", "QC", "Study", "Study"))
raw <- readMsExperiment(spectraFiles = files, sampleData = pd)
xdata <- findChromPeaks(raw, param = CentWaveParam(ppm = 25, peakwidth = c(20, 80), snthresh = 10,
  prefilter = c(3, 1000), noise = 1000, mzdiff = -0.001, integrate = 1L, mzCenterFun = "wMean"))
qc_idx <- which(sampleData(xdata)$sample_type == "QC")
xdata <- adjustRtime(xdata, param = ObiwarpParam(binSize = 0.6, subset = qc_idx, subsetAdjust = "average"))
xdata <- groupChromPeaks(xdata, param = PeakDensityParam(sampleGroups = sampleData(xdata)$sample_group,
  bw = 30, minFraction = 0.5, minSamples = 1, binSize = 0.025))
cat("peaks=", nrow(chromPeaks(xdata)), " qc_subset_n=", length(qc_idx),
    " features=", nrow(featureDefinitions(xdata)), "\n", sep = "")
stopifnot(length(qc_idx) == 2, nrow(chromPeaks(xdata)) > 0, nrow(featureDefinitions(xdata)) > 0)
cat("PASS\n")
