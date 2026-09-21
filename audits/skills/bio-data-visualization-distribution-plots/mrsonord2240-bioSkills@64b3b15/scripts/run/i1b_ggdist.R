# Is there a working R raincloud on the current stack (ggplot2 4.0.3) using packages the SKILL already lists (ggdist)? Same data as input 1.
suppressMessages({library(ggplot2); library(ggdist)}); cat("ggplot2", as.character(packageVersion("ggplot2")), "ggdist", as.character(packageVersion("ggdist")), "\n")
df <- read.csv("data/i1_synthetic_2group.csv"); df$group <- factor(df$group, levels=c("Control","Treated"))
p <- ggplot(df, aes(group, value, fill = group, color = group)) +
  stat_halfeye(adjust = 1, width = 0.6, .width = 0, justification = -0.2, point_colour = NA, alpha = 0.7, bw = "SJ") +
  geom_boxplot(width = 0.15, outlier.shape = NA, alpha = 0.7, color = "black") +
  geom_point(position = position_jitter(width = 0.05, height = 0, seed = 1), alpha = 0.5, size = 1.5, shape = 16, aes(x = as.numeric(group) - 0.2)) +
  scale_fill_manual(values = c('#0072B2', '#D55E00')) + scale_color_manual(values = c('#0072B2', '#D55E00')) + coord_flip()
r <- tryCatch({ ggsave("out/i1b_ggdist_raincloud_gg4.png", p, width=5, height=3.5, dpi=110); "ok" }, error=function(e) conditionMessage(e))
cat("ggdist raincloud on ggplot2 4.0.3:", r, file.size("out/i1b_ggdist_raincloud_gg4.png"), "bytes\n")
ld <- layer_data(p, 2); cat("box medians:", round(ld$middle, 3), "data medians:", round(tapply(df$value, df$group, median), 3), "\n")
