# Remaining SKILL.md R blocks, run with SYNTHETIC data, asserting content
suppressMessages({library(ggplot2);library(viridis);library(RColorBrewer);library(ggsci);library(circlize);library(scales);library(colorspace)})
set.seed(1); d <- data.frame(x=rnorm(200), y=rnorm(200)); d$v <- d$x + rnorm(200,0,.5); d$g <- factor(sample(letters[1:6],200,TRUE))
png("../figs/i7_blocks_%02d.png", 700, 500, res=100)
for (o in c('viridis','magma','inferno','plasma','cividis','turbo')) {
  p <- ggplot(d, aes(x,y,color=v)) + geom_point() + scale_color_viridis_c(option=o) + ggtitle(o); print(p)
  b <- ggplot_build(p)$data[[1]]; cat(o, "n colours drawn:", length(unique(b$colour)), " lowest-value point colour:", b$colour[which.min(d$v)], " highest:", b$colour[which.max(d$v)], "\n")
}
cat("\nBrewer blocks:\n")
for (a in list(list(8,'Dark2'),list(9,'YlOrRd'),list(11,'RdBu'))) { r <- brewer.pal(n=a[[1]], name=a[[2]]); cat(a[[2]], length(r), ifelse(length(r)==a[[1]],"OK","LEN MISMATCH"), r[1], "\n") }
display.brewer.all(colorblindFriendly = TRUE); cat("display.brewer.all(colorblindFriendly=TRUE) drew\n")
r <- try(brewer.pal(n=9,name='Set3')); cat("Set3 n=9 fine; max 12:", brewer.pal.info["Set3","maxcolors"], "\n")
cat("\nggsci scales:\n")
for (f in c(scale_color_npg, scale_color_aaas, scale_color_lancet, scale_color_jama, scale_color_jco, scale_color_nejm)) { p <- ggplot(d, aes(x,y,color=g)) + geom_point() + f(); print(p); cat(length(unique(ggplot_build(p)$data[[1]]$colour)), "colours for 6 groups; ") }
cat("\n\nCustom construction:\n")
my_palette <- c('Control'='#0072B2','Treatment'='#D55E00','Vehicle'='#009E73')
x <- colorRampPalette(c('#0072B2','white','#D55E00'))(100); cat("colorRampPalette len", length(x), " mid pair:", x[50], x[51], " ends:", x[1], x[100], "\n")
cat("Odd-N centre check: colorRampPalette(...)(101)[51] =", colorRampPalette(c('#0072B2','white','#D55E00'))(101)[51], "\n")
col_fun <- colorRamp2(c(-2,0,2), c('#0072B2','white','#D55E00')); cat("colorRamp2 at -2,0,2:", col_fun(c(-2,0,2)), "\n")
cat("lightgrey midpoint failure-mode example EEEEEE distance from white (L* diff):", round(100 - coords(as(hex2RGB("#EEEEEE"),"LAB"))[,"L"],1), "\n")
dev.off()
