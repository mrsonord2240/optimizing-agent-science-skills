# Input 8 (NEW input, not in the pre-fix audit) -- "This run is off an older low-resolution
# quadrupole instrument, mostly profile-quality centroiding. What xcms peak-picking should I
# use?"
#
# Tests a Decision Tree row NEVER exercised by the pre-fix audit's 7 inputs (which only ever
# used CentWaveParam): "Low-res / quadrupole / profile-only -> MatchedFilterParam -- Model-
# peak on binned EICs tolerates poor resolution." This is real, syntactic, executed evidence
# for a code path the fixer was never scored on and could not have specifically targeted.

library(xcms)
library(MsExperiment)

base <- "F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO"
ko_files <- list.files(file.path(base, "KO"), pattern = "\\.CDF$", full.names = TRUE)[1:2]
wt_files <- list.files(file.path(base, "WT"), pattern = "\\.CDF$", full.names = TRUE)[1:2]
cdfs <- c(ko_files, wt_files)
pd <- data.frame(sample_name = sub("\\.CDF$", "", basename(cdfs)),
                 sample_group = c("KO", "KO", "WT", "WT"))
cat("Files (low-res simulation, 2 KO + 2 WT):", paste(basename(cdfs), collapse=", "), "\n")

raw <- readMsExperiment(spectraFiles = cdfs, sampleData = pd)

# MatchedFilterParam per SKILL.md's Decision Tree row for low-res/quadrupole data.
# binSize defaults to 0.1 m/z per the Skill's Common Errors table
# ("matchedFilter (m/z, 0.1)"); fwhm left at the package default and only steepness/snthresh
# tuned for a broad-peak HPLC-style run consistent with Input 1's chromatography.
mfp <- MatchedFilterParam(binSize = 0.1, fwhm = 30, snthresh = 10, steps = 2)
res <- tryCatch({
  t0 <- Sys.time()
  xdata8 <- findChromPeaks(raw, param = mfp)
  dt <- round(as.numeric(Sys.time() - t0, units = "secs"), 1)
  list(status = "OK", peaks = nrow(chromPeaks(xdata8)), secs = dt)
}, error = function(e) list(status = paste("ERROR:", conditionMessage(e))))

if (identical(res$status, "OK")) {
  cat("findChromPeaks(MatchedFilterParam(binSize=0.1, fwhm=30, snthresh=10)) took",
      res$secs, "s\n")
  cat("Peaks detected via MatchedFilterParam:", res$peaks, "\n")
} else {
  cat("findChromPeaks(MatchedFilterParam(...)) result:", res$status, "\n")
}
cat("DONE\n")
