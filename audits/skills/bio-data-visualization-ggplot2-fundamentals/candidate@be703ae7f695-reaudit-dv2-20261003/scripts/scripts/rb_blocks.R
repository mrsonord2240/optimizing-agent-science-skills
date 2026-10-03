# Runs every ```r block of SKILL.md verbatim (cwd = a copy of the Skill dir), then the geoms reference and failure-mode claims.
a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE)
suppressMessages({library(ggplot2); library(ggrepel); library(patchwork); library(grid)})
cat("ggplot2", as.character(packageVersion("ggplot2")), "ggrepel", as.character(packageVersion("ggrepel")), "\n")
chk <- function(l, c) cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l)); flush(stdout())
txt <- readLines(file.path(skill, "SKILL.md"), encoding = "UTF-8")
fence <- grep("^```", txt); blocks <- list(); i <- 1
while (i < length(fence)) { if (grepl("^```r", txt[fence[i]])) blocks[[length(blocks)+1]] <- txt[(fence[i]+1):(fence[i+1]-1)]; i <- i + 2 }
cat("r blocks in SKILL.md:", length(blocks), "\n")
setwd(skill)   # cwd is the Skill copy so source('scripts/publication_figures.R') runs verbatim
set.seed(3)
df <- data.frame(condition = rep(c("ctrl","trt"), each = 30), tissue = rep(c("liver","brain","lung"), 20),
                 expression = exp(rnorm(60, 2)), x = rnorm(60), y = rnorm(60), group = rep(c("a","b"), 30),
                 PC1 = rnorm(60), PC2 = rnorm(60))
p <- ggplot(df, aes(x, y)) + geom_point()
for (k in seq_along(blocks)) {
  W <- character(0); err <- NULL
  ex <- parse(text = blocks[[k]], encoding = "UTF-8")
  r <- tryCatch(withCallingHandlers({
    for (e in ex) { v <- withVisible(eval(e, globalenv()))
      if (v$visible && inherits(v$value, "ggplot")) { png(file.path(out, sprintf("block%d_%s.png", k, "view")), 1000, 700, res = 150); print(v$value); dev.off() } }
    TRUE }, warning = function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") }), error = function(e) { err <<- conditionMessage(e); FALSE })
  chk(sprintf("SKILL.md block %d (%d exprs, first line: %s) runs; warnings: [%s]", k, length(ex), substr(blocks[[k]][1], 1, 40), paste(unique(W), collapse = " | ")), r)
  if (!r) cat("   ERROR:", err, "\n")
}
cat("files written to skill copy:", paste(setdiff(list.files(skill, recursive = TRUE), c("SKILL.md","usage-guide.md","references/failure-modes.md","references/geoms-scales-facets.md","scripts/publication_figures.R")), collapse = ", "), "\n")
# Grammar block rendering: y breaks plain numbers
gd <- df; g <- ggplot(gd, aes(x = condition, y = expression)) + geom_boxplot(outlier.shape = NA) + geom_jitter(aes(color = condition), width = 0.2, alpha = 0.5) +
  scale_y_continuous(transform = 'log10', breaks = scales::breaks_log(), labels = scales::label_number()) + scale_color_manual(values = c('#0072B2', '#D55E00')) +
  labs(x = NULL, y = 'Expression', title = 'Gene X across conditions', caption = 'Source: ...') + facet_wrap(~ tissue, ncol = 3, scales = 'free_y') + theme_classic(base_size = 10) +
  theme(strip.background = element_blank(), strip.text = element_text(face = 'bold'))
bg <- suppressWarnings(ggplot_build(g)); labs_y <- bg$layout$panel_params[[1]]$y$get_labels(); cat("grammar panel1 y labels:", paste(labs_y, collapse = " "), "\n")
chk("grammar y labels plain (no e+)", !any(grepl("e[+-]", labs_y)))
chk("grammar colour legend 'condition' with 2 levels", length(unique(bg$data[[2]]$colour)) == 2)
ggsave(file.path(out, "grammar_183x70.png"), g, width = 183, height = 70, units = "mm", dpi = 170)
# tidy eval claims
pv2 <- function(df, x_var, y_var) ggplot(df, aes(x = {{ x_var }}, y = {{ y_var }})) + geom_point()
chk("plot_var2(df, PC1, PC2) maps data", length(unique(ggplot_build(pv2(df, PC1, PC2))$data[[1]]$x)) > 1)
chk("plot_var2(df, 'PC1','PC2') maps a constant string (as the comment says)", length(unique(ggplot_build(pv2(df, 'PC1', 'PC2'))$data[[1]]$x)) == 1)
# failure-modes claims
b1 <- ggplot_build(ggplot(df, aes(x, y)) + geom_point(aes(color = 'red'))); cat("aes(color='red') colour:", unique(b1$data[[1]]$colour), "\n")
chk("aes(color='red') -> #F8766D salmon", unique(b1$data[[1]]$colour) == "#F8766D")
W <- character(0); withCallingHandlers(ggplot_build(ggplot(df, aes(x, y)) + geom_line(size = 0.5)), warning = function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") })
cat("geom_line(size=) warning:", W, "\n"); chk("size-for-lines deprecation warning fires", length(W) > 0)
W <- character(0); withCallingHandlers(suppressMessages(ggplot_build(ggplot(df, aes_string(x = "x", y = "y")) + geom_point())), warning = function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") })
cat("aes_string warning:", W, "\n"); chk("aes_string deprecation warning fires", length(W) > 0)
chk("aes(x = !!sym(x_var)) works", { xv <- "x"; yv <- "y"; length(unique(ggplot_build(ggplot(df, aes(x = !!sym(xv), y = !!sym(yv))) + geom_point())$data[[1]]$x)) > 1 })
