# Input 3 (Edge): small N, zero-inflated single-cell-like data, ties, NA, notch, N-annotation snippet, bandwidth claims. SYNTHETIC data with planted structure.
suppressMessages({library(ggplot2); library(dplyr)})
cat("ggplot2", as.character(packageVersion("ggplot2")), "\n")
chk <- function(label, ok, note="") cat(sprintf("[%s] %s %s\n", if (isTRUE(ok)) "PASS" else "FAIL", label, note))
try_msgs <- function(expr) { w <- character(); e <- NULL
  val <- withCallingHandlers(tryCatch(expr, error=function(x) { e <<- conditionMessage(x); NULL }), warning=function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") }, message=function(x) { w <<- c(w, paste("msg:", conditionMessage(x))); invokeRestart("muffleMessage") })
  list(val=val, err=e, warn=unique(w)) }

## (a) bandwidth claim: "nrd0 IS Silverman; nrd (Scott) oversmooths less than Silverman"
set.seed(1); x <- c(rnorm(50,0,1), rnorm(50,4,1))
cat("bw.nrd0 (Silverman)", round(bw.nrd0(x),4), " bw.nrd (Scott)", round(bw.nrd(x),4), " ratio nrd/nrd0", round(bw.nrd(x)/bw.nrd0(x),4), "\n")
chk("SKILL claim 'nrd (Scott) oversmooths less than Silverman(nrd0)' is TRUE", bw.nrd(x) < bw.nrd0(x), "-> nrd is 1.06/0.9 = 1.178x LARGER, i.e. it oversmooths MORE")
seps <- c(1.5, 2, 2.5, 3, 4)
xs <- lapply(seps, function(sep) { set.seed(3); c(rnorm(100,0,1), rnorm(100,sep,1)) })
nmodes <- function(v, bw) length(which(diff(sign(diff(density(v, bw=bw)$y))) == -2))
tab <- data.frame(sep = seps, modes_nrd0 = sapply(xs, nmodes, "nrd0"), modes_nrd = sapply(xs, nmodes, "nrd"), modes_SJ = sapply(xs, nmodes, "SJ"))
print(tab)
cat("(n=200 equal-weight mixture, sd=1 each; modes counted in density(); SKILL claims default Silverman collapses bimodal to one peak and SJ fixes it)\n")

## (b) zero-inflated single-cell-like data, the case the SKILL names
set.seed(42)
mk <- function(n, pz) { z <- runif(n) < pz; ifelse(z, 0, round(rlnorm(n, 1.2, 0.35), 2)) }
sc <- rbind(data.frame(cluster="C1", expression=mk(300, 0.6)), data.frame(cluster="C2", expression=mk(250, 0.2)),
            data.frame(cluster="C3", expression=mk(5, 0.4)), data.frame(cluster="C4", expression=rep(0, 40)))
print(sc %>% group_by(cluster) %>% summarise(n=n(), zero_frac=round(mean(expression==0),2), distinct=n_distinct(expression)))
r <- try_msgs({ p <- ggplot(sc, aes(cluster, expression, fill=cluster)) + geom_violin(trim=FALSE, bw="SJ"); ggsave("out/i3_sc_sj.png", p, width=5, height=3.5, dpi=100); p })
cat("SKILL violin recipe geom_violin(trim=FALSE, bw='SJ') on zero-inflated clusters: error =", if (is.null(r$err)) "none" else r$err, "\n"); cat("  warnings:", paste(head(r$warn,4), collapse=" || "), "\n")
chk("bw='SJ' violin draws all 4 zero-inflated clusters without error/warning", is.null(r$err) && length(r$warn)==0)
for (cl in unique(sc$cluster)) { xx <- sc$expression[sc$cluster==cl]; rr <- try_msgs(bw.SJ(xx)); cat(sprintf("   bw.SJ(%s: n=%d) -> %s\n", cl, length(xx), if (is.null(rr$err)) round(rr$val,4) else paste("ERROR:", rr$err))) }
r2 <- try_msgs({ p <- ggplot(sc, aes(cluster, expression, fill=cluster)) + geom_violin(); ggsave("out/i3_sc_default.png", p, width=5, height=3.5, dpi=100); p })
cat("default violin same data: error =", if (is.null(r2$err)) "none" else r2$err, " warnings:", paste(head(r2$warn,3), collapse=" || "), "\n")
# trim=FALSE + bounded data: violin density below 0 (impossible expression)
r2b <- try_msgs({ p <- ggplot(sc[sc$cluster %in% c("C1","C2"),], aes(cluster, expression, fill=cluster)) + geom_violin(trim=FALSE, bw="nrd0"); layer_data(p, 1) })
if (!is.null(r2b$val)) { vd <- r2b$val; if ("quantile" %in% names(vd)) vd <- vd[is.na(vd$quantile),]
  cat("trim=FALSE (nrd0) violin y-range for C1,C2 (data min is 0, expression cannot be negative):\n"); print(aggregate(y ~ group, vd, function(v) round(range(v),3)))
  chk("trim=FALSE keeps violin within physically possible range (>=0)", all(vd$y >= 0), sprintf("min drawn y = %.3f", min(vd$y))) }

## (c) small N: n=5, n=3, n=1
sm <- data.frame(group=rep(c("A","B","C"), c(5,3,1)), value=c(2.1,2.5,3.9,4.2,2.2, 5.0,5.3,4.8, 9.9))
for (bw in c("nrd0","SJ")) { r3 <- try_msgs({ p <- ggplot(sm, aes(group, value)) + geom_violin(bw=bw); ggplot_build(p) })
  cat(sprintf("violin bw=%s at n=5/3/1: error=%s | warnings=%s\n", bw, if (is.null(r3$err)) "none" else r3$err, paste(r3$warn, collapse=" || "))) }
r3 <- try_msgs({ p <- ggplot(sm, aes(group, value)) + geom_violin(bw="SJ"); layer_data(p,1) }); if (!is.null(r3$val)) cat("groups actually drawn by the SJ violin at n=5/3/1:", paste(sort(unique(r3$val$group)), collapse=","), "(1=A n=5, 2=B n=3, 3=C n=1)\n")

## (d) notch with small N
nb <- data.frame(group=rep(c("A","B"), each=8), value=c(c(1,1.2,1.4,3,3.1,3.2,5,5.1), c(2,2.5,2.7,2.9,3.0,4.5,4.6,9)))
r4 <- try_msgs({ p <- ggplot(nb, aes(group, value)) + geom_boxplot(notch=TRUE); ggsave("out/i3_notch8.png", p, width=3, height=3, dpi=90); p })
cat("notch=TRUE n=8 warnings:", paste(r4$warn, collapse=" || "), "\n")
chk("SKILL: notch at N<15 warns 'notch went outside hinges'", any(grepl("notch went outside hinges", r4$warn, ignore.case=TRUE)))
ld <- layer_data(r4$val, 1); qA <- quantile(nb$value[nb$group=="A"], c(.25,.5,.75))
chk("notch limits equal median +/- 1.58*IQR/sqrt(n)", isTRUE(all.equal(c(ld$notchlower[1], ld$notchupper[1]), as.numeric(qA[2] + c(-1,1)*1.58*diff(qA[c(1,3)])/sqrt(8)))), sprintf("drawn [%.3f, %.3f]", ld$notchlower[1], ld$notchupper[1]))

## (e) N annotation snippet (SKILL 'No N annotation' fix), verbatim
set.seed(7); dn <- data.frame(group=rep(c("Control","Drug"), c(12, 20)), value=c(rnorm(12, 5), rnorm(20, 6)))
r5 <- try_msgs({ p <- ggplot(dn, aes(group, value)) + geom_boxplot() +
   stat_summary(geom='text', fun.data = function(x) data.frame(label = paste('n=', length(x)))); ggsave("out/i3_nsnippet.png", p, width=3.5, height=3.2, dpi=100); ggplot_build(p) })
cat("stat_summary(geom='text', fun.data=function(x) data.frame(label=paste('n=', length(x)))) -> error:", if (is.null(r5$err)) "none" else r5$err, "| warnings:", paste(r5$warn, collapse=" || "), "\n")
chk("SKILL's stat_summary N-label snippet draws n labels", is.null(r5$err) && !is.null(r5$val))
r5b <- try_msgs({ p <- ggplot(dn, aes(group, value)) + geom_boxplot() + stat_summary(geom='text', fun.data = function(x) data.frame(y=max(x), label = paste0('n=', length(x))), vjust=-0.5); ggsave("out/i3_nsnippet_fixed.png", p, width=3.5, height=3.2, dpi=100); layer_data(p, 2) })
cat("variant with y = max(x):", if (is.null(r5b$err)) paste(r5b$val$label, collapse=",") else r5b$err, "\n")
dn2 <- dn %>% add_count(group) %>% mutate(lab = paste0(group, " (n=", n, ")"))
lv <- levels(factor(dn2$lab)); chk("tick-label N: labels 'Control (n=12)', 'Drug (n=20)'", identical(lv, c("Control (n=12)", "Drug (n=20)")), paste(lv, collapse=" | "))

## (f) NA handling in N annotation (example script logic: count(group) counts rows, not observations)
set.seed(9); dna <- data.frame(group=rep(c("A","B"), each=10), value=c(rnorm(10), c(rnorm(6), NA,NA,NA,NA)))
nl <- dna %>% count(group); nobs <- dna %>% group_by(group) %>% summarise(n=sum(!is.na(value)))
cat("example-script N label (count(group)):", paste(nl$group, nl$n, collapse="; "), "| points actually drawn:", paste(nobs$group, nobs$n, collapse="; "), "\n")
chk("N annotation via count(group) equals points drawn when NA present", identical(nl$n, nobs$n), "(B labelled n=10 but 6 points exist)")

## (g) bar of mean claim on planted equal-mean data
d1 <- read.csv("data/i1_synthetic_2group.csv")
bars <- tapply(d1$value, d1$group, mean); cat("bar heights (means) Control/Treated:", round(bars,3), "\n")
cat("Treated points within 0.5 of its mean:", sum(abs(d1$value[d1$group=="Treated"] - bars["Treated"]) < 0.5), "of 80\n")
