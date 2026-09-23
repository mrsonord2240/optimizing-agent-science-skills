library(GSVA)
set.seed(456)
ng <- 300; ns <- 16
expr <- matrix(rnorm(ng*ns), nrow=ng, dimnames=list(sprintf("G%03d", seq_len(ng)), sprintf("S%02d",seq_len(ns))))
sets <- list(UP=sprintf("G%03d",1:30), DOWN=sprintf("G%03d",31:60), NULL=sprintf("G%03d",61:100))
expr[sets$UP, 9:16] <- expr[sets$UP,9:16] + 1
expr[sets$DOWN, 9:16] <- expr[sets$DOWN,9:16] - 1
gs <- gsva(gsvaParam(expr, sets, kcdf="Gaussian", minSize=10, maxSize=100))
ss <- gsva(ssgseaParam(expr, sets, minSize=10, maxSize=100))
stopifnot(identical(dim(gs), c(3L,16L)), identical(dim(ss), c(3L,16L)), all(is.finite(gs)), all(is.finite(ss)))
stopifnot(mean(gs["UP",9:16])-mean(gs["UP",1:8]) > 0.3, mean(gs["DOWN",9:16])-mean(gs["DOWN",1:8]) < -0.3)
write.csv(gs, "F:/OpenScience/audits/bio-pathway-gsea/data/input4_gsva_scores.csv")
write.csv(ss, "F:/OpenScience/audits/bio-pathway-gsea/data/input4_ssgsea_scores.csv")
cat(sprintf("ASSERT input4 GSVA_up_delta=%.4f GSVA_down_delta=%.4f\n", mean(gs["UP",9:16])-mean(gs["UP",1:8]), mean(gs["DOWN",9:16])-mean(gs["DOWN",1:8])))
