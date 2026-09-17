# NEW INPUT 9 (this audit). Exercises SKILL.md's "Higher-Order / Bifactor / p-Factor
# Models" section, which no pre-fix input covered (those covered commonfactor,
# usermodel 2-factor, commonfactorGWAS, userGWAS, and 2-trait under-identification only).
# Uses usermodel() with the Skill's own hierarchical p-factor template VERBATIM
# (INT/EXT/THT first-order factors -> second-order p), including THT's 2-indicator
# sub-block exactly as SKILL.md writes it.
#
# "Fit a psychiatric p-factor model: INT =~ anxiety+depression+neuroticism,
# EXT =~ ADHD+alcohol+substance-use, THT =~ schizophrenia+bipolar, second-order
# p =~ INT+EXT+THT. Report first- and second-order standardized loadings and tell me
# if the p-factor is well supported."
#
# Planted: INT loadings 0.70/0.75/0.60; EXT loadings 0.65/0.70/0.55; THT loadings
# 0.75/0.65; second-order p->INT=0.60, p->EXT=0.50, p->THT=0.55 (implied first-order
# factor correlations rF_ij = p_i * p_j via the shared p, e.g. rF(INT,EXT)=0.30).
#
# A first attempt at this input (kept below as "PRELIMINARY") used only 2 first-order
# factors (INT, EXT feeding p) -- which turns out to itself violate the Skill's own
# ">=3 indicators to identify a factor" rule, recursively applied at the second order
# (a 2-indicator p is structurally the same under-identification as Input 7's 2-trait
# common factor). That was a bug in the test design, not a finding about the Skill; the
# MAIN test below uses the Skill's actual 3-factor (INT/EXT/THT) template, where THT's
# own 2 indicators are legitimately identified via cross-factor covariances with the
# well-identified INT/EXT blocks (the standard "2-indicator rule" in SEM identification
# theory) -- exactly what SKILL.md's own example relies on without stating the rule.
source("synth_lib.R")
library(GenomicSEM)

cat("=== INPUT 9a (PRELIMINARY / EDGE CASE): 2-factor p (INT,EXT only) -- expected under-identified ===\n")
traits2 <- c("t_anx","t_dep","t_neuro","t_adhd","t_alc","t_subst")
h2_2 <- c(0.08, 0.09, 0.07, 0.06, 0.05, 0.07)
load_int <- c(0.70, 0.75, 0.60)
load_ext <- c(0.65, 0.70, 0.55)
p_int <- 0.60; p_ext <- 0.50
build_pfactor_S <- function(trait_names, h2, loads_by_factor, fac_of_trait, p_by_factor) {
  k <- length(trait_names)
  load_vec <- unlist(loads_by_factor)
  nfac <- length(p_by_factor)
  R <- diag(1, k)
  for (i in 1:k) for (j in 1:k) if (i != j) {
    phi <- if (fac_of_trait[i] == fac_of_trait[j]) 1 else p_by_factor[fac_of_trait[i]] * p_by_factor[fac_of_trait[j]]
    R[i, j] <- load_vec[i] * load_vec[j] * phi
  }
  S <- diag(sqrt(h2)) %*% R %*% diag(sqrt(h2))
  name_S(S, trait_names)
}
S2 <- build_pfactor_S(traits2, h2_2, list(load_int, load_ext), c(1,1,1,2,2,2), c(p_int, p_ext))
covstruc2 <- list(V = build_V(6, diag_var = 3e-4), S = S2, I = build_I(6))
model2 <- '
    INT =~ NA*t_anx + t_dep + t_neuro
    EXT =~ NA*t_adhd + t_alc + t_subst
    p =~ NA*INT + EXT
    INT ~~ 1*INT
    EXT ~~ 1*EXT
    p ~~ 1*p
'
uf2 <- tryCatch(usermodel(covstruc = covstruc2, model = model2, estimation = "ML"),
                error = function(e) { cat("ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(uf2)) {
  cat("Ran (with warnings expected -- see below); CFI/chisq on an exact-fit S can look",
      "perfect even when the information matrix is singular:\n")
  print(uf2$modelfit)
}

cat("\n=== INPUT 9b (MAIN TEST): SKILL.md's literal 3-factor p-model (INT/EXT/THT -> p) ===\n")
traits3 <- c("t_anx","t_dep","t_neuro","t_adhd","t_alc","t_subst","t_scz","t_bp")
h2_3 <- c(0.08, 0.09, 0.07, 0.06, 0.05, 0.07, 0.06, 0.05)
load_tht <- c(0.75, 0.65)
p_tht <- 0.55
S3 <- build_pfactor_S(traits3, h2_3, list(load_int, load_ext, load_tht), c(1,1,1,2,2,2,3,3),
                       c(p_int, p_ext, p_tht))
check_pd(S3, "S3")
covstruc3 <- list(V = build_V(8, diag_var = 2e-4), S = S3, I = build_I(8))

model3 <- '
    INT =~ NA*t_anx + t_dep + t_neuro
    EXT =~ NA*t_adhd + t_alc + t_subst
    THT =~ NA*t_scz + t_bp
    p =~ NA*INT + EXT + THT
    INT ~~ 1*INT
    EXT ~~ 1*EXT
    THT ~~ 1*THT
    p ~~ 1*p
'

for (est in c("DWLS", "ML")) {
  cat(sprintf("\n--- estimation='%s' ---\n", est))
  uf <- tryCatch(usermodel(covstruc = covstruc3, model = model3, estimation = est),
                 error = function(e) { cat(est, "ERROR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(uf)) {
    cat("SUCCEEDED.\n")
    print(uf$modelfit)
    std_col <- if ("Standardized_Est" %in% names(uf$results)) "Standardized_Est" else "STD_Genotype"
    first_order <- uf$results[uf$results$op == "=~" & uf$results$lhs %in% c("INT","EXT","THT"), ]
    second_order <- uf$results[uf$results$op == "=~" & uf$results$lhs == "p", ]
    planted_first <- c(load_int, load_ext, load_tht)
    print(data.frame(path = paste(first_order$lhs, "=~", first_order$rhs),
                      recovered = round(as.numeric(first_order[[std_col]]), 3),
                      planted = planted_first))
    print(data.frame(path = paste(second_order$lhs, "=~", second_order$rhs),
                      recovered = round(as.numeric(second_order[[std_col]]), 3),
                      planted = c(p_int, p_ext, p_tht)))
    cfi <- uf$modelfit$CFI
    max_err <- max(abs(as.numeric(first_order[[std_col]]) - planted_first))
    cat(sprintf("%s: CFI=%.4f; max abs error on first-order loadings vs planted = %.4f\n", est, cfi, max_err))
  } else {
    cat(sprintf("%s: FAILED -- p-factor pathway is non-functional under this estimator.\n", est))
  }
}
