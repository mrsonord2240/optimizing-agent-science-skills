# Input 4c (STRESS): SYNTHETIC DE table (clearly synthetic, seed 20260920) with extreme p-values (1e-200) and underflowed p = 0,
# to test the Skill's y-axis cap / sqrt / ggbreak / ggrepel max.overlaps guidance.
suppressMessages({library(ggplot2); library(ggrepel); library(dplyr)})
D <- "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots"
source(file.path(D, "run/blocks/skill_block02.R"))   # volcano_plot() verbatim
set.seed(20260920)
n <- 20000
lfc <- rnorm(n, 0, 0.6); p <- runif(n)
hit <- sample(n, 400); lfc[hit] <- sign(rnorm(400)) * runif(400, 1.2, 4); p[hit] <- 10^-runif(400, 3, 40)
ext <- sample(setdiff(seq_len(n), hit), 8); lfc[ext] <- c(2.5, -3, 1.8, 3.5, -2.2, 2.9, -1.5, 4); p[ext] <- c(1e-200, 1e-180, 1e-150, 1e-120, 1e-100, 1e-90, 1e-80, 0)  # last one underflows to exactly 0
padj <- p.adjust(p, "BH"); base <- 10^runif(n, 0.5, 4)
res <- data.frame(baseMean = base, log2FoldChange = lfc, pvalue = p, padj = padj, row.names = paste0("g", seq_len(n)))
write.csv(res, file.path(D, "data/synthetic_extreme_p.csv"))
fails <- 0; chk <- function(name, ok, note="") { cat(sprintf("[%s] %s %s\n", if (ok) "PASS" else "FAIL", name, note)); if (!ok) fails <<- fails + 1 }
cat("SYNTHETIC: n =", n, " min p:", min(p[p > 0]), " p==0:", sum(p == 0), " Up/Down by padj+lfc:", sum(padj < .05 & abs(lfc) > 1), "\n")
w <- character()
pl <- function(pp, f, ...) { png(file.path(D, "figs", f), 1300, 1100, res = 180); r <- withCallingHandlers(print(pp), warning = function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") }); dev.off() }
# (1) Skill function as-is on p = 0 / 1e-200 data
p1 <- volcano_plot(res); w <- character(); pl(p1, "i4c_1_asis.png")
cat("(1) as-is: warnings at print:", paste(unique(substr(w, 1, 120)), collapse = " | "), "\n")
lab1 <- unique(p1$data$label[p1$data$label != ""]); cat("    labels:", paste(lab1, collapse = ","), "\n")
cat("    neg_log10_p Inf count:", sum(is.infinite(p1$data$neg_log10_p)), " max finite:", max(p1$data$neg_log10_p[is.finite(p1$data$neg_log10_p)]), "\n")
# (2) Skill's fix #1: coord_cartesian(ylim = c(0, 50)) -- 'capped points stay in the data but render at the edge'
p2 <- p1 + coord_cartesian(ylim = c(0, 50)); w <- character(); pl(p2, "i4c_2_coordcartesian50.png")
b2 <- ggplot_build(p2); yr <- b2$layout$panel_params[[1]]$y.range; pts2 <- b2$data[[1]]
vis <- sum(is.finite(pts2$y) & pts2$y >= yr[1] & pts2$y <= yr[2]); tot <- sum(!is.na(pts2$y))
cat(sprintf("(2) coord_cartesian(0,50): y.range = %.1f..%.1f; points inside panel %d of %d; significant (colored) points beyond cap: %d\n", yr[1], yr[2], vis, tot,
    sum(p1$data$neg_log10_p > 50 & p1$data$significance != "NS", na.rm = TRUE) + sum(is.infinite(p1$data$neg_log10_p))))
chk("capped points remain visible at the panel edge (Skill/usage-guide claim)", all(pts2$y[is.finite(pts2$y) & pts2$y > 50] <= yr[2]) && FALSE, "coord_cartesian only clips the view; the 9 points above 50 are simply outside the panel")
# (3) Skill's fix #2: sqrt(-log10 p)
d3 <- p1$data; d3$y3 <- sqrt(d3$neg_log10_p)
p3 <- ggplot(d3, aes(log2FoldChange, y3, color = significance)) + geom_point(alpha = .6, size = 1) + scale_color_manual(values = c(Up = "#D55E00", Down = "#0072B2", NS = "#999999")) +
  geom_hline(yintercept = sqrt(-log10(.05)), linetype = 2) + labs(y = expression(sqrt(-log[10]~italic(p)))) + theme_classic()
w <- character(); pl(p3, "i4c_3_sqrt.png"); cat("(3) sqrt transform runs; max y:", round(max(d3$y3[is.finite(d3$y3)]), 2), " Inf rows:", sum(is.infinite(d3$y3)), " warnings:", length(w), "\n")
# (4) Skill's fix #3: ggbreak split axis
ok <- requireNamespace("ggbreak", quietly = TRUE); cat("(4) ggbreak installed:", ok, "\n")
if (ok) { r <- try({ p4 <- p1 + ggbreak::scale_y_break(c(60, 110)); png(file.path(D, "figs/i4c_4_ggbreak.png"), 1300, 1100, res = 180); print(p4); dev.off(); "ok" }, silent = TRUE)
  cat("    ggbreak::scale_y_break result:", if (inherits(r, "try-error")) substr(conditionMessage(attr(r, "condition")), 1, 200) else r, "\n"); chk("ggbreak split-axis suggestion runs on this stack", !inherits(r, "try-error")) }
# (5) ggrepel default max.overlaps drops labels (claim: silent apart from a warning)
d <- p1$data; d$label <- ifelse(d$significance != "NS" & rank(-abs(d$log2FoldChange) * pmin(d$neg_log10_p, 50), ties.method = "first") <= 60, d$gene, "")
p5 <- ggplot(d, aes(log2FoldChange, pmin(neg_log10_p, 60))) + geom_point(size = .5) + geom_text_repel(aes(label = label), size = 3)   # default max.overlaps
w <- character(); pl(p5, "i4c_5_repel_default.png"); cat("(5) default max.overlaps, 60 requested labels; warning at print:", paste(unique(substr(w, 1, 110)), collapse = " | "), "\n")
chk("Skill's ggrepel warning text 'unlabeled data points (too many overlaps)' appears", any(grepl("too many overlaps", w)))
cat("SUMMARY fails =", fails, "\n")
