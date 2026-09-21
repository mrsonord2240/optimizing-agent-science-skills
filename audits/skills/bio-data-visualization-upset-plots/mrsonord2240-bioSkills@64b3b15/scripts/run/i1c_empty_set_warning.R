# Does ComplexUpset tell the user that the empty set H was dropped?
suppressMessages({library(ComplexUpset)})
D <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/data/"
d <- read.delim(paste0(D, "planted_sets.tsv"))
el <- unique(d$gene); df <- data.frame(element = el)
for (s in c("A","B","C","D","E","F","G")) df[[s]] <- df$element %in% d$gene[d$set == s]
df$H <- FALSE
w <- character(); 
p <- withCallingHandlers(upset(df, c("A","B","C","D","E","F","G","H")), warning = function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") },
                         message = function(m) { w <<- c(w, paste("MSG:", conditionMessage(m))); invokeRestart("muffleMessage") })
cat("warnings/messages raised:\n"); print(unique(w))
