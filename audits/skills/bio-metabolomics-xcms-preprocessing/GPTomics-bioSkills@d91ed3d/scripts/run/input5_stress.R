# Input 5 (Stress/multi-part) -- "My trace metabolites disappear from the table on
# Orbitrap qTOF data regardless of snthresh; my grouping bw of 30 seems to be merging
# co-eluting peaks on UHPLC data; and I want to filter by QC CV<0.2 and D-ratio<0.5
# using pooled QC samples marked in my sample sheet. Diagnose and set parameters."
#
# Part A (trace-metabolite / bw diagnosis) is a reasoning-only response graded against
# SKILL.md's own Per-Method Failure Modes table -- no code to execute for a diagnosis.
# Part B (QC filterFeatures) IS executable. Honesty note: faahKO has no real pooled QC
# samples; WT is used here as a documented QC-index stand-in purely to test whether the
# Skill's RsdFilter/DratioFilter code pattern runs and produces a real filtered count.

library(xcms)
library(MsExperiment)

xdata <- readRDS("F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run/xdata_input1.rds")
cat("Loaded xdata:", nrow(featureDefinitions(xdata)), "features x", length(xdata), "samples\n")

qc <- sampleData(xdata)$sample_group == "WT"     # stand-in for real pooled QC
study <- sampleData(xdata)$sample_group == "KO"  # stand-in for real study samples
cat("QC-stand-in (WT) n =", sum(qc), "| study-stand-in (KO) n =", sum(study), "\n")

n_before <- nrow(featureDefinitions(xdata))
res_rsd <- tryCatch({
  xdata_f <- filterFeatures(xdata, filter = RsdFilter(threshold = 0.3, qcIndex = qc))
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("RsdFilter(threshold=0.3) ->", res_rsd, "\n")

if (identical(res_rsd, "OK")) {
  n_after_rsd <- nrow(featureDefinitions(xdata_f))
  cat("Features before RsdFilter:", n_before, "-> after:", n_after_rsd,
      "(", n_before - n_after_rsd, "dropped)\n")

  res_dratio <- tryCatch({
    xdata_f2 <- filterFeatures(xdata_f, filter = DratioFilter(threshold = 0.5, qcIndex = qc,
                                                                studyIndex = study))
    "OK"
  }, error = function(e) paste("ERROR:", conditionMessage(e)))
  cat("DratioFilter(threshold=0.5) ->", res_dratio, "\n")
  if (identical(res_dratio, "OK")) {
    n_after_dratio <- nrow(featureDefinitions(xdata_f2))
    cat("Features after RsdFilter:", n_after_rsd, "-> after DratioFilter:", n_after_dratio,
        "(", n_after_rsd - n_after_dratio, "further dropped)\n")
  }
}
cat("DONE\n")
