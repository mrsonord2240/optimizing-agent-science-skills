# GG audit run 2: SKILL.md / reference / usage-guide snippets, verbatim, with assertions on layer data and rendered output.
# Usage: r.sh g2_snippets.R <outdir>
out <- commandArgs(TRUE)[1]; dir.create(out, FALSE, TRUE); setwd(out)
suppressMessages({library(ggplot2); library(ggtext); library(ggrastr); library(ggrepel)})
cat("ggplot2", as.character(packageVersion("ggplot2")), "\n")
chk <- function(l, c) cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l))
W <- character(0)
wh <- function(expr) withCallingHandlers(expr, warning=function(w){W<<-c(W,conditionMessage(w));invokeRestart("muffleWarning")})
set.seed(11)
df <- data.frame(condition=rep(c("ctrl","trt"), each=60), expression=c(rlnorm(60,3,.8), rlnorm(60,3.6,.8)),
                 tissue=rep(c("liver","brain","kidney"), 40))
# --- Grammar in Layers block verbatim
p <- ggplot(df, aes(x = condition, y = expression)) +
    geom_boxplot(outlier.shape = NA) +
    geom_jitter(width = 0.2, alpha = 0.5) +
    scale_y_continuous(transform = 'log10', labels = scales::label_log()) +
    scale_color_manual(values = c('#0072B2', '#D55E00')) +
    labs(x = NULL, y = 'Expression (log10)', title = 'Gene X across conditions', caption = 'Source: ...') +
    facet_wrap(~ tissue, ncol = 3, scales = 'free_y') +
    theme_classic(base_size = 10) +
    theme(panel.grid = element_blank(), strip.background = element_blank(), strip.text = element_text(face = 'bold'))
W <- character(0); b <- wh(ggplot_build(p)); cat("layers-block warnings:", paste(unique(W), collapse=" | "), "\n")
chk("scale_color_manual is inert: no colour aesthetic mapped (points all one colour)", length(unique(b$data[[2]]$colour)) == 1)
ggsave("grammar_block.png", p, width=183, height=70, units="mm", dpi=150)
lab <- b$layout$panel_params[[1]]$y$get_labels(); cat("y tick labels panel 1:", paste(lab, collapse=", "), "\n")
chk("y axis title 'Expression (log10)' does not duplicate 10^n tick labels", FALSE)  # title says log10 while ticks are 10^n: recorded, judged on image
# --- ggtext label block verbatim
g <- ggplot(df, aes(expression, expression)) + geom_point() +
    labs(x = 'log<sub>2</sub> fold change', y = '−log<sub>10</sub>(*p*)') +
    theme(axis.title.x = element_markdown(), axis.title.y = element_markdown())
ggsave("ggtext.png", g, width=60, height=50, units="mm", dpi=200)
cat("ggtext y label string codepoints:", paste(utf8ToInt('−log'), collapse=" "), "(8722 = U+2212 minus)\n")
# --- Tidy eval
pc <- data.frame(PC1=rnorm(5), PC2=rnorm(5))
plot_var <- function(df, x_var, y_var) ggplot(df, aes(x = .data[[x_var]], y = .data[[y_var]])) + geom_point()
plot_var2 <- function(df, x_var, y_var) ggplot(df, aes(x = {{ x_var }}, y = {{ y_var }})) + geom_point()
chk("plot_var(df,'PC1','PC2') maps PC1/PC2", all.equal(ggplot_build(plot_var(pc,'PC1','PC2'))$data[[1]]$x, pc$PC1))
chk("plot_var2(df, PC1, PC2) maps PC1/PC2", all.equal(ggplot_build(plot_var2(pc,PC1,PC2))$data[[1]]$x, pc$PC1))
r <- ggplot_build(plot_var2(pc, 'PC1', 'PC2'))$data[[1]]; cat("plot_var2 with strings: x values unique =", length(unique(r$x)), "(1 => constant string, silently wrong)\n")
W <- character(0); r <- wh(try(ggplot_build(ggplot(pc, aes_string(x='PC1', y='PC2')) + geom_point()), silent=TRUE)); cat("aes_string conditions:", paste(unique(W), collapse=" | "), "\n")
# --- Saving block
ggsave('figure_cairo.pdf', plot = g, width = 89, height = 70, units = 'mm', device = cairo_pdf)
ggsave('figure_default.pdf', plot = g, width = 89, height = 70, units = 'mm')
ggsave('figure.tiff', g, width = 89, height = 70, units = 'mm', dpi = 300, compression = 'lzw')
ggsave('figure.png', g, width = 89, height = 70, units = 'mm', dpi = 300)
d <- dim(png::readPNG('figure.png')); cat("89 x 70 mm @300 dpi png px:", d[2], "x", d[1], "(expect 1051 x 827)\n")
# rasterise block
big <- data.frame(x = rnorm(50000), y = rnorm(50000))
pr <- ggplot(big, aes(x, y)) + rasterise(geom_point(alpha = 0.5), dpi = 300) + theme_classic()
ggsave('raster.pdf', pr, device = cairo_pdf, width=89, height=70, units='mm')
ggsave('vector.pdf', ggplot(big, aes(x, y)) + geom_point(alpha = 0.5) + theme_classic(), device = cairo_pdf, width=89, height=70, units='mm')
cat(sprintf("rasterised pdf %d B vs all-vector pdf %d B\n", file.size('raster.pdf'), file.size('vector.pdf')))
# --- Guardrail / failure-mode claims
b <- ggplot_build(ggplot(df, aes(expression, expression)) + geom_point(aes(color = 'red')))
cat("aes(color='red') colour rendered:", unique(b$data[[1]]$colour), "(failure-modes.md says 'blue (or whatever default)'; geom default palette first hue is #F8766D salmon)\n")
# ggrepel max.overlaps claims
set.seed(3); sp <- data.frame(x=runif(60), y=runif(60), label=paste0("g",1:60))        # 60 well-spread labels
set.seed(4); dn <- data.frame(x=rnorm(60,sd=.02), y=rnorm(60,sd=.02), label=paste0("g",1:60)) # 60 dense labels
nlab <- function(p) { W2 <- character(0); f <- tempfile(fileext=".png"); png(f, 600, 450, res=100)
  withCallingHandlers(print(p), warning=function(w){W2<<-c(W2,conditionMessage(w));invokeRestart("muffleWarning")}, message=function(m){W2<<-c(W2,conditionMessage(m));invokeRestart("muffleMessage")}); dev.off()
  im <- png::readPNG(f); ink <- sum(apply(im[,,1:3], c(1,2), max) < 0.2)   # dark pixels = label text + point glyphs
  c(dark_px=ink, conditions=length(W2)) }
