suppressMessages({library(ggplot2); library(lvplot)}); cat("ggplot2", as.character(packageVersion("ggplot2")), "\n")
df <- read.csv("data/i1_synthetic_2group.csv")
t1 <- function(p, f) { r <- tryCatch({ ggsave(f, p, width=4, height=3, dpi=80); paste("ok", file.size(f)) }, error=function(e) paste("ERR", conditionMessage(e))); r }
cat("default theme, fill=group, alpha=.7:", t1(ggplot(df, aes(group, value, fill=group)) + geom_lv(k=5, alpha=0.7), "out/lv_a.png"), "\n")
cat("theme_classic, fill=group:", t1(ggplot(df, aes(group, value, fill=group)) + geom_lv(k=5, alpha=0.7) + theme_classic(base_size=10), "out/lv_b.png"), "\n")
cat("default theme, no alpha:", t1(ggplot(df, aes(group, value, fill=group)) + geom_lv(k=5), "out/lv_c.png"), "\n")
cat("default theme, fill=group, scale_fill_manual, alpha=.7:", t1(ggplot(df, aes(group, value, fill=group)) + geom_lv(k=5, alpha=0.7)+ scale_fill_manual(values=c('#0072B2','#D55E00')), "out/lv_d.png"), "\n")
