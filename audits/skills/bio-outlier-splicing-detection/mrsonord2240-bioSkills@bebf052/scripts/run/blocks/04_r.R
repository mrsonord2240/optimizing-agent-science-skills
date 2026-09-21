p <- read.table('patient_outlier_clusterPvals.txt', header = TRUE, sep = '\t', check.names = FALSE)
long <- data.frame(cluster = rep(rownames(p), ncol(p)), sampleID = rep(colnames(p), each = nrow(p)),
                   p = unlist(p, use.names = FALSE))
long <- long[!is.na(long$p), ]
long$q <- p.adjust(long$p, method = 'BH')
hits <- long[long$q < 0.05, ]
