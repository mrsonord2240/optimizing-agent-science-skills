# Input 10 (NEW -- redundancy-pass regression check) -- bio-causal-genomics-mediation-analysis
# Prompt: "My labmate's script from last year calls
#   mediate(med_model, out_model, treat='genotype', mediator='expression',
#           boot=TRUE, sims=1000, boot.ci.type='BCa')
# I'm about to scale this up to sims=5000 for the paper. Anything wrong before I run it?"
#
# This checks a fact that, per fixes/bio-causal-genomics-mediation-analysis.md's redundancy-pass
# table, used to live ONLY in usage-guide.md's now-deleted 13-bullet Tips list ("BCa case-sensitivity
# ('bca' not 'BCa')") and was folded into SKILL.md's "Bootstrap iterations too low" Common Errors
# fix line during the 6e5f414 redundancy pass. If the redundancy pass silently dropped it instead of
# moving it, an agent following only SKILL.md (usage-guide.md no longer has it either) would not catch
# the labmate's bug. Also checks the unrelated sims=1000-vs-5000 threshold in the same section still
# holds (regression, not new).

library(mediation)

set.seed(2010)
n <- 400
genotype <- rbinom(n, 2, 0.3)
age <- rnorm(n, 55, 10); sex <- rbinom(n, 1, 0.5)
expression <- 0.4 * genotype + 0.01 * age - 0.05 * sex + rnorm(n, 0, 0.9)
disease <- rbinom(n, 1, plogis(-1.5 + 0.3 * expression + 0.1 * genotype))
dat <- data.frame(genotype, expression, disease, age, sex)

med_model <- lm(expression ~ genotype + age + sex, data = dat)
out_model <- glm(disease ~ genotype + expression + age + sex, data = dat, family = binomial)

cat("=== Input 10: BCa case-sensitivity (redundancy-pass check) ===\n\n")

cat("--- Attempt A: boot.ci.type='BCa' (labmate's script, wrong case) ---\n")
res_bad <- tryCatch({
  mediate(med_model, out_model, treat = "genotype", mediator = "expression",
          boot = TRUE, sims = 200, boot.ci.type = "BCa")
  "NO ERROR -- silently accepted or silently fell back"
}, error = function(e) paste("ERROR:", conditionMessage(e)),
   warning = function(w) paste("WARNING:", conditionMessage(w)))
print(res_bad)

cat("\n--- Attempt B: boot.ci.type='bca' (fixed SKILL.md's documented correct value) ---\n")
res_good <- tryCatch({
  m <- mediate(med_model, out_model, treat = "genotype", mediator = "expression",
               boot = TRUE, sims = 200, boot.ci.type = "bca")
  "OK -- ran without error"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
print(res_good)

cat("\n--- Grep check: is the 'bca'-not-'BCa' fact present verbatim in the fixed SKILL.md? ---\n")
skill_text <- paste(readLines("skill/SKILL.md"), collapse = "\n")
cat("Contains \"boot.ci.type='bca'\" note with case caveat: ",
    grepl("lowercase.*'bca'.*not.*'BCa'|boot.ci.type='bca'.*lowercase", skill_text, ignore.case = FALSE), "\n")
line <- grep("BCa", readLines("skill/SKILL.md"), value = TRUE)
cat("Matching line(s):\n"); print(line)
