h2 <- readRDS("i3_h2_heights.rds"); hs <- scan("i3_scipy_heights.txt", quiet = TRUE)
cat("R ward.D2 heights vs scipy ward heights max abs diff:", signif(max(abs(sort(h2) - sort(hs))), 3), "\n")
x <- as.matrix(read.csv("i3_x.csv", row.names = 1)); h1 <- hclust(dist(x), "ward.D")
cat("R ward.D heights vs scipy max abs diff:", signif(max(abs(sort(h1$height) - sort(hs))), 3), "\n")
