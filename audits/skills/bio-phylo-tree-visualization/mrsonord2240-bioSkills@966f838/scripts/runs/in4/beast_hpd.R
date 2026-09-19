# Input 4 (Variant B): BEAST2 TreeAnnotator MCC chronogram with 95% HPD bars and posterior labels
suppressPackageStartupMessages({library(treeio); library(ggtree); library(ggplot2)})
b <- read.beast("../../data/beast_mcc.tree")
cat("fields:", paste(get.fields(b), collapse = ", "), "\n")
td <- as_tibble(b)
print(td[!is.na(td$posterior) & td$node > Ntip(b), c("node", "height", "height_0.95_HPD", "posterior")], n = 20)

# --- Part A: the Skill's call, as written in Failure Modes ("geom_range('height_0.95_HPD')") ---
pA <- ggtree(b) + geom_range("height_0.95_HPD")
ggsave("A_skill_geom_range_view.png", pA, width = 7, height = 4, dpi = 90)
cat("Part A built OK\n")

# --- Part B: adapted publication chronogram ---
p <- ggtree(b, size = 0.5) +
  geom_range("height_0.95_HPD", color = "steelblue", size = 3, alpha = 0.45) +
  geom_tiplab(aes(label = gsub("_", " ", label)), fontface = "italic", size = 3, offset = 3) +
  geom_nodelab(aes(label = sprintf("%.2f", posterior)), vjust = -0.7, hjust = 1.15, size = 2.6) +
  theme_tree2()
p <- revts(p) +
  scale_x_continuous(labels = abs, breaks = seq(-350, 0, 50), name = "Time before present (Ma)",
                     expand = expansion(mult = c(0.02, 0.38))) +
  labs(title = "MCC chronogram (BEAST 2 / TreeAnnotator)",
       caption = "Bars = 95% HPD of node age; labels = posterior probability (PP >= 0.95 strong; PP is not bootstrap). Synthetic tree.") +
  theme(plot.caption = element_text(size = 7))
ggsave("B_chronogram.pdf", p, width = 7.5, height = 4.5)
ggsave("B_chronogram_view.png", p, width = 7.5, height = 4.5, dpi = 120)

# verify bar coordinates against the known HPD values
bd <- ggplot_build(p)$data
rng <- bd[[which(sapply(bd, function(d) all(c("xmin", "xmax") %in% names(d))))[1]]]
print(head(rng[order(rng$xmin), c("node", "xmin", "xmax")], 12))
