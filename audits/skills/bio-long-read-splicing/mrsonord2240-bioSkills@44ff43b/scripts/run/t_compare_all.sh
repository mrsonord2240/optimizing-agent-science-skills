#!/bin/bash
# Score FLAIR / IsoQuant outputs against planted truth with compare_counts.py (second method: exact intron-chain match).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
T=$R/data/synth/hifi/truth_counts.tsv; G=$R/data/synth/read_tx.gtf
C="asenv as-core python $R/compare_counts.py"
echo "=== FLAIR (correct -f gtf only, as SKILL minus nonexistent flags) -> collapse -> quantify"
$C $R/out/flair/collapsed.isoforms.bed $R/out/flair/quantified.counts.tsv $T $G
echo; echo "=== FLAIR (correct with --junction_bed short-read junctions) -> collapse -> quantify"
$C $R/out/flair/collapsedSR.isoforms.bed $R/out/flair/quantifiedSR.counts.tsv $T $G
echo; echo "=== IsoQuant 4.0.0 (pacbio_ccs, annotation-guided, 6 FASTQ)"
$C $R/out/isoquant/iq_hifi/OUT/OUT.extended_annotation.gtf $R/out/isoquant/iq_hifi/OUT/OUT.discovered_transcript_grouped_file_name_counts.tsv $T $G
