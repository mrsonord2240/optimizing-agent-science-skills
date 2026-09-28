root <- "/mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs"
out <- file.path(root, "evidence", "valid-api-smoke.json")
results <- list()

run_case <- function(name, expr) {
  warnings <- character()
  started <- proc.time()[["elapsed"]]
  value <- NULL
  error <- NULL
  tryCatch(
    withCallingHandlers(
      value <- force(expr),
      warning = function(w) {
        warnings <<- c(warnings, conditionMessage(w))
        invokeRestart("muffleWarning")
      }
    ),
    error = function(e) error <<- conditionMessage(e)
  )
  results[[name]] <<- list(
    status = if (is.null(error)) "PASS" else "FAIL",
    elapsed_seconds = proc.time()[["elapsed"]] - started,
    warnings = warnings,
    error = error,
    evidence = value
  )
  invisible(value)
}

expect_error <- function(expr, pattern = NULL) {
  message <- tryCatch({ force(expr); NULL }, error = conditionMessage)
  if (is.null(message)) stop("expected an error but call succeeded")
  if (!is.null(pattern) && !grepl(pattern, message, ignore.case = TRUE)) {
    stop("unexpected error: ", message)
  }
  message
}

run_case("gsdesign_obf_and_survival", {
  suppressPackageStartupMessages(library(gsDesign))
  obf <- gsDesign(
    k = 3, test.type = 1, alpha = 0.025, beta = 0.10,
    sfu = sfLDOF, timing = c(0.33, 0.67, 1)
  )
  surv <- gsSurv(
    k = 3, test.type = 2, alpha = 0.025, beta = 0.10,
    sfu = sfLDOF, lambdaC = 0.04, hr = 0.65, eta = 0.005,
    T = 30, minfup = 18, ratio = 1
  )
  stopifnot(
    length(obf$upper$bound) == 3L,
    all(diff(obf$upper$bound) < 0),
    abs(sum(obf$upper$prob[, 1]) - 0.025) < 1e-6,
    surv$en > 0,
    tail(surv$n.I, 1) > 0
  )
  list(
    boundary_z = unname(obf$upper$bound),
    null_crossing_probability = sum(obf$upper$prob[, 1]),
    survival_total_subjects = unname(surv$en),
    survival_final_events = unname(tail(surv$n.I, 1))
  )
})

run_case("rpact_ssr_and_combination", {
  suppressPackageStartupMessages(library(rpact))
  design_ssr <- getDesignGroupSequential(
    kMax = 1, alpha = 0.025, beta = 0.20, sided = 1,
    typeOfDesign = "asUser", userAlphaSpending = 0.025
  )
  ss12 <- getSampleSizeMeans(
    design = design_ssr, alternative = 5, stDev = 12, groups = 2
  )
  ss14 <- getSampleSizeMeans(
    design = design_ssr, alternative = 5, stDev = 14, groups = 2
  )
  inverse <- getDesignInverseNormal(
    kMax = 2, alpha = 0.025, beta = 0.20, sided = 1,
    informationRates = c(0.5, 1), typeOfDesign = "asUser",
    userAlphaSpending = c(0.0125, 0.025)
  )
  fisher <- getDesignFisher(kMax = 3, alpha = 0.025, sided = 1)
  stopifnot(
    ss14$maxNumberOfSubjects > ss12$maxNumberOfSubjects,
    inverse$kMax == 2,
    fisher$kMax == 3
  )
  list(
    subjects_sd12 = ss12$maxNumberOfSubjects,
    subjects_sd14 = ss14$maxNumberOfSubjects,
    inverse_critical_values = unname(inverse$criticalValues),
    fisher_critical_values = unname(fisher$criticalValues)
  )
})

run_case("boin_deterministic_oc", {
  suppressPackageStartupMessages(library(BOIN))
  boundary <- get.boundary(
    target = 0.30, ncohort = 10, cohortsize = 3, n.earlystop = 12,
    p.saf = 0.18, p.tox = 0.42
  )
  args <- list(
    target = 0.30,
    p.true = c(0.05, 0.10, 0.20, 0.30, 0.40, 0.55),
    ncohort = 10, cohortsize = 3, ntrial = 300,
    n.earlystop = 12, seed = 20260928
  )
  oc1 <- do.call(get.oc, args)
  oc2 <- do.call(get.oc, args)
  stopifnot(
    identical(oc1$selpercent, oc2$selpercent),
    abs(sum(oc1$selpercent) - 100) < 1e-8,
    boundary$lambda_e < 0.30,
    boundary$lambda_d > 0.30
  )
  list(
    lambda_e = boundary$lambda_e,
    lambda_d = boundary$lambda_d,
    selected_mtd_percent = unname(oc1$selpercent),
    expected_total_n = oc1$totaln,
    seed = 20260928
  )
})

