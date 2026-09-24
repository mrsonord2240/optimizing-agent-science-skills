# THEIRS request 4: eQTL-style multi-gene mediation loop with BH (their run_eqtl_mediation, verbatim) on dataset C, genes M1..M4.
# Truth: M1,M2 mediate; M3 (alpha only) and M4 (beta only) do not.
source('F:/OpenScience/comparisons/mediation-same-id/run/common.R'); suppressMessages(library(mediation))
ph <- read.csv(file.path(D, 'C_pheno.csv')); M <- read.csv(file.path(D, 'C_mediators.csv')); dat <- cbind(ph, M); set.seed(1)
run_eqtl_mediation <- function(dat, snp_col, expr_col, outcome_col, covariates) {
  covar_formula <- paste(covariates, collapse = ' + ')
  med_formula <- as.formula(paste(expr_col, '~', snp_col, '+', covar_formula))
  out_formula <- as.formula(paste(outcome_col, '~', snp_col, '+', expr_col, '+', covar_formula))
  med_model <- lm(med_formula, data = dat)
  if (length(unique(dat[[outcome_col]])) == 2) { out_model <- glm(out_formula, data = dat, family = binomial) } else { out_model <- lm(out_formula, data = dat) }
  result <- mediate(med_model, out_model, treat = snp_col, mediator = expr_col, boot = TRUE, sims = 1000)
  data.frame(snp = snp_col, gene = expr_col, acme = result$d0, acme_p = result$d0.p, ade = result$z0, ade_p = result$z0.p, total = result$tau.coef, total_p = result$tau.p, prop_mediated = result$n0)
}
genes <- c('M1', 'M2', 'M3', 'M4'); covars <- c('age', 'sex')
res <- try_run('as written', do.call(rbind, lapply(genes, function(g) run_eqtl_mediation(dat, 'genotype', g, 'disease', covars))))
if (is.null(res)) {
  cat('--- adapt: embed the formula object in the model call (bootstrap refits evaluate the call in mediate frame, not the function frame) ---
')
  run_eqtl_mediation <- function(dat, snp_col, expr_col, outcome_col, covariates) {
    cf <- paste(covariates, collapse = ' + ')
    mf <- as.formula(paste(expr_col, '~', snp_col, '+', cf)); of <- as.formula(paste(outcome_col, '~', snp_col, '+', expr_col, '+', cf))
    mm <- eval(bquote(lm(.(mf), data = dat))); om <- eval(bquote(glm(.(of), data = dat, family = binomial)))
    r <- mediate(mm, om, treat = snp_col, mediator = expr_col, boot = TRUE, sims = 1000)
    data.frame(gene = expr_col, acme = r$d0, acme_p = r$d0.p, ade = r$z0, prop_mediated = r$n0) }
  res <- do.call(rbind, lapply(genes, function(g) run_eqtl_mediation(dat, 'genotype', g, 'disease', covars)))
}
res$acme_fdr <- p.adjust(res$acme_p, method = 'BH'); print(res[, c('gene','acme','acme_p','acme_fdr','prop_mediated')])
sigg <- res$gene[res$acme_fdr < 0.05]; cat('significant at BH<0.05:', sigg, '\n')
stopifnot(all(c('M1','M2') %in% sigg)); cat('ASSERT pass: M1,M2 detected\n'); cat('decoys flagged:', intersect(sigg, c('M3','M4')), '\n')
stopifnot(!any(c('M3','M4') %in% sigg)); cat('ASSERT pass: decoys M3,M4 not flagged\n')
