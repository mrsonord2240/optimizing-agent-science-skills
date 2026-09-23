# Fresh Phase-2 TMT10 reporter run and TMTpro-CoA regression. Source block is from fb1efc10.
suppressPackageStartupMessages(library(MSnbase))
data_dir <- 'F:/OpenScience/audits/bio-proteomics-quantification/data'
cat('INPUT 4: TMT10 reporter extraction\n')
raw <- readMSData(file.path(data_dir, 'tmt10_synthetic.mzML'), mode = 'onDisk')
quant <- quantify(raw, reporters = TMT10, method = 'max')
imp <- makeImpuritiesMatrix(x = 10, edit = FALSE)
quant <- purityCorrect(quant, imp)
m <- exprs(quant)
stopifnot(identical(dim(m), c(24L, 10L)), sum(m < 0, na.rm = TRUE) == 0, sum(is.na(m)) == 0)
saveRDS(m, 'tmt10_corrected.rds')
cat('matrix=', paste(dim(m), collapse='x'), ' negatives=', sum(m < 0, na.rm = TRUE), ' nas=', sum(is.na(m)), '\n', sep='')

cat('INPUT 8: TMTpro template/CoA route\n')
stopifnot(exists('TMT16'), !exists('TMT18'))
for (x in c(4,6,8,10)) stopifnot(all(dim(makeImpuritiesMatrix(x=x, edit=FALSE)) == c(x,x)))
for (x in c(11,16)) { bad <- try(makeImpuritiesMatrix(x=x, edit=FALSE), silent=TRUE); stopifnot(inherits(bad, 'try-error')) }
n <- 16; offs <- c(seq(-8,-1), seq(1,8)); coa <- data.frame(Tag=reporterNames(TMT16))
for (o in offs) coa[[as.character(o)]] <- 0
coa[['-1']] <- c(0, rep(0.8, 15)); coa[['1']] <- c(rep(5.0, 15), 0)
write.csv(coa, 'tmtpro16_coa.csv', row.names=FALSE, quote=FALSE)
imp16 <- makeImpuritiesMatrix(filename='tmtpro16_coa.csv', edit=FALSE)
set.seed(23); x <- matrix(runif(1600, 1e5, 1e6), ncol=16, dimnames=list(paste0('P', 1:100), rownames(imp16)))
pc <- purityCorrect(new('MSnSet', exprs=x), imp16)
stopifnot(identical(dim(exprs(pc)), c(100L,16L)), sum(is.na(exprs(pc))) == 0, sum(exprs(pc) < 0) == 0)
cat('TMT16=', length(TMT16), ' TMT18=FALSE coa=', paste(dim(imp16), collapse='x'), ' corrected=', paste(dim(exprs(pc)), collapse='x'), '\n', sep='')
