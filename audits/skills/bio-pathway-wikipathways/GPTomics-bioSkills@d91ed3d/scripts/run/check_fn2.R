suppressMessages({library(clusterProfiler); library(rWikiPathways); library(org.Hs.eg.db)})
cat("exists get_wp_organisms:", exists("get_wp_organisms"), "\n")
# search all loaded namespaces
for (pkg in loadedNamespaces()) {
  ns <- asNamespace(pkg)
  if (exists("get_wp_organisms", envir=ns, inherits=FALSE)) cat("found in", pkg, "\n")
}
cat("packageVersion rWikiPathways:", as.character(packageVersion('rWikiPathways')), "\n")
