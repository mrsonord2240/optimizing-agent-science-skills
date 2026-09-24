# Input 3 (Edge): fixed Skill saturation pre-flight VERBATIM on SYNTHETIC sat12.fa, then deep12.fa as contrast.
library(ape)
for (f in c('sat12', 'deep12')) {
aln <- read.dna(sprintf('../../data/%s.fa', f), format = 'fasta'); rownames(aln) <- trimws(rownames(aln))
cat('==', f, '\n')
L  <- ncol(aln)
p  <- dist.dna(aln, model = 'raw')          # p-distance
d  <- dist.dna(aln, model = 'TN93')         # corrected distance
ts <- dist.dna(aln, model = 'TS') / L       # 'TS'/'TV' return COUNTS -> divide by length for proportions
tv <- dist.dna(aln, model = 'TV') / L
print(mean(p > 0.5))                               # fraction of pairs with p > 0.5; any sizeable fraction = red flag
print(coef(lm(as.vector(ts) ~ as.vector(d)))[2])   # slope of transitions vs distance; near 0 = PLATEAU = saturated
png(sprintf('sat_plot_%s.png', f), 600, 500)
plot(d, ts, col = 'red', ylim = range(c(ts, tv))); points(d, tv, col = 'blue')   # unsaturated = both still rising
dev.off()
cat('mean ts/tv', round(mean(ts / tv), 2), ' NaN in TN93:', sum(is.nan(d)), '\n')
}
