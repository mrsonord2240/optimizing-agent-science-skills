# Fresh Phase-2 R evidence: inputs 1, 2, 3, 5, 8, 10, and 11.
args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 3) stop("usage: phase2_r_regressions.R <skill> <data> <out>")
SK <- normalizePath(args[1], winslash="/", mustWork=TRUE)
DD <- normalizePath(args[2], winslash="/", mustWork=TRUE)
OUT <- normalizePath(args[3], winslash="/", mustWork=TRUE)
suppressPackageStartupMessages({library(limma); library(DEqMS); library(proDA); library(ashr); library(QFeatures); library(msqrob2); library(MsCoreUtils)})
source(file.path(SK,"scripts","limma_de.R"))
source(file.path(SK,"scripts","centring_checks.R"))
fdr <- function(ids, truth) { x <- truth$class[match(ids, truth$protein)]; c(calls=length(ids),fp=sum(x=="null",na.rm=TRUE),fdr=100*sum(x=="null",na.rm=TRUE)/max(1,length(ids))) }
show <- function(label, ids, truth) { z <- fdr(ids,truth); cat(sprintf("%s calls=%d fp=%d fdr=%.2f%%\n",label,z[1],z[2],z[3])); z }
read_lfq <- function() {
 pg <- read.table(file.path(DD,"proteinGroups.txt"),sep="\t",header=TRUE,quote="",comment.char="")
 si <- read.csv(file.path(DD,"sample_annotation.csv"),stringsAsFactors=FALSE)
 ic <- grep("^LFQ.intensity",names(pg),value=TRUE); M <- as.matrix(pg[,ic]); rownames(M) <- pg$Majority.protein.IDs
 colnames(M) <- sub("^LFQ\\.intensity\\.","",ic); M[M==0] <- NA; M <- log2(M); med <- apply(M,2,median,na.rm=TRUE); M <- sweep(M,2,med)+median(med)
 si <- si[match(colnames(M),si[[1]]),]; list(pg=pg,M=M,si=data.frame(sample=colnames(M),condition=si$condition,batch=factor(si$batch)),truth=read.csv(file.path(DD,"truth_proteins.csv")))
}
cat("=== INPUT 1 limma 4v4, shipped limma_de.R ===\n")
d <- read_lfq(); o <- run_limma_de(d$M,d$si,"Treatment-Control")
a <- show("limma",rownames(o$results)[o$results$adj.P.Val<.05],d$truth)
cat(sprintf("tested=%d dropped_valid=%d dropped_nonestimable=%d\n",nrow(o$results),length(o$dropped_valid),length(o$dropped_nonestimable)))
stopifnot(nrow(o$results)>1000,a["fdr"]<=5,length(o$dropped_valid)>0)
cat("=== INPUT 2 treat and DEqMS inline workflows ===\n")
ft <- treat(o$fit2,lfc=log2(1.2),trend=TRUE,robust=TRUE); tr <- topTreat(ft,coef=1,number=Inf); b <- show("treat",rownames(tr)[tr$adj.P.Val<.05],d$truth)
o$fit2$count <- pmax(d$pg$Peptides[match(rownames(o$fit2$coefficients),d$pg$Majority.protein.IDs)],1); f3 <- spectraCounteBayes(o$fit2); dr <- outputResult(f3,coef_col=1)
ids <- dr$gene[dr$sca.adj.pval<.05]; if (is.null(ids)) ids <- rownames(dr)[dr$sca.adj.pval<.05]; c2 <- show("DEqMS",ids,d$truth)
stopifnot(b["fdr"]<=5,c2["fdr"]<=5,all(c("sca.t","sca.adj.pval") %in% names(dr)))
cat("=== INPUT 3 proDA MNAR/on-off ===\n")
fp <- proDA(d$M,design=~condition+batch,col_data=d$si,reference_level="Control"); pr <- test_diff(fp,"conditionTreatment"); sig <- pr[!is.na(pr$adj_pval)&pr$adj_pval<.05,]
onoff <- rownames(d$M)[apply(sapply(unique(d$si$condition),function(g)rowSums(!is.na(d$M[,d$si$condition==g,drop=FALSE]))),1,min)==0]
cat(sprintf("proDA tested=%d calls=%d onoff=%d called_onoff=%d\n",nrow(pr),nrow(sig),length(onoff),sum(onoff %in% sig$name))); stopifnot(length(onoff)>0,all(c("adj_pval","diff") %in% names(pr)))
cat("=== INPUT 5 ashr fold-change shrinkage ===\n")
se <- sqrt(o$fit2$s2.post)*o$fit2$stdev.unscaled[,1]; sh <- ash(o$fit2$coefficients[,1],se,mixcompdist="normal")$result$PosteriorMean
cat(sprintf("ashr n=%d finite=%d exact_zero=%d\n",length(sh),sum(is.finite(sh)),sum(sh==0))); stopifnot(all(is.finite(sh)))
cat("=== INPUT 8 paired donor estimability ===\n")
pm <- as.matrix(read.csv(file.path(DD,"paired_donor_log2.csv"),row.names=1,check.names=FALSE)); ps <- read.csv(file.path(DD,"paired_donor_samples.csv")); ps <- ps[match(colnames(pm),ps[[1]]),]; pt <- read.csv(file.path(DD,"paired_donor_truth.csv"))
po <- run_limma_de(pm,data.frame(sample=colnames(pm),condition=ps$condition,batch=factor(ps$donor)),"LPS-Unstim"); z8 <- show("paired_limma",rownames(po$results)[po$results$adj.P.Val<.05],pt)
cat(sprintf("paired tested=%d nonestimable=%d\n",nrow(po$results),length(po$dropped_nonestimable))); stopifnot(length(po$dropped_nonestimable)>0,z8["fdr"]<=5)
cat("=== INPUT 10 centring checks, both symptoms ===\n")
ann <- read.csv(file.path(DD,"annotation_msstats.csv")); ev <- read.table(file.path(DD,"evidence.txt"),sep="\t",header=TRUE,quote="",comment.char="")
ev <- ev[!(ev$Reverse %in% "+")&!(ev$Potential.contaminant %in% "+")&!is.na(ev$Intensity)&ev$Intensity>0,]; ev$feature <- paste(ev$Modified.sequence,ev$Charge,sep="_"); runs <- as.character(ann$Raw.file)
ag <- aggregate(Intensity~feature+Raw.file+Leading.razor.protein,data=ev,FUN=sum); wide <- reshape(ag,idvar=c("feature","Leading.razor.protein"),timevar="Raw.file",direction="wide"); names(wide) <- sub("Intensity.","",names(wide),fixed=TRUE); wide <- wide[,c("feature","Leading.razor.protein",runs)]; names(wide)[2] <- "protein"
write.csv(wide,file.path(OUT,"peptide_wide.csv"),row.names=FALSE); write.csv(data.frame(run=runs,condition=ann$Condition),file.path(OUT,"peptide_samples.csv"),row.names=FALSE)
cd <- data.frame(quantCols=runs,condition=factor(ann$Condition,levels=c("Control","Treatment")),sample=factor(runs),row.names=runs); pe <- readQFeatures(assayData=wide,quantCols=runs,colData=cd,name="raw",verbose=FALSE); pe <- zeroIsNA(pe,"raw"); pe <- logTransform(pe,base=2,i="raw",name="log"); rowData(pe[["log"]])$nNonZero <- rowSums(!is.na(assay(pe[["log"]]))); pe <- filterFeatures(pe,~nNonZero>=2,keep=TRUE); before <- assay(pe[["log"]]); pe <- normalize(pe,i="log",name="norm",method="center.median"); ratio <- check_sd_ratio(before,assay(pe[["norm"]]),colData(pe)$condition); cat(sprintf("residual_sd_ratio=%.3f threshold=%.2f\n",ratio,SD_RATIO_MIN)); stopped <- tryCatch({check_offset(c(-.22,-.20,-.18));FALSE},error=function(e){cat(conditionMessage(e),"\n");TRUE}); stopifnot(ratio<SD_RATIO_MIN,check_offset(c(-.01,0,.01))==0,stopped)
cat("=== INPUT 11 three-arm ridge guidance ===\n")
ta <- as.matrix(read.csv(file.path(DD,"three_arm_log2.csv"),row.names=1,check.names=FALSE)); ts <- read.csv(file.path(DD,"three_arm_samples.csv")); ts <- ts[match(colnames(ta),ts[[1]]),]; rr <- colnames(ta); pw <- data.frame(feature=rownames(ta),protein=rownames(ta),2^ta,check.names=FALSE); cd3 <- data.frame(quantCols=rr,condition=factor(ts[[2]]),sample=factor(rr),row.names=rr); p3 <- readQFeatures(assayData=pw,quantCols=rr,colData=cd3,name="raw",verbose=FALSE); p3 <- zeroIsNA(p3,"raw"); p3 <- logTransform(p3,base=2,i="raw",name="log"); p3 <- suppressWarnings(aggregateFeatures(p3,i="log",fcol="protein",name="protein",fun=MsCoreUtils::robustSummary,na.rm=TRUE)); ok <- tryCatch({msqrob(p3,i="protein",formula=~condition,robust=TRUE,ridge=TRUE);TRUE},error=function(e){cat(conditionMessage(e),"\n");FALSE}); cat(sprintf("three_arm_ridge_accepted=%s groups=%d\n",ok,nlevels(cd3$condition))); stopifnot(ok)
cat("ALL_R_ASSERTIONS_PASS\n")
