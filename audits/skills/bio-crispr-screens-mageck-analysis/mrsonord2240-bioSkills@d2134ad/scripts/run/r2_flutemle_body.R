library(MAGeCKFlute)
b <- deparse(body(FluteMLE))
writeLines(b, "flutemle_body.txt")
