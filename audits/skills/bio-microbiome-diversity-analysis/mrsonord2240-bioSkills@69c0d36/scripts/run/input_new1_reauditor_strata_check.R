# Independent re-auditor fixture: NOT the fixer's/auditor's long_phyloseq.rds.
# Purpose: verify the new SKILL.md guidance -- adonis2(..., strata = SubjectID) for
# repeated-measures/pseudo-replicated designs -- is accurate, on a fresh synthetic dataset
# with a different seed, different subject/visit counts, and a *known* ground truth (no true
# arm effect; only within-subject correlation).
library(vegan)

set.seed(20260919)  # re-auditor's own seed, distinct from the fixer's

n_subjects <- 14
visits_per_subject <- 3
n_taxa <- 60
n_samples <- n_subjects * visits_per_subject

subject_id <- rep(paste0("Subj", seq_len(n_subjects)), each = visits_per_subject)
arm <- rep(sample(rep(c("placebo", "treatment"), length.out = n_subjects)), each = visits_per_subject)
visit <- rep(c("baseline", "week4", "week8"), times = n_subjects)

# Ground truth: NO real arm effect. Each subject has its own fixed random compositional
# baseline (Dirichlet-like via exp(rnorm)); all visits for that subject are noisy draws
# around the SAME baseline, regardless of arm. This is exactly the pseudo-replication trap:
# 3 correlated draws per subject masquerading as 3 independent samples.
subject_baseline <- matrix(exp(rnorm(n_subjects * n_taxa, mean = 0, sd = 1.2)),
                            nrow = n_subjects, ncol = n_taxa)
subject_baseline <- subject_baseline / rowSums(subject_baseline)

counts <- matrix(0, nrow = n_samples, ncol = n_taxa)
depth <- sample(8000:15000, n_samples, replace = TRUE)
for (i in seq_len(n_samples)) {
  subj_idx <- match(subject_id[i], paste0("Subj", seq_len(n_subjects)))
  # small per-visit compositional jitter around the subject's fixed baseline
  p <- subject_baseline[subj_idx, ] * exp(rnorm(n_taxa, sd = 0.25))
  p <- p / sum(p)
  counts[i, ] <- rmultinom(1, size = depth[i], prob = p)[, 1]
}
rownames(counts) <- paste0("S", seq_len(n_samples), "_", subject_id, "_", visit)
meta <- data.frame(SampleID = rownames(counts), SubjectID = subject_id, Arm = arm, Visit = visit)

cat("Samples:", n_samples, "| Subjects:", n_subjects, "| Taxa:", n_taxa, "\n")
cat("Ground truth: no real Arm effect; only within-subject correlation across visits.\n\n")

bc <- vegdist(counts, method = "bray")

naive <- adonis2(bc ~ Arm, data = meta, permutations = 999)
cat("Naive pooled PERMANOVA (Arm, all", n_samples, "visits treated as independent):\n")
print(naive)

strata_res <- adonis2(bc ~ Arm, data = meta, permutations = 999, strata = meta$SubjectID)
cat("\nRestricted-permutation PERMANOVA (strata = SubjectID):\n")
print(strata_res)

cat(sprintf("\nSUMMARY: naive R2=%.4f p=%.4g | strata R2=%.4f p=%.4g\n",
            naive$R2[1], naive$`Pr(>F)`[1], strata_res$R2[1], strata_res$`Pr(>F)`[1]))
