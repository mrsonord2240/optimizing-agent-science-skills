# GG audit run 1: shipped scripts/publication_figures.R on real airway DESeq2 results + mtcars PCA.
# Usage: r.sh g1_example.R <skilldir> <outdir>
a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE); setwd(out)
suppressMessages({library(ggplot2); library(ggrepel); library(patchwork)})
cat("ggplot2", as.character(packageVersion("ggplot2")), " R", as.character(getRversion()), "\n")
chk <- function(l, c) cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l))
source(file.path(skill, "scripts/publication_figures.R"))
raw <- read.csv("F:/OpenScience/audit-envs/data-visualization/public-data/differential-expression/airway_dex_deseq2_results.csv")
cat("airway rows", nrow(raw), " padj NA:", sum(is.na(raw$padj)), " pvalue NA:", sum(is.na(raw$pvalue)), "\n")
# A. function on RAW results (NA padj kept; as the Skill's own volcano use case would)
W <- character(0)
p_raw <- withCallingHandlers(create_volcano(raw), warning=function(w){W<<-c(W,conditionMessage(w));invokeRestart("muffleWarning")})
b <- withCallingHandlers(ggplot_build(p_raw), warning=function(w){W<<-c(W,conditionMessage(w));invokeRestart("muffleWarning")})
cat("warnings building volcano on raw results:", paste(unique(W), collapse=" | "), "\n")
d <- p_raw$data
sig <- table(d$significance); print(sig)
indep_up <- sum(raw$padj < .05 & raw$log2FoldChange > 1, na.rm=TRUE); indep_dn <- sum(raw$padj < .05 & raw$log2FoldChange < -1, na.rm=TRUE)
chk(sprintf("class counts equal independent (Up %d, Down %d)", indep_up, indep_dn), sig[["Up"]]==indep_up && sig[["Down"]]==indep_dn)
labs <- d$label[!is.na(d$label) & d$label != ""]
cat("labelled genes:", length(labs), "\n")
top10 <- raw$gene[order(raw$padj)][1:10]
chk("labels are the 10 smallest padj genes", setequal(labs, top10))
# threshold line vs colour boundary
hy <- -log10(0.05)
sigcol <- d[d$significance != "NS", ]
min_sig <- min(-log10(sigcol$pvalue))
above_grey <- sum(-log10(d$pvalue) > hy & d$significance == "NS", na.rm=TRUE)
above_grey_lfc <- sum(-log10(d$pvalue) > hy & d$significance == "NS" & abs(d$log2FoldChange) > 1, na.rm=TRUE)
cat(sprintf("hline y=%.3f (=-log10 FDR cutoff) ; smallest -log10(raw p) among coloured points = %.3f ; grey points above line = %d (of which |LFC|>1: %d)\n", hy, min_sig, above_grey, above_grey_lfc))
chk("horizontal threshold equals the colour boundary (min -log10 p of coloured points)", abs(hy - min_sig) < 0.05)
cat("y label expression:", deparse(p_raw$labels$y), "\n")
ggsave("volcano_raw.png", p_raw, width=7, height=5, dpi=150)
# B. how many of the top-10 labels are actually drawn at max.overlaps=20 (as shipped)
png("repel_probe.png", 1050, 750, res=150); print(p_raw); gl <- grid::grid.ls(grid::grid.force(), print=FALSE, grobs=TRUE, viewports=FALSE); dev.off()
cat("textrepel grobs (labelled points drawn incl. '' strings):", sum(grepl("textrepel", gl$name)), "\n")
W2 <- character(0); png("repel_probe2.png", 1050, 750, res=150)
withCallingHandlers(print(p_raw), warning=function(w){W2<<-c(W2,conditionMessage(w));invokeRestart("muffleWarning")}, message=function(m){W2<<-c(W2,conditionMessage(m));invokeRestart("muffleMessage")}); dev.off()
cat("conditions at draw:", paste(unique(W2), collapse=" | "), "\n")
# overlapping labels? measure via repel result: build labels count only; visual check by image
# C. clean results (NA removed) -> other functions
res <- raw[!is.na(raw$padj), ]
p1 <- create_volcano(res)
set.seed(7); df <- data.frame(g=rep(c("A","B","C"), each=20), v=c(rnorm(20), rnorm(20,1), rnorm(20,2)))
p2 <- create_boxplot(df, "g", "v", "g")
bx <- ggplot_build(p2); jit <- bx$data[[2]]
meds <- tapply(df$v, df$g, median)
chk("boxplot medians equal raw group medians", all.equal(as.numeric(bx$data[[1]]$middle), as.numeric(meds)))
chk("boxplot jitter has all 60 points", nrow(jit) == 60)
p2n <- create_boxplot(df, "g", "v")   # no fill_var
ggsave("box_nofill.png", p2n, width=4, height=3, dpi=120)
pc <- prcomp(mtcars[,-1], scale.=TRUE); ve <- 100*pc$sdev^2/sum(pc$sdev^2)
pdf_ <- data.frame(pc$x[,1:2], cyl=factor(mtcars$cyl), am=factor(mtcars$am), var_explained=ve[1:2])
p3 <- create_pca_plot(pdf_, "cyl", "am")
cat(sprintf("PCA axis labels: %s | %s (independent PC1 %.1f%%, PC2 %.1f%%)\n", p3$labels$x, p3$labels$y, ve[1], ve[2]))
chk("PCA axis labels carry prcomp variance", p3$labels$x == sprintf("PC1 (%s%%)", round(ve[1],1)) && p3$labels$y == sprintf("PC2 (%s%%)", round(ve[2],1)))
r <- try(create_pca_plot(pdf_[, c("PC1","PC2","cyl")], "cyl"), silent=TRUE)
cat("create_pca_plot without var_explained column ->", if (inherits(r,"try-error")) paste("ERROR:", gsub("\n"," ",conditionMessage(attr(r,"condition")))) else "ok", "\n")
many <- cbind(pdf_, grp=factor(rep(letters[1:12], length.out=32)))
Wm <- character(0); withCallingHandlers({ pm <- create_pca_plot(many, "grp"); ggplot_build(pm) }, warning=function(w){Wm<<-c(Wm,conditionMessage(w));invokeRestart("muffleWarning")})
cat("create_pca_plot with 12 groups (Set1 max 9):", paste(unique(Wm), collapse=" | "), "\n")
# D. save_publication_figure
save_publication_figure(p1, "pub_fig")
cat("pub_fig.png px:", paste(dim(png::readPNG("pub_fig.png"))[2:1], collapse=" x "), " (expect 2100 x 1500)\n")
# E. multi-panel
mp3 <- create_multi_panel(p1, p2, p3); ggsave("multi3.png", mp3, width=180, height=150, units="mm", dpi=150)
mp4 <- create_multi_panel(p1, p2, p3, p2); ggsave("multi4.png", mp4, width=180, height=150, units="mm", dpi=150)
th <- theme_publication()
cat("standalone theme_publication has panel.border:", !inherits(th$panel.border, "element_blank") , "\n")
ggsave("standalone_p3.png", p3, width=90, height=75, units="mm", dpi=150)
# F. palette vs SKILL baseline: Okabe-Ito
cat("publication_colors:", paste(names(publication_colors), publication_colors, sep="=", collapse=" "), "\n")
oi <- c("#0072B2", "#D55E00"); cat("Okabe-Ito pair in example palette:", any(toupper(oi) %in% toupper(publication_colors)), "\n")
cat("theme_publication is based on theme_bw + panel.border (SKILL baseline: theme_classic, no border):", !inherits(th$panel.border,"element_blank"), "\n")
cat("create_boxplot fill palette: Brewer Set2; create_pca_plot: Brewer Set1 (not Okabe-Ito); publication_colors used only by create_volcano\n")
# G. determinism: two calls of create_boxplot jitter positions
j1 <- ggplot_build(create_boxplot(df, "g", "v"))$data[[2]]$x; j2 <- ggplot_build(create_boxplot(df, "g", "v"))$data[[2]]$x
chk("create_boxplot jitter identical across two builds (seeded)", identical(j1, j2))
