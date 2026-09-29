root <- "/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction"
cand <- "/mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction"
evidence <- file.path(root, "evidence")
dir.create(file.path(root, "runs", "r-stochastic"), recursive=TRUE, showWarnings=FALSE)

sink(file.path(evidence, "r-surfaces.log"), split=TRUE)
on.exit(sink(), add=TRUE)
set.seed(20260928)
suppressPackageStartupMessages(library(ape))

# Valid discrete fixture with 30 tips and both states; the exact candidate reads these files.
tree <- rtree(30)
tree$tip.label <- sprintf("taxon_%02d", seq_len(30))
states <- rep(c(0, 1, 1), length.out=30)
traits <- data.frame(state=states, row.names=tree$tip.label)
write.tree(tree, file.path(root, "runs", "r-stochastic", "species_tree.nwk"))
write.csv(traits, file.path(root, "runs", "r-stochastic", "traits.csv"))
old <- setwd(file.path(root, "runs", "r-stochastic")); on.exit(setwd(old), add=TRUE)
set.seed(20260928)
source(file.path(cand, "scripts", "stochastic_mapping.R"), local=.GlobalEnv)
stopifnot(best_model %in% c("ER", "SYM", "ARD"), length(smaps)==1000,
          nrow(node_pp)>=tree$Nnode, nrow(hmm_fit$states)>=tree$Nnode)
cat("stochastic_best_model", best_model, "\n")
cat("stochastic_maps", length(smaps), "node_pp_rows", nrow(node_pp), "corhmm_state_rows", nrow(hmm_fit$states), "\n")

# Valid continuous fixture; exact candidate receives its declared context objects.
set.seed(20260928)
tree <- rtree(35)
tree$tip.label <- sprintf("species_%02d", seq_len(35))
trait_values <- phytools::fastBM(tree, sig2=0.3)
traits <- data.frame(mass=trait_values, row.names=tree$tip.label)
source(file.path(cand, "scripts", "continuous_trait_asr.R"), local=.GlobalEnv)
stopifnot(nrow(aic_tbl)==6, all(is.finite(aic_tbl$AIC)), best %in% models,
          is.finite(lambda_fit$lambda), is.finite(K_fit$K))
if (best == "BM") stopifnot(length(asr$ace)==tree$Nnode)
if (!best %in% c("BM", "OU")) stopifnot(!is.null(asr_contmap$ace))
cat("continuous_best_model", best, "lambda", lambda_fit$lambda, "K", K_fit$K, "\n")
print(aic_tbl)

# Current direct interfaces advertised outside the extracted scripts.
stopifnot(packageVersion("ape") >= "5.8", packageVersion("phytools") >= "2.3",
          packageVersion("geiger") >= "2.0.11", packageVersion("phangorn") >= "2.12")
cat("package_versions\n")
for (p in c("ape","phytools","geiger","corHMM","phangorn","OUwie","bayou","RPANDA")) {
  cat(p, if (requireNamespace(p, quietly=TRUE)) as.character(packageVersion(p)) else "UNAVAILABLE", "\n")
}

# Adversarial contract: candidate does not reconcile a missing trait row itself.
bad_dir <- file.path(root, "runs", "r-stochastic-bad-taxa")
dir.create(bad_dir, recursive=TRUE, showWarnings=FALSE)
bad_tree <- rtree(6); bad_tree$tip.label <- paste0("b", 1:6)
write.tree(bad_tree, file.path(bad_dir, "species_tree.nwk"))
write.csv(data.frame(state=c(0,1,0,1,0), row.names=paste0("b",1:5)), file.path(bad_dir,"traits.csv"))
bad <- tryCatch({
  old2 <- setwd(bad_dir); on.exit(setwd(old2), add=TRUE)
  source(file.path(cand,"scripts","stochastic_mapping.R"), local=new.env(parent=.GlobalEnv))
  "accepted"
}, error=function(e) paste(class(e)[1], conditionMessage(e)))
cat("bad_taxa_outcome", bad, "\n")

saveRDS(list(best_model=best_model, node_pp=node_pp, aic_tbl=aic_tbl,
             continuous_best=best, lambda=lambda_fit$lambda, K=K_fit$K,
             bad_taxa_outcome=bad), file.path(evidence, "r-surfaces.rds"))

