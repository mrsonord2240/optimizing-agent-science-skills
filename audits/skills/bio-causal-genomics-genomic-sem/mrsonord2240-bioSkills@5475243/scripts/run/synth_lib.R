# Shared helpers to build synthetic ldsc()-shaped covstruc objects (list(V=V,S=S,I=I,N=N,m=m))
# so we can test commonfactor()/usermodel()/commonfactorGWAS() directly without a live
# ldsc() run (no eur_w_ld_chr / munged sumstats needed). All data below is SYNTHETIC.
# Reused verbatim from the pre-fix audit's own generators (regression continuity) --
# F:\OpenScience\audits\_pre-fix-20260917c\bio-causal-genomics-genomic-sem\run\synth_lib.R.

vech_len <- function(k) k * (k + 1) / 2

build_one_factor_S <- function(loadings, h2) {
  k <- length(loadings)
  stopifnot(length(h2) == k)
  S <- matrix(0, k, k)
  for (i in 1:k) for (j in 1:k) {
    if (i == j) {
      S[i, j] <- h2[i]
    } else {
      S[i, j] <- loadings[i] * loadings[j] * sqrt(h2[i] * h2[j])
    }
  }
  S
}

build_V <- function(k, diag_var = 5e-4, overlap_frac = 0) {
  n <- vech_len(k)
  V <- diag(diag_var, n)
  if (overlap_frac > 0) {
    off <- diag_var * overlap_frac
    for (i in 1:(n - 1)) for (j in (i + 1):n) V[i, j] <- V[j, i] <- off
  }
  V
}

build_I <- function(k, intercept = 1.0, cross = 0.05) {
  I <- matrix(cross, k, k)
  diag(I) <- intercept
  I
}

name_S <- function(S, trait_names) {
  colnames(S) <- rownames(S) <- trait_names
  S
}

check_pd <- function(mat, label) {
  ev <- eigen(mat, symmetric = TRUE, only.values = TRUE)$values
  cat(sprintf("  %s eigenvalues: min=%.6g max=%.6g -> %s\n", label, min(ev), max(ev),
              ifelse(min(ev) > 0, "positive definite", "NOT positive definite")))
  invisible(min(ev) > 0)
}
