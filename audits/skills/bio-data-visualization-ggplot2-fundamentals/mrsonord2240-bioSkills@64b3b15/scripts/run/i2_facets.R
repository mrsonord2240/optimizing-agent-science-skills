# Input 2 (Variant A): faceted box+jitter per tissue, free y, log10 axis. SYNTHETIC data (seed 42), labelled as such.
source("F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/run/common.R")
set.seed(42)
tissues <- c(Liver = 2000, Muscle = 200, Brain = 20)          # per-tissue expression scale (differs 100x on purpose)
conds <- c(Control = 1, Treatment = 2.5, Vehicle = 1.1)       # fold effect
df <- do.call(rbind, lapply(names(tissues), function(t) do.call(rbind, lapply(names(conds), function(cn)
  data.frame(tissue = t, condition = cn, expression = tissues[[t]] * conds[[cn]] * rlnorm(12, 0, 0.35))))))
df$tissue <- factor(df$tissue, levels = names(tissues)); df$condition <- factor(df$condition, levels = names(conds))
df$expression[df$tissue == "Liver" & df$condition == "Control"][1] <- 2000 * 8    # one planted high outlier
write.csv(df, file.path(DATA, "synthetic_expression_by_tissue.csv"), row.names = FALSE)
cat("SYNTHETIC data:", nrow(df), "rows;", paste(dim(table(df$tissue, df$condition)), collapse = "x"), "cells, n=12 each\n")

wrn <- character(0)
cap <- function(expr) withCallingHandlers(expr, warning = function(w) { wrn <<- c(wrn, conditionMessage(w)); invokeRestart("muffleWarning") })

# ---- SKILL.md 'Grammar in Layers' block, verbatim (column names adapted only by data) ----
p_asis <- cap(ggplot(df, aes(x = condition, y = expression)) +
    geom_boxplot() +
    geom_jitter(width = 0.2, alpha = 0.5) +
    scale_y_continuous(trans = 'log10', labels = scales::label_log()) +
    scale_color_manual(values = c('#0072B2', '#D55E00')) +
    labs(x = NULL, y = 'Expression (log10)', title = 'Gene X across conditions', caption = 'Source: ...') +
    facet_wrap(~ tissue, ncol = 3, scales = 'free_y') +
    theme_classic(base_size = 10) +
    theme(panel.grid = element_blank(), strip.background = element_blank(), strip.text = element_text(face = 'bold')))
b0 <- cap(ggplot_build(p_asis))
cat("warnings while building the verbatim block:\n"); print(unique(wrn)); wrn <- character(0)
cat("does the verbatim block map colour at all?  aes names in plot+layers:",
    paste(unique(c(names(p_asis$mapping), unlist(lapply(p_asis$layers, function(l) names(l$mapping))))), collapse = ","), "\n")
chk("verbatim block: scale_color_manual is inert (no colour aesthetic mapped)", !"colour" %in% c(names(p_asis$mapping), unlist(lapply(p_asis$layers, function(l) names(l$mapping)))))
bx <- b0$data[[1]]
out_n <- sum(sapply(bx$outliers, length)); cat("verbatim block: boxplot outlier points drawn =", out_n, "(and jitter also draws them: doubled)\n")
chk("verbatim block draws boxplot outliers on top of jitter (Skill's own 'always suppress' rule)", out_n > 0)

# ---- corrected use per the Skill's own rules (outlier.shape = NA, colour mapped, Okabe-Ito, bw='SJ' violin) ----
okabe <- c(Control = '#0072B2', Treatment = '#D55E00', Vehicle = '#009E73')
p <- cap(ggplot(df, aes(x = condition, y = expression, colour = condition)) +
    geom_violin(bw = 'SJ', trim = FALSE, colour = NA, fill = "grey90") +
    geom_boxplot(outlier.shape = NA, width = 0.35, fill = NA) +
    geom_jitter(width = 0.15, alpha = 0.6, size = 1) +
    scale_y_continuous(trans = 'log10', labels = scales::label_log()) +
    scale_color_manual(values = okabe) +
    labs(x = NULL, y = 'Expression (log10)', title = 'Gene X across conditions (synthetic)') +
    facet_wrap(~ tissue, ncol = 3, scales = 'free_y') +
    theme_classic(base_size = 10) +
    theme(panel.grid = element_blank(), strip.background = element_blank(), strip.text = element_text(face = 'bold'), legend.position = "none"))
