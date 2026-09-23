suppressMessages(library(lipidr))
data(data_normalized, package = 'lipidr')
cat(sprintf("R=%s\nlipidr=%s\n", R.version.string, as.character(packageVersion("lipidr"))))
cat(sprintf("data_normalized dimensions=%d x %d\n", nrow(data_normalized), ncol(data_normalized)))
