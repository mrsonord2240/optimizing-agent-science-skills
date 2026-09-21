# Input 5b: run examples/palettes_phd.R block by block on SYNTHETIC data for every object it references (df, de_df), because the shipped file defines neither.
set.seed(20260920)
n <- 400
df <- data.frame(x=runif(n,-3,3), y=runif(n,-3,3))
df$expression <- exp(-(df$x^2+df$y^2)/4)*10 + rnorm(n,0,.3)
df$lfc <- rnorm(n, 0.4, 1.6) + ifelse(df$x>1.5, 3, 0)
df$phase <- atan2(df$y, df$x) %% (2*pi)
df$cell_type <- factor(sample(c("T","B","NK","Mono","DC","Plt","Ery","Other"), n, TRUE))
df$group <- factor(sample(c("A","B","C","D","E"), n, TRUE))
de_df <- data.frame(log2FC=rnorm(600,0,1.5)); de_df$neg_log10_p <- abs(de_df$log2FC)*runif(600,.5,4)
de_df$significance <- factor(ifelse(de_df$log2FC>1&de_df$neg_log10_p>2,"Up",ifelse(de_df$log2FC< -1&de_df$neg_log10_p>2,"Down","NS")), levels=c("Up","Down","NS"))
write.csv(df, "../data/synthetic_phd_df.csv", row.names=FALSE); write.csv(de_df, "../data/synthetic_phd_de_df.csv", row.names=FALSE)
png("../figs/i5_phd_%02d.png", 900, 700, res=110)
exprs <- parse("ex/palettes_phd.R", keep.source=FALSE)
k <- 0
for (e in exprs) {
  k <- k + 1; txt <- paste(deparse(e)[1], collapse=" "); txt <- substr(txt,1,90)
  res <- tryCatch(withCallingHandlers({ v <- withVisible(eval(e, globalenv())); if (v$visible && inherits(v$value,"ggplot")) print(v$value); "OK" },
                  warning=function(w){ message("   WARN: ", conditionMessage(w)); invokeRestart("muffleWarning") }),
                  error=function(err) paste("ERROR:", conditionMessage(err)))
  cat(sprintf("[%02d] %-92s %s\n", k, txt, res))
}
invisible(dev.off())
cat("PNG pages:", length(list.files("../figs", "^i5_phd_")), "\n")
