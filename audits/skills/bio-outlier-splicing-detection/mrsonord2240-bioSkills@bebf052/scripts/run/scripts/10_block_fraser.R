# Run the SKILL.md "FRASER 2 Workflow" block VERBATIM (blocks/01_r.R) from <indir> (which holds bams/), then score against planted truth.
# usage: Rscript 10_block_fraser.R <indir> <blockfile> <synth> <tag> [patient_original_sample=S05] [mismatch_sample=S29]
suppressPackageStartupMessages({library(FRASER); library(BiocParallel)})
a <- commandArgs(TRUE); indir <- a[1]; blockf <- a[2]; synth <- a[3]; tag <- a[4]
pat_orig <- if (length(a) >= 5) a[5] else "S05"; mm <- if (length(a) >= 6) a[6] else "S29"
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))
source(file.path(here, "20_eval_lib.R"))
setwd(indir); unlink("fraser_workdir", recursive = TRUE)
cat("FRASER", as.character(packageVersion("FRASER")), "| running block:", blockf, "\n")
blk_err <- try(source(blockf, echo = FALSE), silent = TRUE)
if (inherits(blk_err, "try-error")) {
    cat("BLOCK ERROR (verbatim block stopped):", conditionMessage(attr(blk_err, "condition")), "\n")
} else {
    cat("block finished; bestQ =", bestQ(fds, "jaccard"), "; patient rows:", nrow(patient_results), "\n")
    print(as.data.frame(patient_results)[, intersect(c("seqnames", "start", "end", "sampleID", "padjust", "deltaPsi"), names(patient_results))])
}
eval_fds(fds, synth, rename = setNames(pat_orig, "PATIENT_001"), tag = tag, mismatch = mm)