cat("warnings building the corrected plot:\n"); print(unique(wrn))
b <- ggplot_build(p)
chk("3 facet panels in 1 row x 3 columns", nrow(b$layout$layout) == 3 && all(b$layout$layout$ROW == 1) && setequal(b$layout$layout$COL, 1:3))
yr <- lapply(b$layout$panel_params, function(pp) 10^pp$y.range); print(do.call(rbind, yr))
chk("free_y: panel y-ranges differ by > 10x between Liver and Brain", (yr[[1]][2] / yr[[3]][2]) > 10)
bx <- b$data[[2]]
truth <- do.call(rbind, lapply(split(df, list(df$tissue, df$condition)), function(d) { f <- fivenum(d$expression); data.frame(ymin = f[1], lower = f[2], middle = f[3], upper = f[4], ymax = f[5]) }))
# ggplot boxplot whiskers stop at the last point within 1.5*IQR, not at min/max: recompute
tw <- do.call(rbind, lapply(split(df, list(df$tissue, df$condition)), function(d) { d$expression <- log10(d$expression); f <- unname(quantile(d$expression, c(0, .25, .5, .75, 1))); i <- f[4] - f[2]; data.frame(lower = f[2], middle = f[3], upper = f[4], ymin = min(d$expression[d$expression >= f[2] - 1.5 * i]), ymax = max(d$expression[d$expression <= f[4] + 1.5 * i])) }))
ord <- order(bx$PANEL, bx$x); bxo <- bx[ord, ]
tw <- tw[order(rep(1:3, each = 3), rep(1:3, 3)), ]  # split() orders Liver.Control, Muscle.Control..; reorder tissue-major
tw <- tw[match(paste(rep(names(tissues), each = 3), rep(names(conds), 3), sep = "."), rownames(tw)), ]
chk("boxplot middle/lower/upper on log axis equal quantile(type 7) of log10(raw data): stats are computed on the log scale (9 boxes)",
    all(abs(bxo$middle - tw$middle) < 1e-9) && all(abs(bxo$lower - tw$lower) < 1e-9) && all(abs(bxo$upper - tw$upper) < 1e-9))
chk("whiskers equal the 1.5*IQR rule", all(abs(bxo$ymax - tw$ymax) < 1e-9) && all(abs(bxo$ymin - tw$ymin) < 1e-9))
jit <- b$data[[3]]; chk("jitter layer has 108 points (one per sample)", nrow(jit) == nrow(df))
chk("colours: 36 points per condition in the mapped hexes", all(table(toupper(jit$colour)) == 36) && setequal(toupper(unique(jit$colour)), toupper(okabe)))
# does colour map to the right condition? Treatment has the highest medians -> check the orange points sit in higher position than blue within Liver
liv <- jit[jit$PANEL == 1, ]; chk("Liver: Treatment (orange) points higher on average than Control (blue)", mean(liv$y[toupper(liv$colour) == "#D55E00"]) > mean(liv$y[toupper(liv$colour) == "#0072B2"]))
chk("planted outlier (16000) visible in Liver panel y-range", max(10^b$layout$panel_params[[1]]$y.range) >= 16000)
labs_y <- b$layout$panel_params[[1]]$y$get_labels(); cat("Liver y labels via label_log():", paste(as.character(labs_y), collapse = " | "), "\n")
vl <- b$data[[1]]; cat("violin density max per group finite:", all(is.finite(vl$density)), " ; min y drawn with trim=FALSE per panel:", paste(signif(tapply(10^vl$y, vl$PANEL, min), 3), collapse = ","), " data min:", paste(signif(tapply(df$expression, df$tissue, min), 3), collapse = ","), "\n")

# 'trans' vs 'transform' argument (deprecated in 3.5.0)
w2 <- character(0)
invisible(withCallingHandlers(ggplot_build(ggplot(df, aes(condition, expression)) + geom_point() + scale_y_continuous(trans = "log10")), warning = function(w) { w2 <<- c(w2, conditionMessage(w)); invokeRestart("muffleWarning") }))
cat("scale_y_continuous(trans='log10') warnings:", if (length(w2)) paste(unique(w2), collapse = " || ") else "none", "\n")
chk("Skill-block 'trans=' emits no deprecation warning on this ggplot2", length(w2) == 0)

ggsave(file.path(OUT, "i2_verbatim.png"), p_asis, width = 183, height = 70, units = "mm", dpi = 200)
ggsave(file.path(OUT, "i2_corrected.png"), p, width = 183, height = 70, units = "mm", dpi = 200)
ggsave(file.path(OUT, "i2_corrected.pdf"), p, width = 183, height = 70, units = "mm", device = cairo_pdf)
png_info(file.path(OUT, "i2_corrected.png")); pdf_info(file.path(OUT, "i2_corrected.pdf"))
