# ArchR block from the fixed ecosystem-workflows.md: run up to and including the new stopifnot guard.
# (a) documented thresholds on the chr1 slice -> guard must stop; (b) relaxed thresholds -> guard passes.
suppressPackageStartupMessages(library(ArchR))
SKILL<-Sys.getenv("SKILL"); D<-Sys.getenv("ATACDATA"); SCA<-Sys.getenv("SCA")
md<-paste(readLines(file.path(SKILL,"references/ecosystem-workflows.md"),encoding="UTF-8"),collapse="\n")
blk<-regmatches(md,gregexpr("(?s)```r\n(.*?)```",md,perl=TRUE))[[1]]; blk<-blk[grepl("createArrowFiles",blk)][1]
blk<-sub("^```r\n","",blk); blk<-sub("```$","",blk)
stopifnot(grepl("stopifnot(length(ArrowFiles) > 0)",blk,fixed=TRUE))
g<-"stopifnot(length(ArrowFiles) > 0)"; pos<-regexpr(g,blk,fixed=TRUE); head_code<-substr(blk,1,pos+nchar(g)-1)   # everything through the guard
fr<-file.path(D,"scatac/outs/fragments.tsv.gz")
head_code<-sub("inputFiles=c('fragments_rep1.tsv.gz', 'fragments_rep2.tsv.gz')",sprintf("inputFiles='%s'",fr),head_code,fixed=TRUE)
head_code<-sub("sampleNames=c('rep1', 'rep2')","sampleNames='rep1'",head_code,fixed=TRUE)
head_code<-sub("addTileMat=TRUE, addGeneScoreMat=TRUE)","addTileMat=TRUE, addGeneScoreMat=TRUE, force=TRUE)",head_code,fixed=TRUE)
run<-function(code,tag){W<-file.path(SCA,"work",paste0("reaudit10x_archr_",tag)); unlink(W,recursive=TRUE); dir.create(W,recursive=TRUE); owd<-setwd(W); on.exit(setwd(owd))
  addArchRThreads(threads=6)
  tryCatch({eval(parse(text=code),envir=globalenv()); cat(tag,": guard PASSED, ArrowFiles =",ArrowFiles,"\n")},
           error=function(e) cat(tag,": STOPPED with:",conditionMessage(e),"\n"))}
cat("--- executed code (a) ---\n",head_code,"\n")
run(head_code,"documented")
run(sub("minTSS=4, minFrags=1000","minTSS=1, minFrags=500",head_code,fixed=TRUE),"relaxed")
