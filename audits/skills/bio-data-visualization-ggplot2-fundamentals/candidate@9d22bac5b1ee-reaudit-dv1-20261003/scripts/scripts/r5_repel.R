# failure-modes claim: default max.overlaps drops labels (with a warning); Inf draws all. Counted from drawn grobs.
a <- commandArgs(TRUE); out <- a[1]; dir.create(out, FALSE, TRUE); setwd(out)
suppressMessages({library(ggplot2); library(ggrepel); library(grid)})
cat("ggplot2", as.character(packageVersion("ggplot2")), " ggrepel", as.character(packageVersion("ggrepel")), "\n")
set.seed(1); dd <- data.frame(x = rnorm(300, sd = .02), y = rnorm(300, sd = .02), l = paste0("GENE", 1:300))
drawn <- function(p) { W <- character(0); png("t.png", 900, 700, res = 100)
  withCallingHandlers({ print(p); grid.force() }, warning = function(w) { W <<- c(W, paste('warning:', conditionMessage(w))); invokeRestart("muffleWarning") },
    message = function(m) { W <<- c(W, paste('message:', conditionMessage(m))); invokeRestart("muffleMessage") })
  g <- grid.ls(grobs = TRUE, viewports = FALSE, print = FALSE); dev.off()
  list(n = sum(grepl("^textrepelgrob", g$name)), warn = unique(W)) }
a1 <- drawn(ggplot(dd, aes(x, y, label = l)) + geom_point() + geom_text_repel(size = 3))
a2 <- drawn(ggplot(dd, aes(x, y, label = l)) + geom_point() + geom_text_repel(size = 3, max.overlaps = Inf, seed = 1))
cat("default: labels drawn", a1$n, "of 300; warning:", a1$warn, "\n")
cat("max.overlaps=Inf: labels drawn", a2$n, "of 300; warning:", length(a2$warn), "\n")
