.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# What does the Skill's ash() call return for proteins whose limma coefficient is NA?
suppressPackageStartupMessages(library(ashr))
set.seed(5); b <- c(rnorm(300, 0, 0.2), rnorm(30, 1.5, 0.2)); s <- rep(0.2, 330)
b[c(1, 320)] <- NA; s[c(1, 320)] <- NA
a <- ash(b, s, mixcompdist = 'normal')
print(a$result[c(1, 2, 320, 321), c('betahat', 'sebetahat', 'PosteriorMean', 'lfsr')])
