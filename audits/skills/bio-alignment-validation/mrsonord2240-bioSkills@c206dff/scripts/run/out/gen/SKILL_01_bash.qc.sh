# Fast: header + EOF block check (misses mid-file truncation, invalid CIGAR)
samtools quickcheck -v x.bam || echo "QUICKCHECK FAILED"
samtools quickcheck -v *.bam > bad_bams.fofn   # one fail-line per bad file

# Slow but thorough: structural validation
picard ValidateSamFile I=x.bam MODE=SUMMARY R=/mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta

# Production: ignore expected-but-noisy
picard ValidateSamFile I=x.bam MODE=SUMMARY R=/mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta \
    IGNORE=INVALID_MAPPING_QUALITY \
    IGNORE=MISMATCH_FLAG_MATE_NEG_STRAND
