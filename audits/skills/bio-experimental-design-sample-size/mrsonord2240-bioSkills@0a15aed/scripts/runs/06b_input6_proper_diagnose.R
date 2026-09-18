# Follow-up diagnosis: SKILL.md's comparePower block prints powres$powerAveraged,
# which returned NULL in the previous run. Inspect the actual structure PROPER 1.38.0
# returns from comparePower() to determine whether this is a real field-name bug in
# the shipped code, or user error.
suppressPackageStartupMessages(library(PROPER))

pilot_counts <- as.matrix(read.csv("data/pilot_6v6_counts.csv", row.names = 1))
storage.mode(pilot_counts) <- "integer"

set.seed(20260918)
counts_mat <- pilot_counts
oldClass(counts_mat) <- "matrix"
params <- estParam(counts_mat, type = 1)
sim.opts <- RNAseq.SimOptions.2grp(ngenes = nrow(counts_mat), seqDepth = params$seqDepth,
                                    lBaselineExpr = params$lmean, lOD = params$lOD,
                                    p.DE = 0.05, lfc = log2(1.5), sim.seed = 20260918)
simres <- runSims(Nreps = c(3, 6, 10, 20), nsims = 10, sim.opts = sim.opts, DEmethod = "DESeq2")
powres <- comparePower(simres, alpha.type = "fdr", alpha.nominal = 0.05,
                       stratify.by = "expr", target.by = "lfc", delta = log2(1.5))

cat("=== names(powres) ===\n")
print(names(powres))
cat("\n=== str(powres), 2 levels ===\n")
str(powres, max.level = 2)
cat("\n=== Does 'powerAveraged' exist anywhere? ===\n")
cat("'powerAveraged' %in% names(powres):", "powerAveraged" %in% names(powres), "\n")
cat("\n=== What SKILL.md's code actually prints ===\n")
print(powres$powerAveraged)
cat("\n=== The ACTUAL correct accessor (if different) ===\n")
if ("powerAvg" %in% names(powres)) print(powres$powerAvg)
