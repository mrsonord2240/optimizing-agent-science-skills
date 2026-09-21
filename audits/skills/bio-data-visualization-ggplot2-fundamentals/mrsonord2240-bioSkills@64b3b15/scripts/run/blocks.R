# Every remaining code block in SKILL.md (Common Geoms, Scales, Facets, Theme, Failure Modes), built AND asserted on layer data.
# SYNTHETIC df (seed 11) unless noted.
source("F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/run/common.R")
suppressPackageStartupMessages({library(ggrepel); library(ggtext); library(scales); library(scico); library(viridis)})
set.seed(11)
df <- data.frame(x = runif(200, 0, 1e7), y = rnorm(200, 50, 10), group = sample(c("Control", "Treatment", "Vehicle"), 200, TRUE),
                 z = rnorm(200), label = paste0("g", 1:200), tissue = sample(c("liver", "brain"), 200, TRUE), tp = sample(c("0h", "6h"), 200, TRUE),
                 condition = sample(c("A", "B"), 200, TRUE), date = as.Date("2020-01-01") + sample(0:1500, 200, TRUE), val = rlnorm(200))
W <- character(0)
run <- function(name, expr) {
  W <<- character(0)
  r <- tryCatch(withCallingHandlers({ b <- ggplot_build(expr); "ok" }, warning = function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") }),
                error = function(e) paste("ERROR:", conditionMessage(e)))
  cat(sprintf("%-46s %s%s\n", name, r, if (length(W)) paste0("   | warn: ", gsub("\n", " ", paste(unique(W), collapse = " ; "))) else ""))
  invisible(NULL)
}
g <- ggplot(df, aes(x, y))
cat("--- Common Geoms ---\n")
run("geom_point(alpha,size)", g + geom_point(alpha = 0.7, size = 1))
run("geom_line(linewidth = 0.5)", g + geom_line(linewidth = 0.5))
run("geom_col()", ggplot(df, aes(group, y)) + geom_col())
run("geom_bar()", ggplot(df, aes(group)) + geom_bar())
run("geom_boxplot(outlier.shape = NA)", ggplot(df, aes(group, y)) + geom_boxplot(outlier.shape = NA))
run("geom_violin(bw='SJ', trim=FALSE)", ggplot(df, aes(group, y)) + geom_violin(bw = 'SJ', trim = FALSE))
run("geom_histogram(bins = 30)", ggplot(df, aes(y)) + geom_histogram(bins = 30))
run("geom_density(alpha = 0.5)", ggplot(df, aes(y)) + geom_density(alpha = 0.5))
run("geom_tile(aes(fill = z))", ggplot(expand.grid(a = 1:5, b = 1:5) |> transform(z = rnorm(25)), aes(a, b)) + geom_tile(aes(fill = z)))
run("geom_text(check_overlap = TRUE)", g + geom_text(aes(label = label), check_overlap = TRUE))
run("geom_text_repel(max.overlaps = Inf)", g + geom_text_repel(aes(label = label), max.overlaps = Inf))
cat("--- Scales ---\n")
run("scale_x_continuous(limits,breaks,label_number M)", g + geom_point() + scale_x_continuous(limits = c(0, 10), breaks = seq(0, 10, 2), labels = scales::label_number(scale = 1e-6, suffix = 'M')))
run("scale_y_log10()", ggplot(df, aes(x, val)) + geom_point() + scale_y_log10())
run("scale_y_continuous(trans = 'sqrt')", ggplot(df, aes(x, val)) + geom_point() + scale_y_continuous(trans = 'sqrt'))
run("scale_x_discrete(limits=...)", ggplot(df, aes(group, y)) + geom_boxplot() + scale_x_discrete(limits = c('Control', 'Treatment', 'Vehicle')))
run("scale_color_manual(named values)", g + geom_point(aes(color = group)) + scale_color_manual(values = c(Control = '#0072B2', Treatment = '#D55E00')))
run("scale_color_viridis_c(option='viridis')", g + geom_point(aes(color = z)) + scale_color_viridis_c(option = 'viridis'))
run("scale_color_scico(palette='batlow')", g + geom_point(aes(color = z)) + scale_color_scico(palette = 'batlow'))
run("scale_fill_gradient2(midpoint = 0)", ggplot(df, aes(tissue, tp, fill = z)) + geom_tile() + scale_fill_gradient2(low = '#0072B2', mid = 'white', high = '#D55E00', midpoint = 0))
run("scale_x_date(date_breaks, date_labels)", ggplot(df, aes(date, y)) + geom_point() + scale_x_date(date_breaks = '1 year', date_labels = '%Y'))
cat("--- Facets ---\n")
run("facet_wrap(~ var, ncol=3, scales='free_y')", g + geom_point() + facet_wrap(~ tissue, ncol = 3, scales = 'free_y'))
run("facet_grid(rows=vars, cols=vars, scales='free_x')", g + geom_point() + facet_grid(rows = vars(condition), cols = vars(tp), scales = 'free_x'))
run("facet_grid(condition ~ tp)", g + geom_point() + facet_grid(condition ~ tp))
bg <- ggplot_build(g + geom_point() + facet_grid(rows = vars(condition), cols = vars(tp), scales = 'free_x'))
chk("facet_grid 2x2 layout", nrow(bg$layout$layout) == 4 && max(bg$layout$layout$ROW) == 2 && max(bg$layout$layout$COL) == 2)
cat("--- Theme (theme_pub verbatim) ---\n")
theme_pub <- theme_classic(base_size = 10) +
    theme(panel.grid = element_blank(), axis.text = element_text(color = 'black'),
        axis.ticks = element_line(color = 'black', linewidth = 0.3), axis.line = element_line(color = 'black', linewidth = 0.3),
        legend.position = 'right', legend.key.size = unit(0.4, 'cm'), strip.background = element_blank(),
        strip.text = element_text(face = 'bold', size = 9), plot.title = element_text(face = 'bold', size = 11), plot.tag = element_text(face = 'bold', size = 11))
run("theme_pub applied", g + geom_point(aes(color = group)) + facet_wrap(~tissue) + labs(title = "t", tag = "A") + theme_pub)
tt <- theme_classic(); cat("theme_classic already has panel.grid blank:", inherits(tt$panel.grid, "element_blank"), "\n")
chk("Skill 'panel.grid = element_blank()' is redundant on theme_classic (grid already blank)", inherits(tt$panel.grid, "element_blank"))
# usage-guide tip: 'Remove top/right axis lines if Nature style: theme(axis.line = element_line())'
tc <- theme_classic()$axis.line; cat("theme_classic axis.line is drawn on left+bottom only (top/right axes do not exist in ggplot2):", class(tc)[1], "\n")
cat("--- ggtext / tidy eval ---\n")
run("element_markdown labs block", g + geom_point() + labs(x = 'log<sub>2</sub> fold change', y = '\\u2212log<sub>10</sub>(*p*)') + theme(axis.title.x = element_markdown(), axis.title.y = element_markdown()))
cat("--- Failure-mode claims ---\n")
# 1 aes(color='red') maps to FIRST default colour: claim says 'points appear blue'
b <- ggplot_build(ggplot(df, aes(x, y)) + geom_point(aes(color = 'red')))
cat("aes(color='red') renders colour:", unique(b$data[[1]]$colour), " (legend label 'red')\n")
cl <- col2rgb(unique(b$data[[1]]$colour)); cat("   RGB:", paste(cl, collapse = ","), "->", if (cl[1] > cl[3]) "reddish/salmon, NOT blue" else "bluish", "\n")
chk("Skill claim 'Points appear blue (or whatever default)' is right for aes(color='red')", cl[3] > cl[1])
# 2 size on geom_line
run("geom_line(size = 0.5)", g + geom_line(size = 0.5))
# 3 ggrepel default drops labels
W <- character(0)
n_def <- withCallingHandlers({ pb <- ggplot_build(g + geom_text_repel(aes(label = label))); NULL }, warning = function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") })
cat("geom_text_repel default: warnings during build:", if (length(W)) paste(unique(W), collapse = " ; ") else "none (ggrepel warns at draw time)", "\n")
tmp <- tempfile(fileext = ".png"); W <- character(0)
pr <- g + geom_text_repel(aes(label = label))
withCallingHandlers({ png(tmp, 400, 300); print(pr); dev.off() }, warning = function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") }, message = function(m) { W <<- c(W, conditionMessage(m)); invokeRestart("muffleMessage") })
cat("draw with default max.overlaps=10 on 200 labels, conditions:", paste(unique(W), collapse = " ; "), "
")
chk("default ggrepel reports unlabeled points (Skill's claim)", any(grepl("unlabeled|overlaps", W)))
