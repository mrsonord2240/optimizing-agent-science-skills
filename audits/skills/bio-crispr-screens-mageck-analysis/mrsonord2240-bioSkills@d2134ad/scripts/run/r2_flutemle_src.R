find_pkg <- find.package("MAGeCKFlute")
cat(find_pkg, "\n")
src <- list.files(find_pkg, recursive=TRUE, pattern="FluteMLE", full.names=TRUE)
print(src)
