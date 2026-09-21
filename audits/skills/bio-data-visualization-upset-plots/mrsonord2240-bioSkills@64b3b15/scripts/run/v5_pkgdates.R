for (p in c("ComplexUpset","UpSetR")) { d <- packageDescription(p); cat(p, d$Version, "Packaged:", d$Packaged, " Date/Publication:", d$`Date/Publication`, " Repository:", d$Repository, "\n") }
cat("has intersects?", exists("intersects", asNamespace("UpSetR")), "\n")
h <- readLines(file.path(find.package("ComplexUpset"), "NEWS.md"), n = 25); cat(h, sep = "\n")
