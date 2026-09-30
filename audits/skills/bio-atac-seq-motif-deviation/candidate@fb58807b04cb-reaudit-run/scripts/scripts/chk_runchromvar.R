if (nzchar(Sys.getenv("SIGNAC_LIB"))) .libPaths(c(Sys.getenv("SIGNAC_LIB"), .libPaths()))
cat(as.character(packageVersion("Signac")), "RunChromVAR exported:", "RunChromVAR" %in% getNamespaceExports("Signac"), "\n")
