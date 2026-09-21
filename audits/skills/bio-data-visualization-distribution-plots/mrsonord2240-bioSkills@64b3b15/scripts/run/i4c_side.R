suppressMessages({library(ggplot2); library(dplyr); library(Biobase); library(ALL); library(introdataviz)})
tag <- Sys.getenv("TAG"); cat("ggplot2", as.character(packageVersion("ggplot2")), "\n")
data(ALL); e <- exprs(ALL); pd <- pData(ALL); pd <- pd[!is.na(pd$BT), ]; e <- e[, rownames(pd)]
d <- data.frame(lineage=factor(substr(as.character(pd$BT),1,1), levels=c("B","T")), cluster=factor(sub("^[BT]","",as.character(pd$BT))), expression=e["38319_at",])
d <- d[d$cluster != "", ]
# balanced subset: only stages/lineages with n >= 5 to remove the n<2 drop, to isolate side logic
d <- d %>% group_by(cluster, lineage) %>% filter(n() >= 5) %>% ungroup()
print(table(d$cluster, d$lineage))
p <- ggplot(d, aes(cluster, expression, fill = lineage)) + geom_split_violin(alpha = 0.7, trim = FALSE, bw = 'SJ') +
  geom_boxplot(width = 0.15, position = position_dodge(0.5), outlier.shape = NA) + scale_fill_manual(values = c(B = '#56B4E9', T = '#D55E00')) + theme_classic(base_size=10)
ld <- layer_data(p,1); if ("quantile" %in% names(ld)) ld <- ld[is.na(ld$quantile),]
print(unique(ld[, c("group","x","fill")]))
bx <- layer_data(p,2); print(bx[, c("group","x","xmin","xmax","fill","middle")])
ggsave(sprintf("out/i4c_side_%s.png", tag), p, width=5, height=3.5, dpi=110)
