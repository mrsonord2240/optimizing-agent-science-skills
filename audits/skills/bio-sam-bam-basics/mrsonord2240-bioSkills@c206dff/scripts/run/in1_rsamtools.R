# Input 1 add-on: the R bullet in SKILL.md ("R: scanBam() (Rsamtools)"), run through the env's r.sh (never bare Rscript).
suppressPackageStartupMessages(library(Rsamtools))
cat("Rsamtools", as.character(packageVersion("Rsamtools")), "\n")
bam <- "F:/OpenScience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam"
sb <- scanBam(bam, param = ScanBamParam(what = c("qname", "flag", "pos", "cigar", "mapq")))[[1]]
cat("scanBam records:", length(sb$qname), "\n")
cat("first read:", sb$qname[1], sb$flag[1], sb$pos[1], sb$cigar[1], sb$mapq[1], "\n")
stopifnot(length(sb$qname) == 5644)           # matches samtools view -c
stopifnot(sb$pos[1] == 1952)                  # Rsamtools pos is 1-based like SAM POS (pysam reference_start would be 1951)
stopifnot(sb$flag[1] == 99, sb$cigar[1] == "130M13S", sb$mapq[1] == 60)
cat("ASSERTIONS OK: scanBam count 5644, pos 1-based 1952, flag 99, CIGAR 130M13S\n")
