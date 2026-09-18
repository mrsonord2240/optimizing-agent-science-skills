# Quick check on the stored 40-term all-null GO table: BH and lambda=0 q-value both
# should report zero discoveries.
go <- read.csv("../data/go_all_null_reaudit.csv")
p <- go$pvalue
cat(sprintf("m=%d, min p=%.4f\n", length(p), min(p)))
cat(sprintf("BH discoveries at 0.05: %d\n", sum(p.adjust(p,'BH') < 0.05)))
library(qvalue)
q0 <- qvalue(p, lambda = 0)
cat(sprintf("qvalue(lambda=0): pi0=%.4f, discoveries q<0.05: %d\n", q0$pi0, sum(q0$qvalues < 0.05)))
