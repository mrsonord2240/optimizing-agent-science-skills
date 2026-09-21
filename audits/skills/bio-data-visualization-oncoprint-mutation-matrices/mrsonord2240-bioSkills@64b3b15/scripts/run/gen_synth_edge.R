# SYNTHETIC data (planted ground truth) for the edge-case audit input. Writes data/synth_edge.maf, data/synth_edge_clin.tsv, data/synth_edge_truth.rds
set.seed(42)
samples <- sprintf("S%02d", 1:30)
# truth table: gene, sample, class (my alteration class), variant class (MAF) -- planted list is the ground truth
T <- data.frame(gene=character(), sample=character(), cls=character(), vc=character(), stringsAsFactors=FALSE)
add <- function(g, s, cls, vc) T[nrow(T)+1,] <<- list(g, s, cls, vc)
add("TP53","S01","Missense","Missense_Mutation"); add("TP53","S01","Truncating","Nonsense_Mutation")   # multi-class
add("MYC","S01","Amp","Amp"); add("KRAS","S01","Missense","Missense_Mutation")
add("TP53","S02","Missense","Missense_Mutation"); add("TP53","S02","Missense","Missense_Mutation")      # 2 hits same class
add("TP53","S03","Splice","Splice_Site"); add("PIK3CA","S03","Missense","Missense_Mutation")
add("RB1","S04","Truncating","Frame_Shift_Del"); add("MYC","S04","Amp","Amp"); add("MYC","S04","Missense","Missense_Mutation")
for (s in samples[5:24]) {
  if (runif(1)<0.25) add("KRAS", s, "Missense", "Missense_Mutation")
  if (runif(1)<0.30) add("TP53", s, sample(c("Missense","Truncating"),1), "Missense_Mutation")
  if (runif(1)<0.15) add("PIK3CA", s, "Missense", "Missense_Mutation")
  if (runif(1)<0.10) add("RB1", s, "Truncating", "Nonsense_Mutation")
}
# fix vc for truncating rows randomly assigned above
T$vc[T$cls=="Truncating" & T$vc=="Missense_Mutation"] <- "Nonsense_Mutation"
T$vc[T$cls=="Missense"] <- "Missense_Mutation"
snv <- T[T$cls!="Amp",]
maf <- data.frame(Hugo_Symbol=snv$gene, Chromosome="1", Start_Position=seq_len(nrow(snv))*100, End_Position=seq_len(nrow(snv))*100+1,
  Reference_Allele="A", Tumor_Seq_Allele2="T", Variant_Classification=snv$vc, Variant_Type="SNP", Tumor_Sample_Barcode=snv$sample, stringsAsFactors=FALSE)
# S25-S27 carry a mutation only in an unrelated gene; S28-S30 are absent from the MAF entirely
extra <- data.frame(Hugo_Symbol="OTHER1", Chromosome="2", Start_Position=c(9000,9100,9200), End_Position=c(9001,9101,9201), Reference_Allele="C", Tumor_Seq_Allele2="G",
  Variant_Classification="Missense_Mutation", Variant_Type="SNP", Tumor_Sample_Barcode=c("S25","S26","S27"), stringsAsFactors=FALSE)
maf <- rbind(maf, extra)
dir.create("data", showWarnings=FALSE)
write.table(maf, "data/synth_edge.maf", sep="\t", quote=FALSE, row.names=FALSE)
clin <- data.frame(Tumor_Sample_Barcode=samples, Subtype=rep(c("Luminal","Basal","HER2"), 10), Stage=rep(c("I","II","III","IV","II"), 6), stringsAsFactors=FALSE)
write.table(clin, "data/synth_edge_clin.tsv", sep="\t", quote=FALSE, row.names=FALSE)
saveRDS(list(T=T, samples=samples), "data/synth_edge_truth.rds")
cat("rows in MAF:", nrow(maf), " truth rows:", nrow(T), "\n")
