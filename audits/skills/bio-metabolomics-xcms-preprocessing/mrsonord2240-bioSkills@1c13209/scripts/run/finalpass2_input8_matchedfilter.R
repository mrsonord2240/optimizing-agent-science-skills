# Final-pass Phase 2 Input 8 (new) -- low-resolution alternative via MatchedFilterParam.
# Usage: F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh finalpass2_input8_matchedfilter.R
library(xcms)
library(MsExperiment)
library(BiocParallel)
register(SerialParam())

base <- "F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO"
files <- c(list.files(file.path(base, "KO"), pattern = "\\.CDF$", full.names = TRUE)[1:2],
           list.files(file.path(base, "WT"), pattern = "\\.CDF$", full.names = TRUE)[1:2])
raw <- readMsExperiment(spectraFiles = files, sampleData = data.frame(sample_group = c("KO", "KO", "WT", "WT")))
xdata <- findChromPeaks(raw, param = MatchedFilterParam(binSize = 0.1, fwhm = 30, snthresh = 10, steps = 2))
cat("matchedfilter_peaks=", nrow(chromPeaks(xdata)), " samples=", length(xdata), "\n", sep = "")
stopifnot(nrow(chromPeaks(xdata)) > 0, length(xdata) == 4)
cat("PASS\n")
