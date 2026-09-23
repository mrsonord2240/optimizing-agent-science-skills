.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(demuxmix))
set.seed(2026092303); n <- 540; tags <- paste0('H',1:3); ids <- paste0('c',seq_len(n))
truth <- sample(c(rep('singlet',420),rep('doublet',60),rep('negative',60)))
counts <- matrix(rpois(3*n,6),nrow=3,dimnames=list(tags,ids)); sample_id <- sample(tags,n,TRUE)
for(i in seq_len(n)) { if(truth[i]=='singlet') counts[sample_id[i],i] <- counts[sample_id[i],i]+rpois(1,150); if(truth[i]=='doublet') counts[sample(tags,2),i] <- counts[sample(tags,2),i]+rpois(2,130) }
rna <- rpois(n,150)
dmm <- demuxmix(as.matrix(counts),rna=rna); calls <- dmmClassify(dmm)
glob <- ifelse(calls$HTO=='negative','negative',ifelse(grepl(',',calls$HTO),'doublet','singlet'))
cat('DEMUXMIX_COUNTS\n'); print(table(calls$HTO)); cat(sprintf('CLASS_ACCURACY=%.3f\n',mean(glob==truth)))
set.seed(90210); nu <- 600L; uclass <- sample(c('singlet','doublet','negative'),nu,TRUE,c(.55,.05,.40)); under <- matrix(0L,nrow=3,ncol=nu,dimnames=list(tags,paste0('u',seq_len(nu))))
for(i in seq_len(nu)) { under[,i] <- pmax(0L,6L+sample(-1:1,3,TRUE)); if(uclass[i]=='singlet') under[sample(tags,1),i] <- under[sample(tags,1),i]+rpois(1,140); if(uclass[i]=='doublet') under[sample(tags,2),i] <- under[sample(tags,2),i]+rpois(2,140) }
err <- tryCatch({demuxmix(under,rna=rpois(nu,150)); 'NO_ERROR'}, error=function(e) conditionMessage(e)); cat(sprintf('UNDERDISPERSED_RAW=%s\n',err))
fallback <- tryCatch({dmm2 <- tryCatch(demuxmix(under,rna=rpois(nu,150)),error=function(e) demuxmix(under,model='naive')); paste0('FALLBACK_OK_',nrow(dmmClassify(dmm2)))},error=function(e) paste0('FALLBACK_ERROR_',conditionMessage(e))); cat(sprintf('UNDERDISPERSED_FALLBACK=%s\n',fallback))
