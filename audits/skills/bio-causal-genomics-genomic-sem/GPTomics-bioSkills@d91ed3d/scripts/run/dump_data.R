# Persist the synthetic inputs used across the audit as flat files under ../data/
# for reproducibility (all SYNTHETIC, planted ground truth documented in the input*.R
# scripts that generate them inline).
source("synth_lib.R")

traits1 <- c("MDD","ANX","PTSD","NEUR")
S1 <- name_S(build_one_factor_S(c(0.75,0.65,0.70,0.55), c(0.10,0.06,0.05,0.12)), traits1)
write.csv(S1, "../data/input1_S_planted_one_factor.csv")

traits3 <- c("BMI","WHRadjBMI","T2D","HDL")
h2 <- c(0.20,0.15,0.08,0.12)
rg <- matrix(c(1,0.97,0.35,-0.30, 0.97,1,0.30,-0.25, 0.35,0.30,1,-0.20, -0.30,-0.25,-0.20,1),4,4)
S3 <- diag(sqrt(h2)) %*% rg %*% diag(sqrt(h2)); dimnames(S3) <- list(traits3, traits3)
write.csv(S3, "../data/input3_S_heywood_near_collinear.csv")

set.seed(42)
n_factor<-5; n_het<-5; n_null<-10; n<-n_factor+n_het+n_null
maf <- runif(n, 0.05, 0.45)
beta <- matrix(0,n,3)
for (i in 1:n_factor) beta[i,] <- 0.05*c(0.75,0.65,0.70)
for (i in (n_factor+1):(n_factor+n_het)) beta[i,] <- c(0.15,0,0)
for (i in (n_factor+n_het+1):n) beta[i,] <- rnorm(3,0,0.002)
SNPs2 <- data.frame(SNP=paste0("rs",1:n), A1="A", A2="G", MAF=maf,
                     beta.MDD=beta[,1], se.MDD=0.01, beta.ANX=beta[,2], se.ANX=0.01,
                     beta.PTSD=beta[,3], se.PTSD=0.01,
                     planted_class=c(rep("factor",n_factor), rep("heterogeneous",n_het), rep("null",n_null)))
write.csv(SNPs2, "../data/input2_SNPs_planted_classes.csv", row.names = FALSE)

cat("Wrote 3 synthetic data files to ../data/\n")
