for (p in c("ComplexHeatmap","pheatmap","circlize","seriation","dendextend","scico","ALL","Biobase","airway","RColorBrewer","cmcrameri")) {
  v <- tryCatch(as.character(packageVersion(p)), error=function(e) "MISSING"); cat(p, v, "\n")
}
cat(R.version.string, "\n"); cat(.libPaths(), sep="\n")
