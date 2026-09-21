suppressMessages(library(ggplot2))
df <- read.csv("data/i1_synthetic_2group.csv"); df$group <- factor(df$group, levels=c("Control","Treated"))
cat("ggplot2", as.character(packageVersion("ggplot2")), "\n")
p <- ggplot(df, aes(group, value)) + geom_violin(trim=FALSE, bw="SJ")
vd <- layer_data(p,1)
cat("rows", nrow(vd), "cols", paste(names(vd), collapse=","), "\n"); print(table(vd$group))

cat("y sorted within group?", all(sapply(split(vd$y, vd$group), function(v) !is.unsorted(v))), "\n")
# independent density
d <- density(df$value[df$group=="Control"], bw="SJ", n=512, cut=3); cat("independent density raw maxima Control:", length(which(diff(sign(diff(d$y)))==-2)), "\n")
d <- density(df$value[df$group=="Treated"], bw="SJ", n=512, cut=3); cat("independent density raw maxima Treated:", length(which(diff(sign(diff(d$y)))==-2)), "\n")
if (requireNamespace("gghalves", quietly=TRUE) && as.character(packageVersion("ggplot2"))=="3.5.2") {
  library(gghalves)
  p4 <- ggplot(df, aes(group, value)) + geom_half_point(side='l', range_scale=0.4, position=position_nudge(x=-0.2))
  l <- layer_data(p4,1); cat("half_point rows", nrow(l), " y range", range(l$y), " data range", range(df$value), "\n"); print(head(l))
}
