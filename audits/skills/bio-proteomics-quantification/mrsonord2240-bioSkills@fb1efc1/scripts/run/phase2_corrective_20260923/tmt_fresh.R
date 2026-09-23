# Fresh Input 4 and Input 8 private-R regression.
suppressPackageStartupMessages(library(MSnbase))
d <- "/mnt/openscience/audits/bio-proteomics-quantification/data"
o <- "/mnt/openscience/audits/bio-proteomics-quantification/run/phase2_corrective_20260923"
raw <- readMSData(file.path(d,"tmt10_synthetic.mzML"),mode="onDisk")
q <- quantify(raw,reporters=TMT10,method="max")
q <- purityCorrect(q,makeImpuritiesMatrix(x=10,edit=FALSE))
m <- exprs(q)
stopifnot(identical(dim(m),c(24L,10L)),sum(m<0,na.rm=TRUE)==0,sum(is.na(m))==0)
saveRDS(m,file.path(o,"tmt10_corrected.rds"))
cat("INPUT4 matrix=",paste(dim(m),collapse="x")," negatives=",sum(m<0)," nas=",sum(is.na(m)),"\n",sep="")
stopifnot(exists("TMT16"),!exists("TMT18"))
for(x in c(4,6,8,10)) stopifnot(all(dim(makeImpuritiesMatrix(x=x,edit=FALSE))==c(x,x)))
for(x in c(11,16)) stopifnot(inherits(try(makeImpuritiesMatrix(x=x,edit=FALSE),silent=TRUE),"try-error"))
offs <- c(seq(-8,-1),seq(1,8))
coa <- data.frame(Tag=reporterNames(TMT16))
for(z in offs) coa[[as.character(z)]] <- 0
coa[["-1"]] <- c(0,rep(.8,15)); coa[["1"]] <- c(rep(5,15),0)
f <- file.path(o,"tmtpro16_coa.csv"); write.csv(coa,f,row.names=FALSE,quote=FALSE)
imp <- makeImpuritiesMatrix(filename=f,edit=FALSE)
set.seed(23); x <- matrix(runif(1600,1e5,1e6),ncol=16,dimnames=list(paste0("P",1:100),rownames(imp)))
pc <- purityCorrect(new("MSnSet",exprs=x),imp)
stopifnot(identical(dim(exprs(pc)),c(100L,16L)),sum(is.na(exprs(pc)))==0,sum(exprs(pc)<0)==0)
cat("INPUT8 TMT16=",length(TMT16)," coa=",paste(dim(imp),collapse="x")," corrected=",paste(dim(exprs(pc)),collapse="x"),"\n",sep="")
