# De-array Kinnex/MAS HiFi reads into segmented reads (S-reads). The adapter FASTA lists the kit's adapters in array order
# (mas16_primers.fasta for the 16-fold single-cell kit, from PacBio via skera.how/adapters)
skera split \
    raw_kinnex.bam \
    mas16_primers.fasta \
    segmented.bam

# Then lima -> isoseq refine -> isoseq cluster2 (bioconda lima, isoseq; see long-read-sequencing/isoseq-analysis)
