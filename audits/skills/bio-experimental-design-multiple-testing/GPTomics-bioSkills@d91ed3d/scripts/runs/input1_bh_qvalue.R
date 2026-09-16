.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 1 (Canonical) -- code written by following SKILL.md sections
# "FDR -- Benjamini-Hochberg and the q-value".
# Data: SYNTHETIC, planted ground truth in column is_truly_de.

d <- read.csv('F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/synthetic_de_pvalues.csv')
p <- d$pvalue
truth <- d$is_truly_de == 1
cat(sprintf('SYNTHETIC input: %d features, %d true alternatives (true pi0 = %.4f)\n',
            length(p), sum(truth), mean(!truth)))

# --- SKILL.md pattern, verbatim -------------------------------------------
padj <- p.adjust(p, method = 'BH')
cat(sprintf('BH discoveries at FDR 0.05 : %d\n', sum(padj < 0.05)))

library(qvalue)
qobj <- qvalue(p)
q    <- qobj$qvalues
lfdr <- qobj$lfdr
cat(sprintf('qvalue estimated pi0        : %.4f  (true pi0 = %.4f)\n', qobj$pi0, mean(!truth)))
cat(sprintf('q-value discoveries q<0.05  : %d\n', sum(q < 0.05)))

# --- audit-only: score the procedures against the planted truth ------------
score <- function(sel, label) {
  R <- sum(sel); V <- sum(sel & !truth); S <- sum(sel & truth)
  cat(sprintf('%-22s R=%5d  true+=%5d  false+=%4d  realized FDP=%.4f  power=%.4f\n',
              label, R, S, V, ifelse(R > 0, V / R, 0), S / sum(truth)))
}
cat('\n-- realized false discovery proportion against planted truth --\n')
score(p    < 0.05, 'uncorrected p<0.05')
score(padj < 0.05, 'BH q<=0.05')
score(q    < 0.05, 'Storey q<0.05')
score(lfdr < 0.20, 'local FDR < 0.20')
score(p.adjust(p, 'bonferroni') < 0.05, 'Bonferroni 0.05')
score(p.adjust(p, 'holm')       < 0.05, 'Holm 0.05')
score(p.adjust(p, 'BY')         < 0.05, 'BY 0.05')

cat('\nlocal FDR range: ', sprintf('%.4f .. %.4f', min(lfdr), max(lfdr)), '\n')
cat('sessionInfo pkg versions: qvalue', as.character(packageVersion('qvalue')), '\n')
