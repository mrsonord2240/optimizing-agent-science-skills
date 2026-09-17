# Input 12 (NEW -- redundancy-pass regression check) -- bio-causal-genomics-mediation-analysis
# Prompt: "I don't have the EValue package available on this cluster node. Given ACME expressed as
# a risk ratio of 1.8 (95% CI lower bound 1.2), compute the mediational E-value by hand using the
# formula in the Skill, then tell me what E-value package call would double-check it if I had network
# access."
#
# Per the fix log's redundancy-pass table, the formula E = RR + sqrt(RR*(RR-1)) "moved" into
# SKILL.md's '## Mediational E-Value for Sensitivity' section during the 6e5f414 pass -- SKILL.md
# previously named the method (Smith & VanderWeele 2019) but never gave the actual formula; the
# formula itself used to live only in usage-guide.md. Checks whether the hand-computed value from the
# fixed SKILL.md's formula matches the EValue package's own evalues.RR(), which IS installed in this
# audit env (TOOLS.md), used here only as an independent check, not as what the labmate would call.

library(EValue)

rr_point <- 1.8
rr_lower <- 1.2

# Hand formula per fixed SKILL.md: E = RR + sqrt(RR * (RR - 1))
e_by_hand <- function(rr) rr + sqrt(rr * (rr - 1))

e_point_hand <- e_by_hand(rr_point)
e_lower_hand <- e_by_hand(rr_lower)

cat("=== Input 12: Mediational E-value hand formula vs EValue package (redundancy-pass check) ===\n\n")
cat("Hand-computed via SKILL.md formula E = RR + sqrt(RR*(RR-1)):\n")
cat("  E(point, RR=1.8)      =", round(e_point_hand, 4), "\n")
cat("  E(CI lower, RR=1.2)   =", round(e_lower_hand, 4), "\n\n")

cat("Package check -- evalues.RR(est=1.8, lo=1.2) [default hi=NA]:\n")
pkg <- evalues.RR(est = rr_point, lo = rr_lower)
print(pkg)

e_point_pkg <- pkg["E-values", "point"]
e_lower_pkg <- pkg["E-values", "lower"]

cat("\n--- Also trying SKILL.md's LITERAL documented call, hi=NULL ---\n")
cat("SKILL.md's own 'Mediational E-Value for Sensitivity' code block ends with:\n")
cat("  evalues.RR(acme_rr, lo=acme_lower_rr, hi=NULL)\n")
pkg_hiNULL <- tryCatch(
  evalues.RR(est = rr_point, lo = rr_lower, hi = NULL),
  error = function(e) paste("ERROR:", conditionMessage(e))
)
print(pkg_hiNULL)
cat("(NEW FINDING, not a redundancy-pass regression: SKILL.md's own documented `hi=NULL`\n",
    " call crashes on installed EValue -- args(evalues.RR) shows hi defaults to NA, not NULL;\n",
    " passing NULL trips `!is.na(hi)` on a length-zero argument. Omitting hi, or passing hi=NA,\n",
    " works. Filed as a new P2 below -- a real, reproducible R error, not a silent wrong answer,\n",
    " in a secondary sensitivity-analysis code block, not the Skill's central operation.)\n")

cat("\nAgreement (hand vs package), point:", round(e_point_hand, 4), "vs", round(e_point_pkg, 4),
    " diff =", round(abs(e_point_hand - e_point_pkg), 6), "\n")
cat("Agreement (hand vs package), CI bound:", round(e_lower_hand, 4), "vs", round(e_lower_pkg, 4),
    " diff =", round(abs(e_lower_hand - e_lower_pkg), 6), "\n")

cat("\n--- Grep check: is the formula text present verbatim in the fixed SKILL.md? ---\n")
line <- grep("RR \\+ sqrt\\(RR \\* \\(RR - 1\\)\\)|E = RR", readLines("skill/SKILL.md"), value = TRUE)
cat("Matching line(s):\n"); print(line)
