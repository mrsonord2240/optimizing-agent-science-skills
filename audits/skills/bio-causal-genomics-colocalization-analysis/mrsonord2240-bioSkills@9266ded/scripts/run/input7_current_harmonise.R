# Regression of the prior audit's six-SNP table against the current implementation.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: input7_current_harmonise.R <harmonise.R>")
source(args[[1]])

df1 <- data.frame(SNP=c("rs1","rs2","rs3","rs4","rs5","rs6"), A1=c("A","A","A","A","C","T"), A2=c("G","G","G","G","G","A"), BETA=c(0.5,-0.3,0.2,0.4,0.1,0.15), MAF=c(0.30,0.20,0.25,0.35,0.45,0.10))
df2 <- data.frame(SNP=c("rs1","rs2","rs3","rs4","rs5","rs6"), A1=c("A","G","C","T","C","A"), A2=c("G","A","T","C","G","T"), BETA=c(0.55,-0.28,0.10,0.42,0.11,0.16), MAF=c(0.31,0.79,0.40,0.66,0.44,0.09))
out <- harmonise(df1, df2)
print(out[, c("SNP", "A1.1", "A2.1", "A1.2", "A2.2", "BETA.2", "MAF.2")])
checks <- c(kept=setequal(out$SNP, c("rs1","rs2","rs3","rs4","rs6")), rs2_flip=isTRUE(all.equal(out$BETA.2[out$SNP == "rs2"], 0.28)), rs3_complement_flip=isTRUE(all.equal(out$BETA.2[out$SNP == "rs3"], -0.10)), rs4_complement_same=isTRUE(all.equal(out$BETA.2[out$SNP == "rs4"], 0.42)), rs5_high_maf_palindromic_dropped=!("rs5" %in% out$SNP), rs6_low_maf_palindromic_flip=isTRUE(all.equal(out$BETA.2[out$SNP == "rs6"], -0.16)))
for (nm in names(checks)) cat(sprintf("ASSERT %s=%s\n", nm, checks[[nm]]))
stopifnot(all(checks))
