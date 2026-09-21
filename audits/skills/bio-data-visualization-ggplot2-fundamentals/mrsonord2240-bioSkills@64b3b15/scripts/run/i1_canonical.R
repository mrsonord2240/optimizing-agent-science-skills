# Input 1 (Canonical): publication volcano-type scatter of REAL airway DESeq2 results, per SKILL.md
source("F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/run/common.R")
suppressPackageStartupMessages({library(ggrepel); library(ggtext); library(dplyr)})
res <- read.csv(DE); cat("rows", nrow(res), " NA padj", sum(is.na(res$padj)), " NA pvalue", sum(is.na(res$pvalue)), "\n")
res <- res %>% filter(!is.na(padj)) %>%
  mutate(sig = case_when(padj < 0.05 & log2FoldChange > 1 ~ "Up", padj < 0.05 & log2FoldChange < -1 ~ "Down", TRUE ~ "NS"),
         label = ifelse(rank(padj, ties.method = "first") <= 10, gene, ""))
tab <- table(res$sig); print(tab)
okabe <- c(Up = "#D55E00", Down = "#0072B2", NS = "grey70")
theme_pub <- theme_classic(base_size = 10) +
  theme(panel.grid = element_blank(), axis.text = element_text(color = 'black'),
        axis.ticks = element_line(color = 'black', linewidth = 0.3), axis.line = element_line(color = 'black', linewidth = 0.3),
        legend.position = 'right', legend.key.size = unit(0.4, 'cm'), strip.background = element_blank(),
        strip.text = element_text(face = 'bold', size = 9), plot.title = element_text(face = 'bold', size = 11),
        plot.tag = element_text(face = 'bold', size = 11))

mk <- function(ylab) ggplot(res, aes(log2FoldChange, -log10(pvalue), color = sig)) +
  geom_point(alpha = 0.7, size = 1) +
  geom_text_repel(aes(label = label), color = "black", size = 2.5, max.overlaps = Inf, min.segment.length = 0) +
  scale_color_manual(values = okabe, breaks = c("Up","Down","NS")) +
  labs(x = 'log<sub>2</sub> fold change', y = ylab, color = NULL) +
  theme_pub + theme(axis.title.x = element_markdown(), axis.title.y = element_markdown())

# (a) ggtext snippet AS WRITTEN in SKILL.md: '\\u2212' inside single quotes in R source
ylab_asis <- '\\u2212log<sub>10</sub>(*p*)'
cat("SKILL.md y-label string as R sees it: ", ylab_asis, "\n")
cat("   contains literal backslash-u2212 (not a minus sign): ", grepl("\\\\u2212", ylab_asis), "\n")
ylab_fix <- '\u2212log<sub>10</sub>(*p*)'
p_asis <- mk(ylab_asis); p_fix <- mk(ylab_fix)

# (b) numbers behind the plot
b <- ggplot_build(p_fix); ld <- b$data[[1]]
chk("points layer has one row per non-NA-padj gene", nrow(ld) == nrow(res))
cmap <- c(Up="#D55E00", Down="#0072B2", NS="#B3B3B3")   # grey70 -> #B3B3B3
hex <- function(x) toupper(rgb(t(col2rgb(x)), maxColorValue = 255))
got <- table(factor(hex(ld$colour), levels = hex(unname(cmap)), labels = names(cmap)))
chk(paste("colour counts Up/Down/NS match input:", paste(got, collapse="/"), "vs", paste(as.integer(tab[c("Up","Down","NS")]), collapse="/")),
    all(as.integer(got) == as.integer(tab[c("Up","Down","NS")])))
up_x <- ld$x[hex(ld$colour) == "#D55E00"]; dn_x <- ld$x[hex(ld$colour) == "#0072B2"]
chk("all Up-colour points have log2FC > 1, all Down < -1", all(up_x > 1) && all(dn_x < -1))
lab <- b$data[[2]]; shown <- lab$label[lab$label != ""]
chk(paste("10 labels drawn with max.overlaps=Inf (n =", length(shown), ")"), length(shown) == 10 && all(shown %in% res$gene))
chk("labelled genes are the 10 smallest padj", setequal(shown, res$gene[order(res$padj)][1:10]))
chk("x scale range covers data", b$layout$panel_params[[1]]$x.range[1] <= min(res$log2FoldChange) && b$layout$panel_params[[1]]$x.range[2] >= max(res$log2FoldChange))
cat("axis titles:", b$plot$labels$x, "|", b$plot$labels$y, "\n")

# (c) export as the Skill directs
for (nm in c("asis", "fix")) {
  p <- if (nm == "asis") p_asis else p_fix
  ggsave(file.path(OUT, paste0("i1_", nm, ".pdf")), p, width = 89, height = 70, units = "mm", device = cairo_pdf)
  ggsave(file.path(OUT, paste0("i1_", nm, ".png")), p, width = 89, height = 70, units = "mm", dpi = 300)
}
pdf_info(file.path(OUT, "i1_fix.pdf"))   # inspected by pdfinfo.py: MediaBox 252x198 pt, TrueType embedded, no Type3
pi <- png_info(file.path(OUT, "i1_fix.png"))
chk("PNG is 89 mm at 300 dpi = 1051 x 827 px", abs(pi$w - 1051) <= 1 && abs(pi$h - 827) <= 1)
# default ggsave pdf, for the Skill's 'fonts not embedded' claim
ggsave(file.path(OUT, "i1_default.pdf"), p_fix, width = 89, height = 70, units = "mm")
pdf_info(file.path(OUT, "i1_default.pdf"))
# pitfall: units omitted
r <- tryCatch({ ggsave(file.path(OUT, "i1_inches2.png"), p_fix, width = 89, height = 70); "no error" }, error = function(e) conditionMessage(e))
cat("ggsave(width=89,height=70) with no units: ", r, "\n")
