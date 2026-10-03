a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE); setwd(out)
suppressMessages({library(ggplot2); library(ggrepel); library(grid)})
cat("ggplot2", as.character(packageVersion("ggplot2")), " ggrepel", as.character(packageVersion("ggrepel")), "\n")
chk <- function(l, c) cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l)); flush(stdout())
# --- GG-009: silent drop, verbose = TRUE only
set.seed(1); dd <- data.frame(x = rnorm(300, sd = .02), y = rnorm(300, sd = .02), l = paste0("GENE", 1:300))
drawn <- function(p) { W <- character(0); png("t.png", 900, 700, res = 100)
  withCallingHandlers({ print(p); grid.force() }, warning = function(w) { W <<- c(W, paste('warning:', conditionMessage(w))); invokeRestart("muffleWarning") },
    message = function(m) { W <<- c(W, paste('message:', conditionMessage(m))); invokeRestart("muffleMessage") })
  g <- grid.ls(grobs = TRUE, viewports = FALSE, print = FALSE); dev.off()
  list(n = sum(grepl("^textrepelgrob", g$name)), cond = unique(W)) }
bp <- function(...) ggplot(dd, aes(x, y, label = l)) + geom_point() + geom_text_repel(size = 3, ...)
a1 <- drawn(bp()); a2 <- drawn(bp(max.overlaps = Inf, seed = 1)); a3 <- drawn(bp(verbose = TRUE))
cat("default: drawn", a1$n, "of 300; conditions:", if (length(a1$cond)) a1$cond else "none", "\n")
cat("Inf: drawn", a2$n, "of 300; conditions:", if (length(a2$cond)) a2$cond else "none", "\n")
cat("verbose=TRUE: drawn", a3$n, "; conditions:", if (length(a3$cond)) a3$cond else "none", "\n")
chk("default drops labels silently (no warning/message)", a1$n < 300 && length(a1$cond) == 0)
chk("Inf draws all 300", a2$n == 300)
chk("verbose=TRUE emits a message", length(a3$cond) > 0)
# stdout/stderr leakage check (not only conditions): run draw to a file device and capture output
op <- capture.output(print(bp()), type = "output"); chk("default: nothing printed to stdout", length(op) == 0)
# 'a label overlapping more than 10 others': sparse plot unaffected
ds <- data.frame(x = 1:30, y = rep(1:3, 10), l = paste0("G", 1:30)); n_s <- drawn(ggplot(ds, aes(x, y, label = l)) + geom_point() + geom_text_repel())$n
chk(sprintf("sparse plot: all 30 drawn at default (%d)", n_s), n_s == 30)
# options(ggrepel.max.overlaps = Inf) alternative
options(ggrepel.max.overlaps = Inf); n_o <- drawn(ggplot(dd, aes(x, y, label = l)) + geom_point() + geom_text_repel(size = 3))$n; options(ggrepel.max.overlaps = NULL)
chk(sprintf("options(ggrepel.max.overlaps=Inf) draws all (%d)", n_o), n_o == 300)
# --- geoms reference snippets (illustrative lines run on mtcars-like data)
set.seed(2); d <- data.frame(g = rep(c("ctrl","trt","veh"), each = 20), z = rnorm(60), x = runif(60, 0, 10), group = rep(c("a","b"), 30), label = paste0("L", 1:60), y = rnorm(60), condition = rep(c("c1","c2"), 30), timepoint = rep(c("t1","t2","t3"), 20), dt = as.Date("2020-01-01") + 365 * (1:60 %% 7), stringsAsFactors = FALSE)
library(scales); has <- function(p) { r <- tryCatch({ suppressWarnings(ggplot_build(p)); NULL }, error = function(e) conditionMessage(e)); is.null(r) || (cat("   ERR:", r, "\n") & FALSE) }
base <- ggplot(d, aes(x, y))
tests <- list(
 geom_point = base + geom_point(alpha = 0.7, size = 1), geom_line = base + geom_line(linewidth = 0.5), geom_col = ggplot(d, aes(g, z)) + geom_col(),
 geom_bar = ggplot(d, aes(g)) + geom_bar(), geom_boxplot = ggplot(d, aes(g, z)) + geom_boxplot(outlier.shape = NA), geom_violin = ggplot(d, aes(g, z)) + geom_violin(bw = 'SJ', trim = FALSE),
 geom_histogram = ggplot(d, aes(z)) + geom_histogram(bins = 30), geom_density = ggplot(d, aes(z)) + geom_density(alpha = 0.5),
 geom_tile = ggplot(d, aes(condition, timepoint, fill = z)) + geom_tile(aes(fill = z)), geom_text = base + geom_text(aes(label = label), check_overlap = TRUE),
 geom_text_repel = base + geom_text_repel(aes(label = label), max.overlaps = Inf), mapping = base + geom_point(aes(color = group, fill = group), shape = 21),
 const = base + geom_point(color = 'red'), sx_cont = base + scale_x_continuous(limits = c(0, 10), breaks = seq(0, 10, 2), labels = scales::label_number(scale = 1e-6, suffix = 'M')),
 sy_log10 = ggplot(transform(d, y = exp(y)), aes(x, y)) + geom_point() + scale_y_log10(), sy_sqrt = ggplot(transform(d, y = abs(y)), aes(x, y)) + geom_point() + scale_y_continuous(transform = 'sqrt'),
 disc = ggplot(d, aes(g, z)) + geom_point() + scale_x_discrete(limits = c('ctrl', 'trt', 'veh')), manual = base + geom_point(aes(color = g)) + scale_color_manual(values = c(ctrl = '#0072B2', trt = '#D55E00', veh = 'grey')),
 viridis = base + geom_point(aes(color = x)) + scale_color_viridis_c(option = 'viridis'), grad2 = base + geom_point(aes(color = y)) + scale_color_gradient2(low = '#0072B2', mid = 'white', high = '#D55E00', midpoint = 0),
 date = ggplot(d, aes(dt, y)) + geom_point() + scale_x_date(date_breaks = '1 year', date_labels = '%Y'),
 fwrap = base + geom_point() + facet_wrap(~ group, ncol = 3, scales = 'free_y'), fgrid = base + geom_point() + facet_grid(rows = vars(condition), cols = vars(timepoint), scales = 'free_x'),
 fgrid2 = base + geom_point() + facet_grid(condition ~ timepoint))
