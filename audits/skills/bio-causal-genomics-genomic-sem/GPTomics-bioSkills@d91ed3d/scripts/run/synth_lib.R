# Shared helpers to build synthetic ldsc()-shaped covstruc objects (list(V=V,S=S,I=I,N=N,m=m))
# so we can test commonfactor()/usermodel()/commonfactorGWAS() directly without a live
# ldsc() run (no eur_w_ld_chr / munged sumstats needed). All data below is SYNTHETIC.
# Verified against GenomicSEM 0.0.5 internals: commonfactor()/usermodel() read
# covstruc[[1]] as V (sampling covariance of vech(S), dim k*(k+1)/2) and covstruc[[2]] as S
# (genetic covariance, k x k). commonfactorGWAS() additionally reads covstruc[[3]] as I
# (LDSC intercept matrix, k x k) and expects SNPs columns SNP,A1,A2,MAF,beta.<trait>,se.<trait>.

vech_len <- function(k) k * (k + 1) / 2

# Build a k-trait genetic covariance matrix S implied by a single common factor with
# standardized loadings `loadings` (length k), on the genetic-covariance (not correlation)
# scale, with SNP-heritability h2 per trait so that S[i,i] = h2[i].
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

# Small, well-behaved sampling covariance V for vech(S): diagonal dominant, tiny positive
# off-diagonal noise scaled to `overlap_frac` of the diagonal (mimics partial sample overlap).
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
