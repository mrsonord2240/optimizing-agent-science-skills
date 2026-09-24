# OURS request 4: same loop, using the run_mediation() function shipped in OUR examples/eqtl_mediation.R (extracted verbatim, sims=500 hardcoded there).
source('F:/OpenScience/comparisons/mediation-same-id/run/common.R'); suppressMessages(library(mediation))
ph <- read.csv(file.path(D, 'C_pheno.csv')); M <- read.csv(file.path(D, 'C_mediators.csv')); dat <- cbind(ph, M); set.seed(1)
src <- readLines('F:/optimized-scientific-skills/skills/bio-causal-genomics-mediation-analysis/examples/eqtl_mediation.R')
i0 <- grep('^run_mediation <- function', src); i1 <- which(src == '}' & seq_along(src) > i0)[1]
eval(parse(text = src[i0:i1]))
genes <- c('M1', 'M2', 'M3', 'M4')
res <- try_run('as written', do.call(rbind, lapply(genes, function(g) run_mediation(dat, g, covars = c('age', 'sex')))))
if (is.null(res)) {
  cat('--- adapt: embed the formula object in the model call (same fix as theirs_r4.R) ---
')
  run_mediation <- function(dat, gene_col, covars = c('age', 'sex')) {
    cs <- paste(covars, collapse = ' + ')
    mf <- as.formula(paste(gene_col, '~ genotype +', cs)); of <- as.formula(paste('disease ~ genotype +', gene_col, '+', cs))
    mm <- eval(bquote(lm(.(mf), data = dat))); om <- eval(bquote(glm(.(of), data = dat, family = binomial)))
    r <- mediate(mm, om, treat = 'genotype', mediator = gene_col, boot = TRUE, sims = 500)
    data.frame(gene = gene_col, acme = r$d0, acme_p = r$d0.p, ade = r$z0, prop_mediated = r$n0) }
  res <- do.call(rbind, lapply(genes, function(g) run_mediation(dat, g, covars = c('age', 'sex'))))
}
res$acme_fdr <- p.adjust(res$acme_p, method = 'BH'); print(res)
sigg <- res$gene[res$acme_fdr < 0.05]; cat('significant at BH<0.05:', sigg, '\n')
stopifnot(all(c('M1','M2') %in% sigg)); cat('ASSERT pass: M1,M2 detected\n'); cat('decoys flagged:', intersect(sigg, c('M3','M4')), '\n')
stopifnot(!any(c('M3','M4') %in% sigg)); cat('ASSERT pass: decoys M3,M4 not flagged\n')