run_case("dfcrm_deterministic_crm", {
  suppressPackageStartupMessages(library(dfcrm))
  args <- list(
    PI = c(0.05, 0.10, 0.20, 0.30, 0.40, 0.55),
    prior = c(0.05, 0.10, 0.20, 0.30, 0.50, 0.65),
    target = 0.30, n = 30, x0 = 1, nsim = 100, mcohort = 1,
    count = FALSE, method = "bayes", model = "logistic", seed = 20260928
  )
  sim1 <- do.call(crmsim, args)
  sim2 <- do.call(crmsim, args)
  stopifnot(identical(sim1, sim2), inherits(sim1, "sim"))
  list(
    class = class(sim1),
    fields = names(sim1),
    seed = 20260928,
    simulations = 100
  )
})

run_case("rbest_map_mixture_ess", {
  suppressPackageStartupMessages(library(RBesT))
  historical <- data.frame(
    study = c("study1", "study2", "study3"),
    n = c(40, 35, 50), r = c(8, 6, 12)
  )
  set.seed(20260928)
  map_mcmc <- gMAP(
    cbind(r, n - r) ~ 1 | study,
    data = historical, family = binomial,
    tau.dist = "HalfNormal", tau.prior = 0.5,
    beta.prior = cbind(0, 2),
    iter = 2400, warmup = 800, thin = 2, chains = 2, cores = 1
  )
  map_mix <- automixfit(map_mcmc)
  map_ess <- ess(map_mix)
  stopifnot(is.finite(map_ess), map_ess > 0, ncol(map_mix) > 0)
  list(
    mixture_components = ncol(map_mix),
    effective_sample_size = unname(map_ess),
    seed = 20260928,
    iterations = 2400,
    chains = 2
  )
})

run_case("gsdesign2_nonph_design", {
  suppressPackageStartupMessages(library(gsDesign2))
  design <- gs_design_ahr(analysis_time = c(18, 24, 30, 36))
  stopifnot(inherits(design, "gs_design"), nrow(design$analysis) == 4L)
  list(analysis_rows = nrow(design$analysis), analysis_columns = names(design$analysis))
})

run_case("simtrial_fixed_n", {
  suppressPackageStartupMessages(library(simtrial))
  set.seed(20260928)
  simulations <- sim_fixed_n(
    n_sim = 20, sample_size = 120, target_event = 80,
    total_duration = 36
  )
  stopifnot(is.data.frame(simulations), nrow(simulations) > 0)
  list(rows = nrow(simulations), columns = names(simulations), seed = 20260928)
})

run_case("adaptr_multiarm_rar_engine", {
  suppressPackageStartupMessages(library(adaptr))
  spec <- setup_trial_binom(
    arms = c("control", "dose_a", "dose_b"),
    true_ys = c(0.30, 0.40, 0.45),
    max_n = 60, look_after_every = 15,
    control = "control", min_probs = rep(0.10, 3),
    highest_is_best = TRUE, n_draws = 1000
  )
  trials1 <- run_trials(spec, n_rep = 20, cores = 1, base_seed = 20260928)
  trials2 <- run_trials(spec, n_rep = 20, cores = 1, base_seed = 20260928)
  stopifnot(
    identical(trials1$trial_results, trials2$trial_results),
    length(trials1$trial_results) == 20L
  )
  list(replicates = length(trials1$trial_results), seed = 20260928, arms = 3)
})

run_case("invalid_input_contracts", {
  suppressPackageStartupMessages(library(gsDesign))
  suppressPackageStartupMessages(library(rpact))
  suppressPackageStartupMessages(library(BOIN))
  suppressPackageStartupMessages(library(dfcrm))
  errors <- list(
    nonmonotone_information = expect_error(
      gsDesign(k = 3, timing = c(0.50, 1.20, 1.0)), "timing"
    ),
    rpact_missing_user_spending = expect_error(
      getDesignGroupSequential(kMax = 1, alpha = 0.025, beta = 0.2,
                               sided = 1, typeOfDesign = "asUser"),
      "userAlphaSpending"
    ),
    boin_invalid_target = expect_error(
      get.boundary(target = 1.1, ncohort = 10, cohortsize = 3), "target"
    ),
    crm_shape_mismatch = expect_error(
      print(crmsim(
        PI = c(0.05, 0.10, 0.20), prior = c(0.05, 0.10), target = 0.30,
        n = 3, x0 = 1, nsim = 2, count = FALSE, model = "logistic"
      ))
    )
  )
  errors
})

jsonlite::write_json(
  list(
    captured_utc = format(Sys.time(), tz = "UTC", usetz = TRUE),
    all_passed = all(vapply(results, function(x) identical(x$status, "PASS"), logical(1))),
    results = results
  ),
  out, auto_unbox = TRUE, pretty = TRUE, null = "null", digits = 10
)

if (!all(vapply(results, function(x) identical(x$status, "PASS"), logical(1)))) {
  quit(status = 1L)
}
