# What does ComputePSI(CoverageThreshold=10) actually threshold on? Compare the NA pattern of marvel$PSI$SE (planted set, 4800 cell-event pairs) with two candidate rules.
suppressMessages({library(MARVEL); library(data.table); library(Seurat)})
setwd('F:/OpenScience/audits/bio-single-cell-splicing/run/out/in4_planted'); options(warn = -1)
invisible(capture.output(source('F:/OpenScience/audits/bio-single-cell-splicing/run/blocks/S04_r.R', echo = FALSE)))
psi <- marvel$PSI$SE; rownames(psi) <- psi$tran_id; cells <- setdiff(colnames(sj), 'coord.intron'); sjm <- as.data.frame(sj); rownames(sjm) <- sjm$coord.intron
res_ <- list(); 
for (tid in rownames(psi)) { p <- strsplit(strsplit(tid, '@')[[1]], ':'); e <- lapply(p, function(x) as.integer(x[2:3])); chr <- p[[1]][1]; if (p[[1]][4] == '-') e <- rev(e)
  g <- function(j) if (j %in% rownames(sjm)) unlist(sjm[j, cells]) else rep(0, length(cells))
  a <- g(paste(chr, e[[1]][2] + 1, e[[2]][1] - 1, sep = ':')); b <- g(paste(chr, e[[2]][2] + 1, e[[3]][1] - 1, sep = ':')); s <- g(paste(chr, e[[1]][2] + 1, e[[3]][1] - 1, sep = ':'))
  res_[[tid]] <- data.frame(isna = is.na(unlist(psi[tid, cells])), a = a, b = b, s = s) }
d <- do.call(rbind, res_)
d$ruleA <- (d$a + d$b) / 2 + d$s >= 10; d$ruleB <- d$a + d$b + d$s >= 10; d$ruleC <- (d$a + d$b) / 2 >= 10 | d$s >= 10; d$ruleD <- pmin((d$a + d$b) / 2, 1e9) + d$s >= 10 & (d$a > 0 | d$b > 0 | d$s > 0)
for (r in c('ruleA', 'ruleB', 'ruleC')) cat(r, ': mismatches vs (PSI not NA) =', sum(d$isna == d[[r]]), 'of', nrow(d), '\n')
cat('PSI NA fraction', round(mean(d$isna), 3), '\n')
