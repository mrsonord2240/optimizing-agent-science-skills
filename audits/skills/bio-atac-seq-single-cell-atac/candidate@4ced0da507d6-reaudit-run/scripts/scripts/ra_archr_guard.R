# Re-audit: ArchR block from live ecosystem-workflows.md through the stopifnot guard; documented thresholds must stop, relaxed must pass.
suppressPackageStartupMessages(library(ArchR))
SKILL<-Sys.getenv("SKILL"); D<-Sys.getenv("ATACDATA"); SCA<-Sys.getenv("SCA")
md<-paste(readLines(file.path(SKILL,"references/ecosystem-workflows.md"),encoding="UTF-8"),collapse="\n")
blk<-regmatches(md,gregexpr("(?s)```r\n(.*?)```",md,perl=TRUE))[[1]]; blk<-blk[grepl("createArrowFiles",blk)][1]
blk<-sub("^```r\n","",blk); blk<-sub("```$","",blk)
g<-"stopifnot(length(ArrowFiles) > 0)"; stopifnot(grepl(g,blk,fixed=TRUE))
pos<-regexpr(g,blk,fixed=TRUE); head_code<-substr(blk,1,pos+nchar(g)-1)
fr<-file.path(D,"scatac/outs/fragments.tsv.gz")
head_code<-sub("inputFiles=c('fragments_rep1.tsv.gz', 'fragments_rep2.tsv.gz')",sprintf("inputFiles='%s'",fr),head_code,fixed=TRUE)
head_code<-sub("sampleNames=c('rep1', 'rep2')","sampleNames='rep1'",head_code,fixed=TRUE)
run<-function(code,tag){W<-file.path(SCA,"work",paste0("ra_archr_",tag)); unlink(W,recursive=TRUE); dir.create(W,recursive=TRUE); owd<-setwd(W); on.exit(setwd(owd))
  addArchRThreads(threads=6)
  tryCatch({eval(parse(text=code),envir=globalenv()); cat(tag,": guard PASSED, ArrowFiles =",ArrowFiles,"\n")
            print(file.info(ArrowFiles)$size)
            cat("cells in arrow:", length(h5read(ArrowFiles[1],"Metadata/CellNames")), "\n")},
           error=function(e) cat(tag,": STOPPED with:",conditionMessage(e),"\n"))}
run(head_code,"documented")
run(sub("minTSS=4, minFrags=1000","minTSS=1, minFrags=500",head_code,fixed=TRUE),"relaxed")
