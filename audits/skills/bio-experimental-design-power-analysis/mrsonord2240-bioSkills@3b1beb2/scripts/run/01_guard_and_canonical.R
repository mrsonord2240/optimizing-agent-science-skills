source_path <- "F:/OpenScience/wt/experimental-design-power-analysis/experimental-design/power-analysis/examples/rnaseq_power.R"
lines <- readLines(source_path,warn=FALSE); marker <- grep("^# ---------------------------------------------------------------------------$",lines)[1]; eval(parse(text=lines[1:(marker-1)]))
must_fail <- function(expr){inherits(try(force(expr),silent=TRUE),"try-error")}
stopifnot(is.finite(checked_rnapower(depth=2,n=14,cv=.3,effect=1.5,alpha=.05)), must_fail(checked_rnapower(depth=2,n=14,cv=.3,effect=1.5,alpha=1.5)), must_fail(checked_rnapower(depth=2,n=14,cv=-.3,effect=1.5,alpha=.05)), must_fail(checked_rnapower(depth=2,n=14,cv=.3,effect=1,alpha=.05)))
gate <- assess_realized_fdr(cbind(SS1=c(3,5,8),`Actual FDR`=c(.04,.06,NaN),`Marginal power`=c(.4,.5,.6)),.05,0)
stopifnot(identical(gate$decision,c("ACCEPT","REJECT","REJECT")))
cat(sprintf("valid_canonical_power=%.6f\n",checked_rnapower(depth=2,n=14,cv=.3,effect=1.5,alpha=.05))); print(gate); cat("GUARD_AND_CANONICAL=PASS\n")