rp <- function(d, ...) ggplot(d, aes(x,y)) + geom_point() + geom_text_repel(aes(label=label), ...)
cat("spread N=60 default:", nlab(rp(sp)), " | Inf:", nlab(rp(sp, max.overlaps=Inf)), "\n")
cat("dense  N=60 default:", nlab(rp(dn)), " | Inf:", nlab(rp(dn, max.overlaps=Inf)), "\n")
W <- character(0); invisible(wh(ggplot_build(rp(dn))))
# Does the claim 'N > 10 labels' trigger? spread labels all drawn at N=60 => no.
# --- Reference geom/scales
cat("--- geoms-scales-facets.md blocks ---\n")
set.seed(5); d2 <- data.frame(x=runif(200,0,1e7), y=rnorm(200,50,10), group=sample(c("Control","Treatment","Vehicle"),200,TRUE), label=paste0("g",1:200),
  z=rnorm(200), tissue=sample(c("liver","brain"),200,TRUE), tp=sample(c("0h","6h"),200,TRUE), cond=sample(c("A","B"),200,TRUE), date=as.Date("2020-01-01")+sample(0:1500,200,TRUE))
t1 <- function(n, e) { W <<- character(0); r <- tryCatch({wh(ggplot_build(e)); "ok"}, error=function(x) paste("ERROR", conditionMessage(x))); cat(sprintf("%-44s %s %s\n", n, r, paste(unique(W), collapse=" ; "))) }
g0 <- ggplot(d2, aes(x, y))
t1("geom_violin(bw='SJ', trim=FALSE)", ggplot(d2, aes(group, y)) + geom_violin(bw='SJ', trim=FALSE))
t1("geom_line(linewidth)", g0 + geom_line(linewidth=.5))
t1("geom_line(size) deprecated", g0 + geom_line(size=.5))
t1("geom_text(check_overlap)", g0 + geom_text(aes(label=label), check_overlap=TRUE))
t1("scale_x_continuous(limits 0-10, label_number 1e-6 M)", g0 + geom_point() + scale_x_continuous(limits=c(0,10), breaks=seq(0,10,2), labels=scales::label_number(scale=1e-6, suffix='M')))
t1("scale_y_continuous(transform='sqrt')", g0 + geom_point() + scale_y_continuous(transform='sqrt'))
t1("scale_color_scico(batlow)", g0 + geom_point(aes(color=z)) + scico::scale_color_scico(palette='batlow'))
t1("scale_fill_gradient2", ggplot(d2, aes(tissue,tp,fill=z)) + geom_tile() + scale_fill_gradient2(low='#0072B2', mid='white', high='#D55E00', midpoint=0))
t1("scale_x_date", ggplot(d2, aes(date,y)) + geom_point() + scale_x_date(date_breaks='1 year', date_labels='%Y'))
t1("facet_grid(rows=vars, cols=vars, free_x)", g0 + geom_point() + facet_grid(rows=vars(cond), cols=vars(tp), scales='free_x'))
bl <- ggplot_build(g0 + geom_point() + facet_grid(rows=vars(cond), cols=vars(tp), scales='free_x')); chk("facet_grid 2x2", nrow(bl$layout$layout)==4)
tc <- theme_classic(); cat("theme_classic panel.grid already blank:", inherits(tc$panel.grid, "element_blank"), "; axis.line class:", class(tc$axis.line)[1], "(theme_classic has no top/right axis lines to remove, usage-guide tip is inert)
")
theme_pub <- theme_classic(base_size = 10) + theme(panel.grid = element_blank(), axis.text = element_text(color = 'black'),
        axis.ticks = element_line(color = 'black', linewidth = 0.3), axis.line = element_line(color = 'black', linewidth = 0.3),
        legend.position = 'right', legend.key.size = unit(0.4, 'cm'), strip.background = element_blank(),
        strip.text = element_text(face = 'bold', size = 9), plot.title = element_text(face = 'bold', size = 11), plot.tag = element_text(face = 'bold', size = 11))
t1("theme_pub verbatim", g0 + geom_point(aes(color=group)) + facet_wrap(~tissue) + labs(title="t", tag="A") + theme_pub)
