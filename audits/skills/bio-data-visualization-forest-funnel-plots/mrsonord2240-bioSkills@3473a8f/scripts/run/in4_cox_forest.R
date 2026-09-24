# Input 4: SKILL.md ggforest block on REAL data (survival::lung, NCCTG lung cancer, 228 pts). "treatment"=sex stand-in, age, ph.ecog stand-in for stage.
suppressMessages({library(survival); library(survminer)})
D <- "F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots"
df <- na.omit(lung[, c("time","status","sex","age","ph.ecog")])
df$treatment <- factor(df$sex, levels = c(1,2), labels = c("Male","Female"))
df$stage <- factor(df$ph.ecog, levels = 0:3, labels = c("ECOG0","ECOG1","ECOG2","ECOG3"))
df$sexf <- df$treatment
cat("n =", nrow(df), "events =", sum(df$status == 2), "\n")
# ---- SKILL.md block (sex column replaced by 'sexf' so treatment/sex are not identical) ----
fit <- coxph(Surv(time, status) ~ treatment + age + stage, data = df)
print(summary(fit)$conf.int)
png(file.path(D, "figs/in4_ggforest.png"), width = 1000, height = 600, res = 110)
p <- ggforest(fit, data = df, main = 'Subgroup HRs', cpositions = c(0.02, 0.22, 0.4),
              fontsize = 0.7, refLabel = 'Reference', noDigits = 2)
print(p)
dev.off()
# ground truth from the model
ci <- exp(cbind(coef(fit), confint(fit))); colnames(ci) <- c("HR","lo","hi"); print(round(ci, 3))
# extract what ggforest actually plotted (its plot data has the label text)
ld <- p$layers[[1]]$data; print(class(ld))
cat("(plotted values checked via image)
")
# Skill claim: 'Single-trial subgroup HRs -> ggforest' & 'Cox subgroup forest ... with interaction p-values'
# what a real subgroup forest needs: treatment HR within each subgroup + interaction test
fit_int <- coxph(Surv(time, status) ~ treatment * stage + age, data = df)
lrt <- anova(fit_int, coxph(Surv(time, status) ~ treatment + stage + age, data = df))
cat("interaction LRT p (treatment x stage):", lrt$`Pr(>|Chi|)`[2], "\n")
sub <- sapply(c("ECOG0","ECOG1","ECOG2"), function(s) { f <- coxph(Surv(time,status) ~ treatment + age, data = df[df$stage==s,]); c(HR=exp(coef(f)[1]), lo=exp(confint(f)[1,1]), hi=exp(confint(f)[1,2]), n=f$n) })
print(round(t(sub), 3))
cat("ggforest has an interaction argument? ", "interaction" %in% names(formals(ggforest)), "\n"); print(names(formals(ggforest)))
# numeric-sex trap: coded 1/2 as in lung
fit2 <- coxph(Surv(time, status) ~ sex + age + ph.ecog, data = df)
png(file.path(D, "figs/in4_ggforest_numeric.png"), width = 1000, height = 450, res = 110); print(ggforest(fit2, data = df)); dev.off()
# example step 8 as shipped (clinical_df undefined)
r <- try(coxph(Surv(time, status) ~ treatment + age + sex + stage, data = clinical_df), silent = TRUE); cat("example step 8 as shipped:", conditionMessage(attr(r, "condition")), "\n")