for (n in names(tests)) chk(paste("geoms-scales-facets:", n), has(tests[[n]]))
sc <- tryCatch({ suppressWarnings(ggplot_build(base + geom_point(aes(color = x)) + scico::scale_color_scico(palette = 'batlow'))); TRUE }, error = function(e) { cat("   scico ERR:", conditionMessage(e), "\n"); FALSE })
chk("scale_color_scico(palette='batlow') (needs library(scico), listed in usage-guide install)", sc)
# --- fonts/PDF claims
pdf("font_default.pdf", 3.5, 2.7); print(ggplot(d, aes(x, y)) + geom_point() + labs(x = "log2 fold change", y = "Expression")); dev.off()
ggsave("font_cairo.pdf", ggplot(d, aes(x, y)) + geom_point() + labs(x = "log2 fold change", y = "Expression"), width = 89, height = 70, units = "mm", device = cairo_pdf)
ggsave("font_default_ggsave.pdf", ggplot(d, aes(x, y)) + geom_point() + labs(x = "log2 fold change", y = "Expression"), width = 89, height = 70, units = "mm")
# ggsave without units: default inches
ggsave("units_in.pdf", base + geom_point(), width = 89, height = 70, limitsize = FALSE, device = cairo_pdf)
# tiff, png, ggrastr from Saving block
library(ggrastr); pp <- ggplot(d, aes(x, y)) + rasterise(geom_point(alpha = 0.5), dpi = 300)
ggsave("t.tiff", pp, width = 89, height = 70, units = "mm", dpi = 300, compression = "lzw"); ggsave("t.png", pp, width = 89, height = 70, units = "mm", dpi = 300)
cat("png px:", paste(dim(png::readPNG("t.png"))[2:1], collapse = "x"), "(expect 1051x827)\n")
