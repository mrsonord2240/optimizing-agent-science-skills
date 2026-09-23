# Input 9 (NEW -- not in the pre-fix 7) -- Directly tests the fix log's "found while
# fixing" defect: SKILL.md's MR-RAPS section previously implied over.dispersion= and
# loss.function= are top-level arguments to TwoSampleMR::mr_raps(). The fix added a code
# block showing the real nested form (parameters = list(...)) and a note that the bare
# top-level form throws "unused arguments". This input verifies BOTH halves of that claim
# against the actually-installed TwoSampleMR 0.7.9: (a) the bare form fails, (b) the
# nested form in the current SKILL.md succeeds. Not exercised as a scored input pre-fix
# (pre-fix Input 4 already used the nested form without ever showing what the bare form
# does).

library(TwoSampleMR)

dat <- readRDS('F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_weak.rds')

cat('=== mr_raps() real signature ===\n')
print(args(TwoSampleMR::mr_raps))

cat('\n=== (a) BARE top-level arguments (the OLD, pre-fix-implied calling form) ===\n')
bare_result <- tryCatch({
  TwoSampleMR::mr_raps(b_exp = dat$beta.exposure, b_out = dat$beta.outcome,
                        se_exp = dat$se.exposure, se_out = dat$se.outcome,
                        over.dispersion = TRUE, loss.function = 'huber')
  'SUCCEEDED (unexpected)'
}, error = function(e) {
  cat('ERROR:', conditionMessage(e), '\n')
  'ERRORED'
})
cat('Bare top-level form:', bare_result, '\n')

cat('\n=== (b) NESTED parameters=list(...) form (the CURRENT SKILL.md code block) ===\n')
nested_result <- tryCatch({
  r <- TwoSampleMR::mr_raps(b_exp = dat$beta.exposure, b_out = dat$beta.outcome,
                             se_exp = dat$se.exposure, se_out = dat$se.outcome,
                             parameters = list(over.dispersion = TRUE, loss.function = 'huber', shrinkage = FALSE))
  cat('b:', round(r$b, 4), ' se:', round(r$se, 4), ' p:', format.pval(r$pval), '\n')
  'SUCCEEDED'
}, error = function(e) {
  cat('ERROR:', conditionMessage(e), '\n')
  'ERRORED'
})
cat('Nested parameters= form:', nested_result, '\n')

cat('\n=== Regression verdict ===\n')
if (bare_result == 'ERRORED' && nested_result == 'SUCCEEDED') {
  cat('CONFIRMED: bare top-level over.dispersion=/loss.function= throws an error (unused arguments),\n')
  cat('  and the current SKILL.md nested parameters=list(...) form is the one that actually works.\n')
  cat('  The added code block and warning note are accurate.\n')
} else {
  cat('UNEXPECTED result pattern -- flag for re-review: bare=', bare_result, ' nested=', nested_result, '\n')
}
