suppressMessages({library(clusterProfiler)})
cat("get_wp_organisms in package:clusterProfiler exports:", "get_wp_organisms" %in% ls("package:clusterProfiler"), "\n")
res <- tryCatch(get_wp_organisms(), error=function(e) e)
if (inherits(res, 'error')) { cat("ERROR:", conditionMessage(res), "\n") } else {
  cat("class:", class(res), " length:", length(res), "\n")
  print(head(res, 10))
  cat("Danio rerio present:", "Danio rerio" %in% res, "\n")
}
