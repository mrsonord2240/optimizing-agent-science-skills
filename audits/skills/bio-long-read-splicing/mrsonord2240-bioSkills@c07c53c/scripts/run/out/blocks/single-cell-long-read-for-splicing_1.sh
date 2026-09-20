# Demultiplex MAS-Iso-seq reads (command checked against `skera split --help`, skera 1.4.0; not run: no Kinnex data)
skera split \
    raw_kinnex.bam \
    mas12_primers.fasta \
    demuxed.bam

# Then lima -> isoseq refine -> isoseq cluster2 (bioconda lima, isoseq; see long-read-sequencing/isoseq-analysis)
