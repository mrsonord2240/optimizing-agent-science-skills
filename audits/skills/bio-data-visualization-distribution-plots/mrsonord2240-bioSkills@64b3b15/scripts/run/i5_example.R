# Input 5 (Stress): the shipped example examples/raincloud_phd.R.
#  (1) as shipped, no data prelude  (2) with a prelude that defines the data frames the example uses but never creates
#  (3) render every plot the example builds, assert on drawn content.  SYNTHETIC data, planted structure.
suppressMessages({library(ggplot2); library(dplyr)})
gv <- as.character(packageVersion("ggplot2")); cat("ggplot2", gv, "\n")
ex <- "F:/OpenScience/audits/bio-data-visualization-distribution-plots/run/skill/data-visualization/distribution-plots/examples/raincloud_phd.R"
chk <- function(label, ok, note="") cat(sprintf("[%s] %s %s\n", if (isTRUE(ok)) "PASS" else "FAIL", label, note))
tryp <- function(expr) tryCatch(expr, error=function(e) structure(conditionMessage(e), class="err"))
dir.create("out/i5", showWarnings=FALSE, recursive=TRUE); setwd("out/i5")

## (1) as shipped
env0 <- new.env()
r <- tryp({ sys.source(ex, envir=env0); "ran" })
cat("(1) example as shipped ->", gsub("\n", " ", r), "\n"); chk("shipped example runs standalone (no data prelude)", identical(r, "ran"))

## (2) prelude: df = full data (3 groups, n=80 each); df_small = 15-per-group subset of df; df_med = df; df_large = 2000/group; df_paired
set.seed(11)
grp <- c("Ctrl","Low","High")
df <- data.frame(group = factor(rep(grp, each=80), levels=grp), value = c(rnorm(80, 10, 2), c(rnorm(40, 8, .7), rnorm(40, 14, .7)), rlnorm(80, 2.4, .45)))
df_small <- df %>% group_by(group) %>% slice_head(n=15) %>% ungroup()
df_med <- df
df_large <- data.frame(group = factor(rep(grp, each=2000), levels=grp), value = c(rlnorm(2000, 1, 0.9), rnorm(2000, 5, 2), c(rnorm(1000, 2, .5), rnorm(1000, 9, 1.2))))
df_paired <- data.frame(cluster = factor(rep(c("c1","c2","c3"), each=120)), condition = factor(rep(rep(c("Control","Treatment"), each=60), 3), levels=c("Control","Treatment")),
                        expression = c(rnorm(60, 1, .5), rnorm(60, 2, .5), rnorm(60, 3, 1), c(rnorm(30, 1, .4), rnorm(30, 5, .4)), rnorm(60, 2, .6), rnorm(60, 2.2, .6)))
write.csv(df, "df.csv", row.names=FALSE); write.csv(df_large, "df_large.csv", row.names=FALSE); write.csv(df_paired, "df_paired.csv", row.names=FALSE)
env <- new.env(); for (nm in c("df","df_small","df_med","df_large","df_paired")) assign(nm, get(nm), env)
r <- tryp({ sys.source(ex, envir=env); "ran" })
cat("(2) example with data prelude ->", gsub("\n", " ", r), "\n"); chk(paste0("example (source + its own ggsave to raincloud.pdf) runs with a prelude, ggplot2 ", gv), identical(r, "ran"))
cat("raincloud.pdf exists:", file.exists("raincloud.pdf"), " size:", if (file.exists("raincloud.pdf")) file.size("raincloud.pdf") else NA, "\n")

## (3) plots the example builds
E <- function(n) get(n, envir=env)
# 3a small-N beeswarm
pS <- E("p_small"); rS <- tryp({ ggsave("p_small.png", pS, width=4, height=3, dpi=100); layer_data(pS, 1) })
if (inherits(rS, "err")) cat("p_small render error:", rS, "\n") else {
  cm <- layer_data(pS, 2)$y; chk("p_small crossbar = per-group medians of df_small", isTRUE(all.equal(cm, as.numeric(tapply(df_small$value, df_small$group, median)))), paste(round(cm,2), collapse="/"))
  chk("p_small draws 15 points per group", all(table(round(rS$x)) == 15), paste(as.integer(table(round(rS$x))), collapse="/"))
  labs <- ggplot_build(pS)$layout$panel_params[[1]]$x$get_labels(); cat("p_small x tick labels:", paste(gsub("\n", " ", labs), collapse=" | "), "\n")
  chk("p_small x labels state the n actually plotted (15)", all(grepl("n=15", labs)), "labels come from n_per_group computed on df (n=80), not df_small")
}
# 3b raincloud
pR <- E("p_raincloud"); rR <- tryp({ ggsave("p_raincloud.png", pR, width=5, height=3.5, dpi=100); "ok" })
cat("p_raincloud render:", gsub("\n", " ", rR), "\n"); chk("raincloud in shipped example renders", identical(rR, "ok"))
if (identical(rR, "ok")) { ly <- lapply(1:3, function(i) layer_data(pR, i)); chk("raincloud boxes = data medians of df_med", isTRUE(all.equal(as.numeric(ly[[2]]$middle), as.numeric(tapply(df_med$value, df_med$group, median)))))
  vd <- ly[[1]]; chk("half-violin trim=FALSE extends beyond data range (Ctrl min)", min(vd$y[vd$group==1]) < min(df_med$value[df_med$group=="Ctrl"])) }
# 3c letter-value (N=2000)
pL <- E("p_lv"); rL <- tryp({ ggsave("p_lv.png", pL, width=4.5, height=3.2, dpi=100); layer_data(pL, 1) })
if (inherits(rL, "err")) cat("p_lv render error:", rL, "\n") else {
  print(rL[rL$LV %in% c("M","F"), c("x","LV","lower","upper")])
  q <- df_large %>% group_by(group) %>% summarise(med=median(value), q1=quantile(value,.25), q3=quantile(value,.75), .groups="drop")
  M <- rL[rL$LV=="M",]; Fr <- rL[rL$LV=="F",]
  chk("LV median equals group medians (N=2000)", isTRUE(all.equal(as.numeric(M$lower), q$med, tolerance=1e-8)))
  cat("LV F lower/upper:", paste(round(Fr$lower,3), round(Fr$upper,3), sep="..", collapse=" | "), " data q1..q3:", paste(round(q$q1,3), round(q$q3,3), sep="..", collapse=" | "), "
")
  chk("LV fourths (F) equal group quartiles (rel. tol 2%)", isTRUE(all.equal(unname(c(Fr$lower, Fr$upper)), unname(c(q$q1, q$q3)), tolerance=0.02)))
  chk("k=5 gives 5 letter-value levels per group", all(table(rL$x) == 5), paste(as.integer(table(rL$x)), collapse="/")) }
# 3d split violin
pP <- E("p_split"); rP <- tryp({ ggsave("p_split.png", pP, width=5, height=3.5, dpi=100); layer_data(pP, 2) })
if (inherits(rP, "err")) cat("p_split render error:", rP, "\n") else {
  tm <- df_paired %>% group_by(cluster, condition) %>% summarise(med=median(expression), .groups="drop")
  chk("split-violin box medians equal (cluster,condition) medians", isTRUE(all.equal(sort(as.numeric(rP$middle)), sort(tm$med), tolerance=1e-8)), paste(round(sort(as.numeric(rP$middle)),2), collapse=",")) }
# 3e PDF export: inspected by i5_pdf.py
cat("raincloud.pdf bytes:", if (file.exists("raincloud.pdf")) file.size("raincloud.pdf") else NA, "
")
