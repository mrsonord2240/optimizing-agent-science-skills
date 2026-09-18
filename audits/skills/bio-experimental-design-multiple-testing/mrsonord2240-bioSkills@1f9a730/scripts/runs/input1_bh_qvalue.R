# Input 1 (Canonical, regression of pre-fix Input 1) -- follows SKILL.md
# "FDR -- Benjamini-Hochberg and the q-value" verbatim.
de <- read.csv("../data/de_pvalues_reaudit.csv")
p <- de$pvalue
is_alt <- de$is_true_alt == "True"

padj <- p.adjust(p, method = 'BH')
sum(padj < 0.05)

library(qvalue)
qobj <- qvalue(p)
qobj$pi0
q    <- qobj$qvalues
lfdr <- qobj$lfdr

report <- function(name, sig) {
  R <- sum(sig); TP <- sum(sig & is_alt); FP <- sum(sig & !is_alt)
  cat(sprintf("%-22s R=%5d true+=%5d false+=%4d realized FDP=%.4f power=%.4f\n",
              name, R, TP, FP, ifelse(R>0, FP/R, 0), TP/sum(is_alt)))
}

cat(sprintf("true pi0 = %.4f\n", 1 - sum(is_alt)/length(is_alt)))
cat(sprintf("BH discoveries at FDR 0.05: %d\n", sum(padj < 0.05)))
cat(sprintf("qvalue estimated pi0: %.4f\n", qobj$pi0))
cat(sprintf("Storey q-value discoveries q<0.05: %d\n", sum(q < 0.05)))
report("BH q<=0.05", padj <= 0.05)
report("Storey q<0.05", q < 0.05)
report("local FDR < 0.20", lfdr < 0.20)
report("Bonferroni 0.05", p.adjust(p,'bonferroni') < 0.05)
report("Holm 0.05", p.adjust(p,'holm') < 0.05)
report("BY 0.05", p.adjust(p,'BY') < 0.05)
