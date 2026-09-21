# Which of the two gaps breaks the example's GRanges: NA position (unparsable HGVSp) or NA colour (class missing from the 7-class palette)?
suppressMessages({library(trackViewer); library(GenomicRanges)})
try_ <- function(label, expr) { cat("\n==== ", label, "\n"); tryCatch({expr; cat("OK\n")}, error=function(e) cat("ERROR:", conditionMessage(e), "\n")) }
pal <- c(Missense_Mutation = '#D55E00', Nonsense_Mutation = '#000000')
try_("NA position only", { s <- GRanges('chr17', IRanges(c(175, NA), width = 1), color = pal[c("Missense_Mutation","Missense_Mutation")], score = c(5, 1)) })
try_("class not in palette only (Translation_Start_Site)", { s <- GRanges('chr17', IRanges(c(175, 1), width = 1), color = pal[c("Missense_Mutation","Translation_Start_Site")], score = c(5, 1)) })
print(pal[c("Missense_Mutation","Translation_Start_Site")])
try_("both fine", { s <- GRanges('chr17', IRanges(c(175, 1), width = 1), color = pal[c("Missense_Mutation","Nonsense_Mutation")], score = c(5, 1)) })
