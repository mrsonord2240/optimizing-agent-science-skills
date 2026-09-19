# Skill Veto T3 check: does inferCNV::run() on identical input/params give
# identical output across two independent runs (no set.seed() is called
# anywhere in SKILL.md/usage-guide.md/examples/ despite HMM + Bayesian-network
# + Leiden-clustering-based subclustering steps in the pipeline)?
o1 <- readRDS("/mnt/openscience/audits/bio-single-cell-cnv-inference/run/infercnv_out_input1/run.final.infercnv_obj")
o2 <- readRDS("/mnt/openscience/audits/bio-single-cell-cnv-inference/run/infercnv_out_input1_rerun/run.final.infercnv_obj")

cat("expr.data identical:", isTRUE(all.equal(o1@expr.data, o2@expr.data)), "\n")
d <- o1@expr.data - o2@expr.data
cat("max abs diff:", max(abs(d)), " mean abs diff:", mean(abs(d)), "\n")

grp1 <- o1@tumor_subclusters
grp2 <- o2@tumor_subclusters
cat("tumor_subclusters identical structure:", isTRUE(all.equal(grp1, grp2)), "\n")

score1 <- colSums((o1@expr.data - 1)^2)
score2 <- colSums((o2@expr.data - 1)^2)
cat("cnv_score correlation run1 vs run2:", cor(score1, score2[names(score1)]), "\n")
cat("cnv_score max abs diff:", max(abs(score1 - score2[names(score1)])), "\n")

hmm1 <- read.table("/mnt/openscience/audits/bio-single-cell-cnv-inference/run/infercnv_out_input1/HMM_CNV_predictions.HMMi6.leiden.hmm_mode-subclusters.Pnorm_0.5.pred_cnv_regions.dat", header = TRUE)
hmm2 <- read.table("/mnt/openscience/audits/bio-single-cell-cnv-inference/run/infercnv_out_input1_rerun/HMM_CNV_predictions.HMMi6.leiden.hmm_mode-subclusters.Pnorm_0.5.pred_cnv_regions.dat", header = TRUE)
cat("HMM predicted regions run1:", nrow(hmm1), " run2:", nrow(hmm2), "\n")
cat("HMM state calls identical:", isTRUE(all.equal(hmm1$state, hmm2$state)), "\n")
