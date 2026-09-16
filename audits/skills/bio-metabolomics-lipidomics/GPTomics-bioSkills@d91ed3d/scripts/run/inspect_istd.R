suppressMessages(library(lipidr))
cat(deparse(args(annotate_lipids)), "\n")
# find istd detection logic
src <- deparse(lipidr:::annotate_lipids)
cat(paste(src[grepl("istd", src, ignore.case=TRUE)], collapse="\n"), "\n")
