# SYNTHETIC data, planted structure: equal means, different distributions (Weissgerber point)
set.seed(20260920)
ctrl <- rnorm(25, 5, 1)
trt  <- c(rnorm(40, 3, 0.5), rnorm(40, 7, 0.5))
df <- data.frame(group = factor(rep(c("Control","Treated"), c(25, 80)), levels=c("Control","Treated")),
                 value = c(ctrl, trt))
write.csv(df, "data/i1_synthetic_2group.csv", row.names=FALSE)
print(aggregate(value ~ group, df, function(x) c(n=length(x), mean=round(mean(x),3), median=round(median(x),3), sd=round(sd(x),3))))
