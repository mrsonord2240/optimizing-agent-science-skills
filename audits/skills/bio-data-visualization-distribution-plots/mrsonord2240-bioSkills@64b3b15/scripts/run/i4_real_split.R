# Input 4 (Variant B): REAL data. Bioconductor ALL (Chiaretti 2004 ALL microarray, 128 samples): most B-vs-T discriminating probe, per stage.
# SKILL blocks used: split violin (introdataviz) + boxplot dodge, bw='SJ', trim=FALSE, N in tick labels.
suppressMessages({library(ggplot2); library(dplyr); library(Biobase); library(ALL); library(introdataviz)})
cat("ggplot2", as.character(packageVersion("ggplot2")), "\n")
chk <- function(label, ok, note="") cat(sprintf("[%s] %s %s\n", if (isTRUE(ok)) "PASS" else "FAIL", label, note))
data(ALL); e <- exprs(ALL); pd <- pData(ALL)
pd <- pd[!is.na(pd$BT), ]; e <- e[, rownames(pd)]
lin <- factor(substr(as.character(pd$BT), 1, 1), levels=c("B","T")); stage <- sub("^[BT]", "", as.character(pd$BT))
cat("BT table:\n"); print(table(as.character(pd$BT)))
tt <- apply(e, 1, function(v) abs(t.test(v ~ lin)$statistic)); probe <- names(which.max(tt)); cat("most B/T discriminating probe:", probe, " |t| =", round(max(tt),1), "\n")
if (requireNamespace("hgu95av2.db", quietly=TRUE)) { suppressMessages(library(hgu95av2.db)); cat("symbol:", paste(unlist(mget(probe, hgu95av2SYMBOL)), collapse=","), "\n") }
d <- data.frame(sample=rownames(pd), lineage=lin, cluster=ifelse(stage == "", "0", stage), expression=e[probe, ])
d <- d[d$cluster != "0", ]   # samples with only 'B'/'T' and no stage are dropped: labelled
d$cluster <- factor(d$cluster)
cat("cells (stage x lineage) n:\n"); print(with(d, table(cluster, lineage)))
truth <- d %>% group_by(cluster, lineage) %>% summarise(n=n(), med=median(expression), .groups="drop"); print(truth)

# SKILL split-violin block, verbatim aesthetics (fill = condition -> lineage), with SKILL example-script arguments (trim=FALSE, bw='SJ')
p <- ggplot(d, aes(cluster, expression, fill = lineage)) +
    geom_split_violin(alpha = 0.7, trim = FALSE, bw = 'SJ') +
    geom_boxplot(width = 0.15, position = position_dodge(0.5), outlier.shape = NA) +
    scale_fill_manual(values = c(B = '#56B4E9', T = '#D55E00')) +
    labs(x = 'Stage', y = 'Expression', fill = NULL) +
    theme_classic(base_size = 10) + theme(legend.position = 'top')
ggsave("out/i4_split.png", p, width=6, height=3.8, dpi=110)
ld <- layer_data(p, 2)
bm <- as.numeric(ld$middle)
tm <- truth %>% arrange(cluster, lineage) %>% pull(med)
chk("box medians equal per-(stage,lineage) data medians", isTRUE(all.equal(bm[order(ld$xmin + 0)], tm[order(as.numeric(as.factor(paste(truth$cluster, truth$lineage))))], check.attributes=FALSE)) || isTRUE(all.equal(sort(bm), sort(tm))), paste(round(sort(bm),2), collapse=","))
chk("8 boxes drawn (4 stages x 2 lineages)", nrow(ld) == 8)
lv <- layer_data(p, 1); if ("quantile" %in% names(lv)) lv <- lv[is.na(lv$quantile), ]
cat("violin fill per group id:", paste(sapply(sort(unique(lv$group)), function(g) unique(lv$fill[lv$group==g])), collapse=" "), "\n")
chk("violin group ids odd=B (left half), even=T (right half) at every stage", all(sapply(sort(unique(lv$group)), function(g) unique(lv$fill[lv$group==g])) == rep(c("#56B4E9", "#D55E00"), 4)))

# EDGE: one stage has only one lineage (a cluster present in one condition only) -> half-assignment shifts
d2 <- d[!(d$cluster == "2" & d$lineage == "B"), ]
p2 <- ggplot(d2, aes(cluster, expression, fill = lineage)) + geom_split_violin(alpha = 0.7, trim = FALSE, bw = 'SJ') +
    geom_boxplot(width = 0.15, position = position_dodge(0.5), outlier.shape = NA) + scale_fill_manual(values = c(B = '#56B4E9', T = '#D55E00')) + theme_classic(base_size=10)
ggsave("out/i4_split_missingB.png", p2, width=6, height=3.8, dpi=110)
lv2 <- layer_data(p2, 1); if ("quantile" %in% names(lv2)) lv2 <- lv2[is.na(lv2$quantile), ]
cols <- sapply(sort(unique(lv2$group)), function(g) unique(lv2$fill[lv2$group==g])); cat("with stage-2 B removed, violin group ids/fills:", paste(sort(unique(lv2$group)), cols, collapse=" | "), "\n")
side <- sapply(sort(unique(lv2$group)), function(g) if (g %% 2 == 1) "left" else "right"); names(side) <- cols
cat("half drawn on the left/right, by colour (B blue #56B4E9, T orange #D55E00):", paste(names(side), side, sep="=", collapse=" "), "\n")
tside <- side[cols == "#D55E00"]; chk("T (orange) is always drawn on the right half, also when the paired B is missing", all(tside == "right"), paste("T sides:", paste(tside, collapse=",")))

# small-N groups actually plotted with a KDE violin
small <- truth %>% filter(n < 15); cat("cells with n < 15 that still get a KDE violin:", paste(small$cluster, small$lineage, small$n, sep=":", collapse="  "), "\n")

# N annotation, per SKILL guidance, via tick label; every cell
d <- d %>% add_count(cluster, lineage, name="n_cell")
labs_n <- d %>% group_by(cluster) %>% summarise(lab = paste0("Stage ", first(cluster), "\n(B n=", sum(lineage=="B"), ", T n=", sum(lineage=="T"), ")"), .groups="drop")
cat("tick labels:", paste(gsub("\n", " ", labs_n$lab), collapse=" | "), "\n")
p3 <- p + scale_x_discrete(labels = setNames(labs_n$lab, labs_n$cluster))
ggsave("out/i4_split_n.png", p3, width=6.5, height=4, dpi=110)
chk("N per cell in tick labels equals table", identical(as.integer(table(d$lineage[d$cluster=="1"])), c(sum(d$lineage=="B" & d$cluster=="1"), sum(d$lineage=="T" & d$cluster=="1"))))
