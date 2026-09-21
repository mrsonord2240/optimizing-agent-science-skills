# SYNTHETIC 600-sample cohort with planted structure. Writes data/synth_cohort.maf, data/synth_cohort_clin.tsv, data/synth_cohort_truth.rds
set.seed(7)
N <- 600
samples <- sprintf("PT%04d", sample(1:N))          # shuffled ids: file order != sorted order
sub <- sample(rep(c("Luminal","Basal","HER2"), c(300,180,120)))
stage <- sample(c("I","II","III","IV"), N, replace=TRUE, prob=c(.2,.4,.3,.1))
genes <- c("TP53","PIK3CA","CDH1","GATA3","MYC","ERBB2","BRAF","NRAS","KRAS","EGFR","PTEN","RB1","MAP3K1","ARID1A","NF1","CDKN2A")
G <- matrix(FALSE, N, length(genes), dimnames=list(samples, genes))
bern <- function(p) runif(N) < p
G[,"TP53"]   <- bern(ifelse(sub=="Basal", .75, .20))
G[,"MYC"]    <- ifelse(G[,"TP53"], bern(.55), bern(.05))            # planted CO-OCCURRENCE with TP53
G[,"PIK3CA"] <- bern(ifelse(sub=="Luminal", .40, .15))
G[,"CDH1"]   <- bern(ifelse(sub=="Luminal", .25, .03))
G[,"GATA3"]  <- bern(ifelse(sub=="Luminal", .20, .02))
G[,"ERBB2"]  <- bern(ifelse(sub=="HER2", .60, .03))
G[,"BRAF"]   <- bern(.15)
G[,"NRAS"]   <- ifelse(G[,"BRAF"], bern(.005), bern(.17))           # planted MUTUAL EXCLUSIVITY with BRAF
G[,"KRAS"]   <- bern(.08); G[,"EGFR"] <- ifelse(G[,"KRAS"], bern(.01), bern(.09))   # second mutex pair (small counts)
for (g in c("PTEN","RB1","MAP3K1","ARID1A","NF1","CDKN2A")) G[,g] <- bern(.06)
cls_pool <- c("Missense_Mutation","Nonsense_Mutation","Frame_Shift_Del","Splice_Site")
rows <- list(); truth <- data.frame(gene=character(), sample=character(), vc=character(), stringsAsFactors=FALSE)
for (g in genes) for (s in samples[G[,g]]) {
  k <- if (g=="TP53" && runif(1)<.15) 2 else 1                          # planted multi-hit: two variants in TP53 (different classes)
  vcs <- if (k==2) sample(cls_pool, 2) else sample(cls_pool, 1, prob=c(.65,.15,.12,.08))
  for (v in vcs) { rows[[length(rows)+1]] <- data.frame(Hugo_Symbol=g, Tumor_Sample_Barcode=s, Variant_Classification=v, stringsAsFactors=FALSE); truth[nrow(truth)+1,] <- list(g,s,v) }
}
mut <- do.call(rbind, rows)
# TMB: filler passenger variants in FILL genes; 3 hypermutators
target <- pmax(round(rexp(N, 1/25)) + 3, 3); hyper <- sample(N, 3); target[hyper] <- c(3000, 2500, 1800)
have <- table(factor(mut$Tumor_Sample_Barcode, levels=samples)); need <- pmax(target - as.integer(have), 0)
fill <- data.frame(Hugo_Symbol=sprintf("FILL%05d", sample(1:20000, sum(need), replace=TRUE)), Tumor_Sample_Barcode=rep(samples, need), Variant_Classification="Missense_Mutation", stringsAsFactors=FALSE)
all <- rbind(mut, fill)
all$Chromosome <- "1"; all$Start_Position <- seq_len(nrow(all)); all$End_Position <- all$Start_Position; all$Reference_Allele <- "A"; all$Tumor_Seq_Allele2 <- "T"; all$Variant_Type <- "SNP"
all <- all[, c("Hugo_Symbol","Chromosome","Start_Position","End_Position","Reference_Allele","Tumor_Seq_Allele2","Variant_Classification","Variant_Type","Tumor_Sample_Barcode")]
dir.create("data", showWarnings=FALSE)
write.table(all, "data/synth_cohort.maf", sep="\t", quote=FALSE, row.names=FALSE)
tmb <- as.integer(table(factor(all$Tumor_Sample_Barcode, levels=samples)))
clin <- data.frame(Tumor_Sample_Barcode=samples, subtype=sub, stage=stage, tmb=tmb, stringsAsFactors=FALSE)
write.table(clin, "data/synth_cohort_clin.tsv", sep="\t", quote=FALSE, row.names=FALSE)
saveRDS(list(G=G, truth=truth, clin=clin, hyper=samples[hyper]), "data/synth_cohort_truth.rds")
cat("MAF rows:", nrow(all), " hypermutator TMBs:", tmb[hyper], " median TMB:", median(tmb), "\n")
