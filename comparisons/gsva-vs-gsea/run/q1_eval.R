suppressMessages(library(jsonlite))
S <- "F:/OpenScience/comparisons/gsva-vs-gsea/shim/"; O <- "F:/OpenScience/comparisons/gsva-vs-gsea/out/"
tr <- fromJSON("F:/OpenScience/comparisons/gsva-vs-gsea/data/truth.json"); nulls <- tr$correlated_null_sets
gv <- read.csv(paste0(S,"gsva-analysis-and-visualization/out_q1/table/GSVA_diff.csv"))
ip <- read.csv(paste0(S,"immune-pathway-analysis/out_q1/table/immune_pathway_diff.csv"))
ss <- read.csv(paste0(S,"ssgsea-immune-infiltration-analysis/out_q1/table/ssgsea_group_compare.csv"))
gs <- read.csv(paste0(O,"ours_q1_gsea_t.csv")); cm <- read.csv(paste0(O,"ours_q1_camera_NA.csv")); c0 <- read.csv(paste0(O,"ours_q1_camera_default.csv"))
res <- list(
 gsva_skill = data.frame(id=gv$geneset, eff=gv$logFC, fdr=gv$adj.P.Val),
 immune_pathway = data.frame(id=ip$geneset, eff=ip$logFC, fdr=ip$adj.P.Val),
 ssgsea_skill_wilcox = data.frame(id=ss$cell_type, eff=ss$delta_mean, fdr=ss$p_adj),
 ours_GSEA_limma_t = data.frame(id=gs$ID, eff=gs$NES, fdr=gs$p.adjust),
 ours_CAMERA_NA = data.frame(id=cm$ID, eff=ifelse(cm$Direction=="Up",1,-1), fdr=cm$FDR),
 ours_CAMERA_default = data.frame(id=c0$ID, eff=ifelse(c0$Direction=="Up",1,-1), fdr=c0$FDR))
out <- do.call(rbind, lapply(names(res), function(n) { d <- res[[n]]; d$rk <- rank(d$fdr, ties.method="min")
  cc <- d[d$id=="KEGG_CELL_CYCLE",]; ox <- d[d$id=="KEGG_OXIDATIVE_PHOSPHORYLATION",]
  data.frame(side=n, n_sets=nrow(d), n_sig=sum(d$fdr<0.05), cellcycle_dir=sign(cc$eff), cellcycle_fdr=signif(cc$fdr,3),
    oxphos_dir=sign(ox$eff), oxphos_fdr=signif(ox$fdr,3), corr_null_sig=sum(d$fdr[d$id %in% nulls]<0.05), corr_null_n=sum(d$id %in% nulls)) }))
print(out, row.names=FALSE); write.csv(out, paste0(O,"q1_summary.csv"), row.names=FALSE)
# duplicate check: gsva-skill vs immune-pathway with identical gene sets + method
m <- merge(gv, ip, by="geneset"); cat("gsva-skill vs immune-pathway: n=", nrow(m), " max|dlogFC|=", max(abs(m$logFC.x-m$logFC.y)), " max|dP|=", max(abs(m$adj.P.Val.x-m$adj.P.Val.y)), "\n")
# clean nulls: KEGG sets with zero gene overlap with any planted set and not a correlated-null set
suppressMessages(library(msigdbr))
kegg <- msigdbr(species="Homo sapiens", collection="C2", subcollection="CP:KEGG_LEGACY"); K <- split(kegg$gene_symbol, kegg$gs_name)
E <- read.csv("F:/OpenScience/comparisons/gsva-vs-gsea/data/expr.csv", check.names=FALSE)$gene
pl <- unique(c(K[["KEGG_CELL_CYCLE"]], K[["KEGG_OXIDATIVE_PHOSPHORYLATION"]],
  unique(msigdbr(species="Homo sapiens", collection="C2", subcollection="CP:REACTOME")[["gene_symbol"]][msigdbr(species="Homo sapiens", collection="C2", subcollection="CP:REACTOME")$gs_name=="REACTOME_INTERFERON_GAMMA_SIGNALING"])))
clean <- names(K)[sapply(K, function(x) length(intersect(x, pl))==0)]; clean <- setdiff(clean, nulls)
cat("clean-null KEGG sets (no planted overlap, not correlated-null):", length(clean), "\n")
for (n in names(res)) { d <- res[[n]]; cat(sprintf("%-22s clean-null sets called FDR<0.05: %d of %d\n", n, sum(d$fdr[d$id %in% clean]<0.05), sum(d$id %in% clean))) }
