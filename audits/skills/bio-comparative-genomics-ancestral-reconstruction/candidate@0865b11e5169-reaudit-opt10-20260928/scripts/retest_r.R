#!/usr/bin/env Rscript
suppressPackageStartupMessages(library(ape))
suppressPackageStartupMessages(library(phytools))
suppressPackageStartupMessages(library(geiger))
cand <- "/mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction"
root <- "/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction"
out <- "/mnt/openscience/audits/bio-comparative-genomics-ancestral-reconstruction/reaudit-opt10-20260928/evidence"
run <- file.path(out, "r-run")
dir.create(run, recursive=TRUE, showWarnings=FALSE)

cat("ENV", R.version.string, "ape", as.character(packageVersion("ape")),
    "phytools", as.character(packageVersion("phytools")),
    "geiger", as.character(packageVersion("geiger")),
    "corHMM", as.character(packageVersion("corHMM")),
    "OUwie", as.character(packageVersion("OUwie")), "\n")

# Exact shipped stochastic script, fresh deterministic fixture, explicit caller seed.
set.seed(314159)
tree <- rtree(30); tree$tip.label <- sprintf("rt_%02d", seq_len(30))
x <- setNames(rep(c("0", "1", "1"), length.out=30), tree$tip.label)
write.tree(tree, file.path(run, "species_tree.nwk"))
write.csv(data.frame(state=x, row.names=names(x)), file.path(run, "traits.csv"))
old <- setwd(run)
args <- c("--seed=20260928")
source(file.path(cand, "scripts/stochastic_mapping.R"), local=.GlobalEnv)
stopifnot(result_metadata$seed == 20260928, length(smaps) == 1000,
          nrow(node_pp) >= tree$Nnode, nrow(hmm_fit$states) >= tree$Nnode)
cat("STOCHASTIC", result_metadata$selected_model, "tips", result_metadata$taxa,
    "maps", length(smaps), "node rows", nrow(node_pp), "seed", result_metadata$seed, "\n")
setwd(old)

# Taxon reconciliation rejects both missing and extra rows with actionable names.
bad <- setNames(rep(c("0", "1"), length.out=5), paste0("rt_", sprintf("%02d", 1:5)))
write.csv(data.frame(state=bad, row.names=names(bad)), file.path(run, "traits.csv"))
old <- setwd(run)
err <- tryCatch({ source(file.path(cand, "scripts/stochastic_mapping.R"), local=new.env(parent=.GlobalEnv), chdir=FALSE); "ACCEPTED" },
                error=function(e) conditionMessage(e))
stopifnot(grepl("rt_06", err), grepl("Trait-only taxa: none", err), grepl("Align row names", err))
cat("STOCHASTIC_MISMATCH", err, "\n")
setwd(old)

# BM is exercised on an independently generated Brownian 35-tip fixture.
set.seed(20260928)
tree <- rtree(35); tree$tip.label <- sprintf("bm_%02d", seq_len(35))
traits <- data.frame(mass=fastBM(tree, sig2=.3), row.names=tree$tip.label)
source(file.path(cand, "scripts/continuous_trait_asr.R"), local=.GlobalEnv)
stopifnot(best == "BM", length(result$estimates) == tree$Nnode,
          nrow(result$uncertainty) == tree$Nnode,
          all(is.finite(aic_tbl$AIC)))
cat("BM", "selected", best, "nodes", length(result$estimates),
    "95pct interval rows", nrow(result$uncertainty), "all AIC finite", all(is.finite(aic_tbl$AIC)), "\n")

# OUwie single-regime diagnostic is independently reproduced, then actual
# OUwie.anc is exercised through the exact candidate's fitted-object route.
set.seed(20260928)
tree <- rtree(24); tree$tip.label <- sprintf("ou_%02d", seq_len(24))
tree <- force.ultrametric(tree, method="extend")
traits <- setNames(fastBM(tree, a=2, sig2=.2), tree$tip.label)
actual_fitContinuous <- geiger::fitContinuous
fitContinuous <- function(tree, trait, model, ...) list(opt=list(aic=if (model == "OU") 1 else 2))
source(file.path(cand, "scripts/continuous_trait_asr.R"), local=.GlobalEnv)
fitContinuous <- actual_fitContinuous
stopifnot(best == "OU", result$status == "exploratory_point_estimates_only",
          is.null(result$uncertainty), grepl("not provided", result$uncertainty_type),
          length(result$estimates) > 0)
cat("OU", result$status, "fitted OUwie object", inherits(ou_fit, "OUwie"),
    "points", length(result$estimates), "uncertainty", result$uncertainty_type, "\n")

ou_data <- data.frame(species=tree$tip.label, regime=rep("1", length(traits)), trait=unname(traits))
diag <- tryCatch({OUwie::OUwie(tree, ou_data, model="OU1", simmap.tree=FALSE, quiet=TRUE); "ACCEPTED"},
                 error=function(e) conditionMessage(e))
cat("OUWIE_DEFAULT_IDENTIFY", diag, "\n")

# Each transformed-model winner must refuse before emitting original-tree results.
actual_fitContinuous <- geiger::fitContinuous
for (winner in c("EB", "lambda", "kappa", "delta")) {
  set.seed(2718)
  tree <- rtree(18); tree$tip.label <- sprintf("%s_%02d", winner, seq_len(18))
  traits <- setNames(fastBM(tree), tree$tip.label)
  fitContinuous <- local({selected <- winner; function(tree, trait, model, ...) list(opt=list(aic=if (model == selected) 1 else 2))})
  err <- tryCatch({source(file.path(cand, "scripts/continuous_trait_asr.R"), local=.GlobalEnv); "ACCEPTED"},
                  error=function(e) conditionMessage(e))
  stopifnot(grepl(paste0("Selected ", winner, " model is not implemented"), err),
            grepl("No original-tree fastAnc/contMap result was substituted", err))
  cat("TRANSFORMED_WINNER", winner, "REFUSED", err, "\n")
}
fitContinuous <- actual_fitContinuous

# Missing seed stops before attempting to open its input files.
missing_seed <- system2(file.path(root, "conda-env/bin/Rscript"),
                        args=c(file.path(cand, "scripts/stochastic_mapping.R")),
                        stdout=TRUE, stderr=TRUE)
code <- attr(missing_seed, "status"); if (is.null(code)) code <- 0L
stopifnot(code != 0L, any(grepl("exactly one reproducibility seed", missing_seed)))
cat("MISSING_SEED", "exit", code, "message", paste(missing_seed, collapse=" | "), "\n")

writeLines(capture.output(sessionInfo()), file.path(out, "r-sessionInfo.txt"))
