# Input 6 (Scope Boundary, NEW — not tested in the pre-fix audit at all) —
# Prompt: "You said PROPER is the most defensible route for pilot-based sizing. Actually
# run it on my pilot instead of just estimating dispersion by hand."
#
# Pre-fix: PROPER had ZERO code anywhere in the Skill (P1 finding, "no executable
# pattern"). The fix log claims a full estParam/RNAseq.SimOptions.2grp/runSims/
# comparePower block was added, including an undocumented workaround for a real
# PROPER::estParam bug on R>=4.0 (oldClass(X) <- "matrix"). Verify independently.
suppressPackageStartupMessages(library(PROPER))

pilot_counts <- as.matrix(read.csv("data/pilot_6v6_counts.csv", row.names = 1))
storage.mode(pilot_counts) <- "integer"

cat("=== Part A: confirm the bug SKILL.md documents actually fires without the workaround ===\n")
bug_result <- tryCatch({
  estParam(pilot_counts, type = 1)
  "NO ERROR -- the bug SKILL.md warns about did not reproduce on this PROPER/R version"
}, error = function(e) paste("ERROR (matches SKILL.md's documented bug):", conditionMessage(e)))
cat(bug_result, "\n")

cat("\n=== Part B: SKILL.md's workaround + full pipeline, run verbatim ===\n")
set.seed(20260918)
counts_mat <- pilot_counts
oldClass(counts_mat) <- "matrix"
params <- estParam(counts_mat, type = 1)
cat("estParam() succeeded with the workaround. Class of counts_mat before call:", class(counts_mat), "\n")
cat("params$seqDepth (first 3):", head(params$seqDepth, 3), "\n")

sim.opts <- RNAseq.SimOptions.2grp(ngenes = nrow(counts_mat), seqDepth = params$seqDepth,
                                    lBaselineExpr = params$lmean, lOD = params$lOD,
                                    p.DE = 0.05, lfc = log2(1.5), sim.seed = 20260918)
cat("RNAseq.SimOptions.2grp() succeeded.\n")

simres <- runSims(Nreps = c(3, 6, 10, 20), nsims = 20, sim.opts = sim.opts, DEmethod = "DESeq2")
cat("runSims() succeeded across Nreps = 3,6,10,20.\n")

powres <- comparePower(simres, alpha.type = "fdr", alpha.nominal = 0.05,
                       stratify.by = "expr", target.by = "lfc", delta = log2(1.5))
cat("comparePower() succeeded. Class of result:", class(powres), "\n")
cat("Average power by Nreps:\n")
print(powres$powerAveraged)

cat("\n=== Part C: does PROPER's own answer roughly track the ssizeRNA/edgeR answer for the same design? ===\n")
cat("(Not expected to match exactly -- different simulation engines/DE tools -- but should be the\n",
    " same order of magnitude, i.e. 'tens of replicates', not single digits, at fc=1.5/FDR 0.05/80%.)\n")
