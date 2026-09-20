#!/bin/bash
# Verify every flag / subcommand claim in SKILL.md against the installed tools.
# Output is captured to run/out/probe_help.txt by the caller.
R=/mnt/openscience/audits/bio-alignment-validation/run
D=$AFDATA
echo "### versions"
samtools --version | head -1; python -c "import pysam;print('pysam',pysam.__version__)"; picard ValidateSamFile --version 2>&1 | tail -1
echo "### awk flavour"; awk --version 2>&1 | head -1; awk -W version 2>&1 | head -1; which awk gawk mawk
echo "### samtools quickcheck usage"; samtools quickcheck 2>&1 | head -20
echo "### samtools view -s help"; samtools view 2>&1 | grep -E '^\s+-s|subsamp'
echo "### samtools dict usage"; samtools dict 2>&1 | head -20
echo "### samtools flagstat usage"; samtools flagstat 2>&1 | head -12
echo "### picard ValidateSamFile IGNORE enum"; picard ValidateSamFile --help 2>&1 | grep -E 'INVALID_MAPPING_QUALITY|MISMATCH_FLAG_MATE_NEG_STRAND|IGNORE|MODE' | head -12
echo "### picard ValidateSamFile options"; picard ValidateSamFile --help 2>&1 | grep -E '^(R|REFERENCE_SEQUENCE|I|INPUT|MODE|IGNORE|IS_BISULFITE|VALIDATE_INDEX|IGNORE_WARNINGS)=' | head
echo "### picard CollectInsertSizeMetrics required"; picard CollectInsertSizeMetrics --help 2>&1 | grep -E '^(H|HISTOGRAM_FILE|O|OUTPUT|I)=' | head
echo "### picard CollectGcBiasMetrics required"; picard CollectGcBiasMetrics --help 2>&1 | grep -E '^(CHART|CHART_OUTPUT|S|SUMMARY_OUTPUT|R|REFERENCE_SEQUENCE|O|OUTPUT)=' | head
echo "### picard CollectAlignmentSummaryMetrics"; picard CollectAlignmentSummaryMetrics --help 2>&1 | grep -E '^(R|O|I)=' | head
echo "### picard CrosscheckFingerprints"; picard CrosscheckFingerprints --help 2>&1 | grep -E '^(HAPLOTYPE_MAP|H|LOD_THRESHOLD|I|INPUT)=' | head
echo "### picard CollectMultipleMetrics / CollectHsMetrics / CollectWgsMetrics exist"; for t in CollectMultipleMetrics CollectHsMetrics CollectWgsMetrics; do picard $t --help 2>&1 | grep -m1 -E "^$t|USAGE" ; done
echo "### deepTools computeGCBias"; computeGCBias --help 2>&1 | grep -E '^\s+(--bamfile|-b|-g|--genome|--effectiveGenomeSize|--GCbiasFrequenciesFile|-freq|-o|--biasPlot|--plotFileFormat|--fragmentLength|-l|--regionSize)' | head -20
echo "### verifybamid2 options"; verifybamid2 --help 2>&1 | head -40
echo "### somalier"; somalier extract 2>&1 | head -30; somalier relate 2>&1 | head -40
echo "### plot-bamstats"; plot-bamstats 2>&1 | head -8
echo "### infer_experiment.py"; infer_experiment.py --help 2>&1 | head -5
echo "### samtools stats IS / summary"; samtools stats $D/human/test.paired_end.sorted.bam | grep -E '^(IS|SN)' | head -40
