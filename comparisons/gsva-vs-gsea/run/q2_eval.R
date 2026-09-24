S <- "F:/OpenScience/comparisons/gsva-vs-gsea/shim/"; O <- "F:/OpenScience/comparisons/gsva-vs-gsea/out/"
ss <- read.csv(paste0(S,"ssgsea-immune-infiltration-analysis/out_q2/table/ssgsea_group_compare.csv"))
ip <- read.csv(paste0(S,"immune-pathway-analysis/out_q2/table/immune_pathway_diff.csv"))
gv <- read.csv(paste0(S,"gsva-analysis-and-visualization/out_q2/table/GSVA_diff.csv"))
o1 <- read.csv(paste0(O,"ours_q2_reactome_gsea.csv")); o2 <- read.csv(paste0(O,"ours_q2_immunecell_gsea.csv"))
rep <- function(lbl, id, eff, fdr, target) { rk <- rank(fdr, ties.method="min"); i <- match(target, id)
  cat(sprintf("%-42s n_sets=%4d n_sig=%3d | %s: dir=%+d FDR=%.2e rank=%s\n", lbl, length(id), sum(fdr<0.05), target, sign(eff[i]), fdr[i], rk[i])) }
rep("ssgsea skill (own 28-cell table, Wilcoxon)", ss$cell_type, ss$delta_mean, ss$p_adj, "Activated_CD8_T_cell")
rep("immune-pathway (own 41 Reactome immune)", ip$geneset, ip$logFC, ip$adj.P.Val, "REACTOME_INTERFERON_GAMMA_SIGNALING")
rep("gsva skill (MSigDB C2 Reactome, 1839)", gv$geneset, gv$logFC, gv$adj.P.Val, "REACTOME_INTERFERON_GAMMA_SIGNALING")
rep("ours GSEA t-rank, Reactome (msigdbr)", o1$ID, o1$NES, o1$p.adjust, "REACTOME_INTERFERON_GAMMA_SIGNALING")
rep("ours GSEA t-rank, immune cell table", o2$ID, o2$NES, o2$p.adjust, "Activated CD8 T cell")
cat("ssgsea skill: other cell types called FDR<0.05:", paste(setdiff(ss$cell_type[ss$p_adj<0.05], "Activated_CD8_T_cell"), collapse="; "), "\n")
cat("ours immune-cell GSEA: other cell types FDR<0.05:", paste(setdiff(o2$ID[o2$p.adjust<0.05], "Activated CD8 T cell"), collapse="; "), "\n")
