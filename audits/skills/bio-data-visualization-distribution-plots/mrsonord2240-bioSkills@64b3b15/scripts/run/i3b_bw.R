# Input 3b: does bw='SJ' beat the default nrd0 at showing bimodality? 300 simulated draws per condition. SYNTHETIC mixtures, labelled.
suppressMessages(library(ggplot2))
cat("ggplot2", as.character(packageVersion("ggplot2")), "\n")
nmodes <- function(v, bw) { d <- try(density(v, bw=bw), silent=TRUE); if (inherits(d, "try-error")) return(NA_integer_)
  y <- d$y; idx <- which(diff(sign(diff(y))) == -2) + 1
  if (length(idx) <= 1) return(length(idx))
  keep <- sapply(idx, function(i) { h <- idx[y[idx] > y[i]]; if (!length(h)) return(TRUE); j <- h[which.min(abs(h - i))]; (y[i] - min(y[min(i,j):max(i,j)])) >= 0.1 * max(y) }); sum(keep) }
sim <- function(n, sep, reps = 300) { r <- replicate(reps, { set.seed(NULL); v <- c(rnorm(n/2, 0, 1), rnorm(n/2, sep, 1)); c(nrd0=nmodes(v,"nrd0"), nrd=nmodes(v,"nrd"), SJ=nmodes(v,"SJ"), ucv=nmodes(v,"ucv")) }); rowMeans(r == 2, na.rm=TRUE) }
set.seed(123)
grid <- expand.grid(n=c(30, 100, 400), sep=c(2, 2.5, 3, 4))
res <- do.call(rbind, lapply(seq_len(nrow(grid)), function(i) data.frame(n=grid$n[i], sep=grid$sep[i], t(round(sim(grid$n[i], grid$sep[i]), 2)))))
cat("Fraction of 300 draws in which the density shows exactly 2 prominent modes (equal-weight mixture, sd 1, separation 'sep'):\n"); print(res)
cat("Mean across the grid: nrd0", round(mean(res$nrd0),3), " nrd (Scott)", round(mean(res$nrd),3), " SJ", round(mean(res$SJ),3), "\n")
cat("SJ better than nrd0 in", sum(res$SJ > res$nrd0), "cells; worse in", sum(res$SJ < res$nrd0), "; equal in", sum(res$SJ == res$nrd0), "of", nrow(res), "\n")
cat("nrd (Scott) at least as good as nrd0 (i.e. oversmooths less) in", sum(res$nrd >= res$nrd0), "of", nrow(res), "cells (SKILL says it should)\n")

# SJ on zero-inflated clusters WITHOUT an all-zero cluster
set.seed(42)
mk <- function(n, pz) { z <- runif(n) < pz; ifelse(z, 0, round(rlnorm(n, 1.2, 0.35), 2)) }
sc <- rbind(data.frame(cluster="C1", expression=mk(300, 0.6)), data.frame(cluster="C2", expression=mk(250, 0.2)), data.frame(cluster="C3", expression=mk(5, 0.4)))
w <- character(); p <- withCallingHandlers({ p <- ggplot(sc, aes(cluster, expression, fill=cluster)) + geom_violin(trim=FALSE, bw="SJ"); ggsave("out/i3b_sc_sj_no_allzero.png", p, width=5, height=3.5, dpi=100); p }, warning=function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") })
cat("SJ, three clusters, none all-identical: warnings =", if (length(w)) paste(w, collapse=" || ") else "none", "\n")
vd <- layer_data(p, 1); vd <- if ("quantile" %in% names(vd)) vd[is.na(vd$quantile),] else vd
cat("drawn groups:", paste(sort(unique(vd$group)), collapse=","), "\n")
# a cluster whose values are 90% ties
set.seed(5); tie <- data.frame(g="T", v=c(rep(0, 90), round(rlnorm(10, 1.2, .3), 2)))
r <- try(bw.SJ(tie$v), silent=TRUE); cat("bw.SJ on 90% zeros n=100:", if (inherits(r, "try-error")) conditionMessage(attr(r, "condition")) else round(r, 4), "\n")
r <- try(bw.SJ(c(rep(0, 60), round(rlnorm(40, 1.2, .3), 2))), silent=TRUE); cat("bw.SJ on 60% zeros n=100:", if (inherits(r, "try-error")) conditionMessage(attr(r, "condition")) else round(r, 4), "\n")
