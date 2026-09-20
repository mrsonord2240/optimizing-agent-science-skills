# The Skill's SKILL.md "FRASER 2.0 Workflow" block, run on the synthetic cohort, then scored against the planted truth.
# Only deviations from the Skill text: (1) DataFrame() wrapper [documented crash otherwise], (2) BPPARAM by platform, (3) args.
# Usage: Rscript 30_workflow.R <bamdir> <workdir> <synth> <tag> <q|NA> [corr:PCA|AE|default] [ncpu]
suppressPackageStartupMessages({library(FRASER); library(BiocParallel)})
a <- commandArgs(TRUE); bamdir <- a[1]; wd <- a[2]; synth <- a[3]; tag <- a[4]
q <- if (a[5] == "NA") NA else as.integer(a[5]); corr <- if (length(a) >= 6) a[6] else "default"; ncpu <- if (length(a) >= 7) as.integer(a[7]) else 8
source(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))), "20_eval_lib.R"))
bp <- if (.Platform$OS.type == "windows") SerialParam() else MulticoreParam(ncpu)
bam_files <- list.files(bamdir, pattern = '.bam$', full.names = TRUE)
sample_table <- data.frame(sampleID = gsub('.bam', '', basename(bam_files)), bamFile = bam_files, pairedEnd = TRUE)
settings <- FraserDataSet(colData = S4Vectors::DataFrame(sample_table), workingDir = wd, name = 'rare_disease_cohort')
settings <- countRNAData(settings, BPPARAM = bp)
fds <- calculatePSIValues(settings)
fds <- filterExpressionAndVariability(fds, minDeltaPsi = 0.0, minExpressionInOneSample = 20, quantile = 0.05, quantileMinExpression = 1)
cat("after filter: junctions =", nrow(fds), "\n")
fitMetrics(fds) <- 'jaccard'
currentType(fds) <- 'jaccard'
if (is.na(q)) { cat("q not given: estimating\n") }
args <- list(fds, q = c(jaccard = q), BPPARAM = bp)
if (corr != "default") args$correction <- corr
fds <- do.call(FRASER, args)
saveFraserDataSet(fds, dir = wd, name = paste0("fitted_", tag))
cat("saved fitted fds\n")
eval_fds(fds, synth, tag = tag)
