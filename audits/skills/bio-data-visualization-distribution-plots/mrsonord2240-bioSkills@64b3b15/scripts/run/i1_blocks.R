# Input 1: every plain R block of SKILL.md, run verbatim (df from data/i1_synthetic_2group.csv), then assertions on the built plot data.
suppressMessages({library(ggplot2)})
tag <- Sys.getenv("TAG", "gg4")
df <- read.csv("data/i1_synthetic_2group.csv"); df$group <- factor(df$group, levels=c("Control","Treated"))
cat("ggplot2", as.character(packageVersion("ggplot2")), "\n")
modes <- function(y, d, prom = 0.15) {  # prominent modes: peak must rise >= prom*max above the valley separating it from a higher peak
  idx <- which(diff(sign(diff(d))) == -2) + 1; if (length(idx) <= 1) return(length(idx))
  keep <- sapply(seq_along(idx), function(k) { i <- idx[k]; higher <- idx[d[idx] > d[i]]
    if (!length(higher)) return(TRUE); j <- higher[which.min(abs(higher - i))]; (d[i] - min(d[min(i,j):max(i,j)])) >= prom * max(d) })
  sum(keep) }
rawmodes <- function(d) length(which(diff(sign(diff(d))) == -2) + 1)
chk <- function(label, ok, note="") cat(sprintf("[%s] %s %s\n", if (isTRUE(ok)) "PASS" else "FAIL", label, note))
blk <- function(name, expr) {
  res <- try(expr, silent=TRUE)
  if (inherits(res, "try-error")) { cat("BLOCK ERROR", name, ":", conditionMessage(attr(res,"condition")), "\n"); return(invisible(NULL)) }
  invisible(res)
}
qs <- tapply(df$value, df$group, function(x) quantile(x, c(0,.25,.5,.75,1)))

## ---- Block 1: boxplot + jitter (verbatim)
p1 <- blk("boxplot", {
p <- ggplot(df, aes(group, value, fill = group)) +
    geom_boxplot(outlier.shape = NA, alpha = 0.7, width = 0.5) +
    geom_jitter(width = 0.2, alpha = 0.5, size = 1) +
    scale_fill_manual(values = c('#0072B2', '#D55E00')) +
    labs(x = NULL, y = 'Expression') +
    theme_classic()
ggsave(sprintf("out/i1_box_%s.png", tag), p, width=4, height=3.5, dpi=110); p })
if (!is.null(p1)) {
  ld <- layer_data(p1, 1); jd <- layer_data(p1, 2)
  chk("box medians equal data medians", all.equal(ld$middle, as.numeric(sapply(qs, `[`, 3))), paste(round(ld$middle,3), collapse="/"))
  chk("box fill order Control=#0072B2 Treated=#D55E00", identical(toupper(ld$fill), c("#0072B2","#D55E00")), paste(ld$fill, collapse="/"))
  chk("jitter shows every point (25 + 80)", nrow(jd) == 105 && all(table(round(jd$x)) == c(25, 80)))
  chk("boxplot Q1/Q3 equal data quartiles", all.equal(c(ld$lower, ld$upper), as.numeric(c(sapply(qs, `[`, 2), sapply(qs, `[`, 4)))))
  cat("Treated box median", round(ld$middle[2],3), "lies in the empty gap between the two modes (3 and 7): the box hides bimodality (as the SKILL says).\n")
}

## ---- Block 2: violin, bw = 'SJ', trim = FALSE (verbatim)
p2 <- blk("violin", {
p <- ggplot(df, aes(group, value, fill = group)) +
    geom_violin(alpha = 0.7, trim = FALSE,
                bw = 'SJ') +                            # Sheather-Jones bandwidth
    geom_boxplot(width = 0.1, fill = 'white', outlier.shape = NA) +
    scale_fill_manual(values = c('#0072B2', '#D55E00'))
ggsave(sprintf("out/i1_violin_%s.png", tag), p, width=4, height=3.5, dpi=110); p })
if (!is.null(p2)) {
  vd <- layer_data(p2, 1)
  if ("quantile" %in% names(vd)) vd <- vd[is.na(vd$quantile), ]   # ggplot2 4.x appends 3 quantile rows per violin to layer_data; drop before counting modes
  m <- sapply(split(vd, vd$group), function(d) modes(d$y, d$density))
  chk("SJ violin: Control unimodal, Treated bimodal (prominent modes)", identical(unname(m), c(1L, 2L)), paste("prominent modes", paste(m, collapse="/"), "| raw local maxima", paste(sapply(split(vd, vd$group), function(d) rawmodes(d$density)), collapse="/")))
  bws <- c(Control=bw.SJ(df$value[df$group=="Control"]), Treated=bw.SJ(df$value[df$group=="Treated"]))
  cat("SJ bw:", round(bws,3), " nrd0 bw:", round(c(bw.nrd0(df$value[df$group=="Control"]), bw.nrd0(df$value[df$group=="Treated"])),3), "\n")
  chk("trim=FALSE: violin extends past data range", min(vd$y[vd$group==2]) < min(df$value[df$group=="Treated"]) - 0.1,
      sprintf("violin y [%.2f, %.2f] vs data [%.2f, %.2f]", min(vd$y[vd$group==2]), max(vd$y[vd$group==2]), min(df$value[df$group=="Treated"]), max(df$value[df$group=="Treated"])))
}
## default (Silverman/nrd0) violin for the same data: SKILL claims it oversmooths bimodality
pd <- ggplot(df, aes(group, value)) + geom_violin(); vd0 <- layer_data(pd, 1); if ("quantile" %in% names(vd0)) vd0 <- vd0[is.na(vd0$quantile), ]
m0 <- sapply(split(vd0, vd0$group), function(d) modes(d$y, d$density))
cat("default nrd0 violin prominent modes (Control/Treated):", paste(m0, collapse="/"), "raw maxima", paste(sapply(split(vd0, vd0$group), function(d) rawmodes(d$density)), collapse="/"), "-> claim 'oversmooths bimodal to a single peak' is", if (m0[2]==1) "TRUE here" else "FALSE here (well-separated modes survive)", "\n")

