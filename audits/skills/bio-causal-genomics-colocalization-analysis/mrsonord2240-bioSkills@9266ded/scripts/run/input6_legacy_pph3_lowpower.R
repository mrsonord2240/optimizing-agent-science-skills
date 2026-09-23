# Input 6 -- Scope Boundary: NEW test (not in fix log) of the REVISED PP.H3-inflation
# trigger claim in SKILL.md: "2+ independent causal signals in moderate LD (r2 ~0.3-0.6)
# AND comparable effect sizes / limited power at the two signals" (the P1 fix added the
# power/effect-size clause). The pre-fix audit only showed r2-alone does NOT trigger
# inflation in a well-powered locus; it never tested whether the NEW, fuller condition
# (r2 in range + comparable effects + limited power) actually produces the claimed
# ambiguous PP.H3-dominant symptom. This input checks that.

library(coloc)
set.seed(777)
n_ind <- 4000
n_snps <- 300
positions <- sort(sample(40000000:41000000, n_snps))

rho <- 0.85
Sigma <- rho^abs(outer(1:n_snps, 1:n_snps, '-'))
Lchol <- chol(Sigma)
G <- matrix(rnorm(n_ind * n_snps), n_ind, n_snps) %*% Lchol
G <- scale(G)

## AR(1) LD decays with INDEX distance (rho^d), not raw bp -- pick two indices a
## fixed small distance apart (d=6 -> rho^6=0.85^6=0.377, squared r2~0.14; tuned
## by direct search below to land in the 0.3-0.6 r2 band the trigger text names).
causal1 <- 150
best_d <- which.min(abs(sapply(1:15, function(d) cor(G[, causal1], G[, causal1 + d])^2) - 0.45))
causal2 <- causal1 + best_d
r2_val <- cor(G[, causal1], G[, causal2])^2
cat(sprintf('PLANTED: causal1 idx %d, causal2 idx %d, r2=%.3f (target 0.3-0.6 band)\n', causal1, causal2, r2_val))

get_sumstats <- function(y, G) {
  beta <- se <- numeric(ncol(G))
  for (j in 1:ncol(G)) {
    fit <- summary(lm(y ~ G[, j]))$coefficients
    beta[j] <- fit[2, 1]; se[j] <- fit[2, 2]
  }
  list(beta = beta, se = se)
}

# Small effect sizes + SMALL eQTL N (limited power) -- the newly-added condition.
# GWAS driven by causal1 with a comparable-magnitude effect to what eQTL sees at causal2,
# and eQTL is underpowered (N=150, well under the Skill's own N<200 "underpowered" band).
n_eqtl_small <- 150
idx_small <- sample(1:n_ind, n_eqtl_small)

y_gwas <- 0.12 * G[, causal1] + rnorm(n_ind, 0, 1)          # comparable, modest effect
y_eqtl <- 0.12 * G[idx_small, causal2] + rnorm(n_eqtl_small, 0, 1)   # comparable effect, small N

gwas_ss <- get_sumstats(y_gwas, G)
eqtl_ss <- get_sumstats(y_eqtl, G[idx_small, , drop = FALSE])

snp_ids <- paste0('rs', 1:n_snps)

gwas_input <- list(beta = gwas_ss$beta, varbeta = gwas_ss$se^2, snp = snp_ids,
                    position = positions, type = 'quant', sdY = 1, N = n_ind)
eqtl_input <- list(beta = eqtl_ss$beta, varbeta = eqtl_ss$se^2, snp = snp_ids,
                    position = positions, type = 'quant', sdY = 1, N = n_eqtl_small)

res <- coloc.abf(dataset1 = gwas_input, dataset2 = eqtl_input, p1 = 1e-4, p2 = 1e-4, p12 = 5e-6)
print(res$summary)
cat(sprintf('\nPP.H3=%.4f PP.H4=%.4f (r2=%.3f, comparable modest effects, eQTL N=%d [underpowered])\n',
            res$summary['PP.H3.abf'], res$summary['PP.H4.abf'], r2_val, n_eqtl_small))

if (res$summary['PP.H3.abf'] > 0.5 && res$summary['PP.H4.abf'] < 0.5) {
  cat('RESULT: PP.H3-dominant / ambiguous -- consistent with the REVISED trigger claim (r2 in range + comparable/limited-power effects)\n')
} else if (res$summary['PP.H4.abf'] > 0.9 || res$summary['PP.H3.abf'] > 0.9) {
  cat('RESULT: resolved decisively (not ambiguous) -- would CONTRADICT the revised trigger claim under these exact conditions\n')
} else {
  cat('RESULT: intermediate / neither posterior dominant -- partially consistent with an "ambiguous" symptom\n')
}

# --- Follow-up: same r2/effect-size setup but moderate (not extreme) power, N=400 ---
n_eqtl_mod <- 400
idx_mod <- sample(1:n_ind, n_eqtl_mod)
y_eqtl_mod <- 0.12 * G[idx_mod, causal2] + rnorm(n_eqtl_mod, 0, 1)
eqtl_ss_mod <- get_sumstats(y_eqtl_mod, G[idx_mod, , drop = FALSE])
eqtl_input_mod <- list(beta = eqtl_ss_mod$beta, varbeta = eqtl_ss_mod$se^2, snp = snp_ids,
                        position = positions, type = 'quant', sdY = 1, N = n_eqtl_mod)
res_mod <- coloc.abf(dataset1 = gwas_input, dataset2 = eqtl_input_mod, p1 = 1e-4, p2 = 1e-4, p12 = 5e-6)
cat(sprintf('\n[Follow-up, N=%d]  PP.H1=%.4f PP.H3=%.4f PP.H4=%.4f (r2=%.3f)\n',
            n_eqtl_mod, res_mod$summary['PP.H1.abf'], res_mod$summary['PP.H3.abf'], res_mod$summary['PP.H4.abf'], r2_val))
