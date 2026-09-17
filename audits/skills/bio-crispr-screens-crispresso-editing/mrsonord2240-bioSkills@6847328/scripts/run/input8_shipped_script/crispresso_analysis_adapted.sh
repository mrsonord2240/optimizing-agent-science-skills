#!/bin/bash
# Runs the Skill's shipped examples/crispresso_analysis.sh (fixed version, commit 6847328)
# end-to-end, verbatim in structure, adapted only to point at real single-end test FASTQs
# (--fastq_r1 only, no --fastq_r2) since the audit's real data is single-end.
# Verifies the independently-found+fixed CRISPRessoCompare positional-argument bug:
# the fixed script uses positional output-folder args, not the old (nonexistent)
# --crispresso_output_folder_1/_2 flags.
set -e

AMPLICON="CGGATGTTCCAATCAGTACGCAGAGAGTCGCCGTCTCCAAGGTGAAAGCGGAAGTAGGGCCTTCGCGCACCTCATGGAATCCCTTCTGCAGCACCTGGATCGCTTTTCCGAGCTTCTGGCGGTCTCAAGCACTACCTACGTCAGCACCTGGGACCCCGCCACCGTGCGCCGGGCCTTGCAGTGGGCGCGCTACCTGCGCCACATCCATCGGCGCTTTGGTCGG"
GUIDE="GGAATCCCTTCTGCAGCACC"
OUTPUT_DIR="crispresso_results"

mkdir -p "$OUTPUT_DIR"

echo "Analyzing control sample..."
CRISPResso \
    --fastq_r1 FANC.Untreated.fastq \
    --amplicon_seq "$AMPLICON" \
    --guide_seq "$GUIDE" \
    --output_folder "$OUTPUT_DIR" \
    --name control \
    --quantification_window_size 10

echo "Analyzing edited sample..."
CRISPResso \
    --fastq_r1 FANC.Cas9.fastq \
    --amplicon_seq "$AMPLICON" \
    --guide_seq "$GUIDE" \
    --output_folder "$OUTPUT_DIR" \
    --name edited \
    --quantification_window_size 10

echo "Comparing samples..."
CRISPRessoCompare \
    "$OUTPUT_DIR/CRISPResso_on_control" \
    "$OUTPUT_DIR/CRISPResso_on_edited" \
    --output_folder "$OUTPUT_DIR/comparison"

echo "Analysis complete!"
echo "Results in: $OUTPUT_DIR"