## ---- Block 3: quasirandom + crossbar (verbatim)
p3 <- blk("quasirandom", {
library(ggbeeswarm)
p <- ggplot(df, aes(group, value, color = group)) +
    geom_quasirandom(method = 'quasirandom', width = 0.3, alpha = 0.7) +
    scale_color_manual(values = c('#0072B2', '#D55E00')) +
    stat_summary(fun = median, geom = 'crossbar', width = 0.5, color = 'black')
ggsave(sprintf("out/i1_quasi_%s.png", tag), p, width=4, height=3.5, dpi=110); p })
if (!is.null(p3)) {
  qd <- layer_data(p3, 1); cd <- layer_data(p3, 2)
  chk("quasirandom draws all 105 points, n per group 25/80", nrow(qd)==105 && all(table(round(qd$x)) == c(25,80)))
  chk("crossbar y equals group median", all.equal(cd$y, as.numeric(tapply(df$value, df$group, median))), paste(round(cd$y,3), collapse="/"))
  # the y of every point must equal a data value (no vertical distortion)
  chk("quasirandom y values are the data values", all.equal(sort(qd$y), sort(df$value)))
  qd2 <- layer_data(ggplot(df, aes(group, value)) + geom_quasirandom(method='quasirandom', width=0.3), 1)
  chk("quasirandom deterministic across two builds", isTRUE(all.equal(qd$x, layer_data(p3,1)$x)) && isTRUE(all.equal(qd2$x, layer_data(ggplot(df, aes(group, value)) + geom_quasirandom(method='quasirandom', width=0.3),1)$x)))
  qs2 <- sapply(1:2, function(i) layer_data(ggplot(df, aes(group, value)) + geom_quasirandom(width=0.3), 1)$x); chk("quasirandom x identical on re-run", identical(qs2[,1], qs2[,2]) )
}
## ---- Block 4: raincloud gghalves (verbatim)
p4 <- blk("raincloud", {
library(gghalves)
p <- ggplot(df, aes(group, value, fill = group, color = group)) +
    geom_half_violin(side = 'r', alpha = 0.7, position = position_nudge(x = 0.15)) +
    geom_boxplot(width = 0.15, outlier.shape = NA, alpha = 0.7,
                 position = position_nudge(x = -0.05)) +
    geom_half_point(side = 'l', alpha = 0.5, size = 1.5, range_scale = 0.4,
                    position = position_nudge(x = -0.2)) +
    scale_fill_manual(values = c('#0072B2', '#D55E00')) +
    scale_color_manual(values = c('#0072B2', '#D55E00')) +
    coord_flip()                                          # horizontal "raincloud"
ggsave(sprintf("out/i1_raincloud_%s.png", tag), p, width=5, height=3.5, dpi=110); p })
if (!is.null(p4)) {
  ly <- lapply(1:3, function(i) layer_data(p4, i))
  py <- unlist(ly[[3]]$point_y)   # gghalves stores the raw points in a list column, one row per group
  chk("raincloud half-points: 105 raw points, y equals data", length(py)==105 && isTRUE(all.equal(sort(py), sort(df$value))), paste("n per group", paste(sapply(ly[[3]]$point_y, length), collapse="/")))
  chk("raincloud box medians equal data medians", isTRUE(all.equal(ly[[2]]$middle, as.numeric(tapply(df$value, df$group, median)))))
  # geometry: after nudges, violin x-range vs box vs points must not overlap
  cat("group1 (Control) x extents: violin", paste(round(range(ly[[1]]$x[ly[[1]]$group==1]),2), collapse=".."), " box", paste(round(c(ly[[2]]$xmin[1], ly[[2]]$xmax[1]),2), collapse=".."), " points", paste(round(range(ly[[3]]$x[ly[[3]]$group==1]),2), collapse=".."), "\n")
}
## ---- Block 5: letter-value (verbatim)
p5 <- blk("lv", {
library(lvplot)
p <- ggplot(df, aes(group, value, fill = group)) +
    geom_lv(k = 5, alpha = 0.7) +
    scale_fill_manual(values = c('#0072B2', '#D55E00'))
ggsave(sprintf("out/i1_lv_%s.png", tag), p, width=4, height=3.5, dpi=110); p })
if (!is.null(p5)) { ld5 <- layer_data(p5, 1); cat("lv layer rows", nrow(ld5), "cols", paste(names(ld5), collapse=","), "\n")
  print(ld5[, c("x","LV","lower","upper","depth")])
  med <- ld5[ld5$LV == "M", ]  # letter M = median
  chk("lv LV=1 (median) equals data medians", isTRUE(all.equal(as.numeric(med$lower), as.numeric(tapply(df$value, df$group, median)))), paste(round(med$lower,3), collapse="/")) }
