# Assertions against planted truth, from saved RDS of each side.
D <- "F:/OpenScience/comparisons/pleiotropy-same-id/run/"
truth_out <- as.integer(sub("rs","",readLines(paste0(D,"data/C_true_outliers.txt"))))
cat("planted outliers (C):", truth_out, "\n")
for (s in c("theirs","ours")) {
  cat("\n#####", s, "\n")
  for (ds in c("A_balanced","B_directional","C_outliers","D_chp")) {
    x <- readRDS(paste0(D,"out/",s,"_",ds,".rds")); r <- x$res
    if (s=="theirs") { b <- r$battery; e <- r$egger_block; p <- r$presso_block
      cat(sprintf("%-14s IVW %.3f Egger %.3f (int %.4f p=%.3f) WM %.3f WMode %.3f Qp %.2g | PRESSO global %s raw %.3f corr %s | errs: %s\n", ds, b$ivw,b$egger,b$egger_int,b$egger_int_p,b$median,b$mode,b$q_p, as.character(b$presso_global), p$raw, format(p$corrected), paste(names(x$err),collapse=",")))
      if (ds=="C_outliers") { ot <- p$presso$`MR-PRESSO results`$`Outlier Test`; pv <- suppressWarnings(as.numeric(sub("<","",ot$Pvalue)))
        cat("   verbatim `which(Pvalue<0.05)` ->", p$outlier_idx, "\n   numeric parse (<x -> x, p<0.05) ->", which(pv<0.05), "\n")
        cat("   numeric hits in planted:", length(intersect(which(pv<0.05), truth_out)), "of", length(truth_out), " false hits:", length(setdiff(which(pv<0.05), truth_out)), "\n") }
    } else {
      cat(sprintf("%-14s IVW %.3f Egger %.3f (int %.4f p=%.3f) WM %.3f WMode %.3f Qp %.2g | PRESSO global %s raw %.3f corr %s n_out(verbatim) %s | errs: %s\n", ds, r$ivw,r$egger,r$egger_int,r$egger_int_p,r$median,r$mode,r$q_p, as.character(r$global_p), r$raw, format(r$corrected), r$n_outliers, paste(names(x$err),collapse=",")))
      if (ds=="C_outliers") cat("   verbatim which(outlier_p<0.05) ->", r$outlier_idx, "\n")
    }
  }
}
