.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
cat('R version:', R.version.string, '\n')
pkgs <- c('clusterProfiler','fgsea','DOSE','org.Hs.eg.db','GO.db','msigdbr','ReactomePA','reactome.db','enrichplot','limma','DESeq2','edgeR','GSVA','gprofiler2')
for (p in pkgs) {
  v <- tryCatch(as.character(packageVersion(p)), error=function(e) 'NOT INSTALLED')
  cat(sprintf('%-16s %s\n', p, v))
}
