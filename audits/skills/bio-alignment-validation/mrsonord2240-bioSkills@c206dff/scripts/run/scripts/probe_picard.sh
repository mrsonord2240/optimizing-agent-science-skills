#!/bin/bash
# Picard 3.5.0 option syntax: skill uses legacy KEY=VALUE; check it and the required options / R dependency
for t in ValidateSamFile CollectInsertSizeMetrics CollectGcBiasMetrics CollectAlignmentSummaryMetrics CrosscheckFingerprints; do
  echo "### $t"; picard $t --help 2>&1 | grep -E '^--(INPUT|OUTPUT|HISTOGRAM_FILE|CHART_OUTPUT|SUMMARY_OUTPUT|REFERENCE_SEQUENCE|HAPLOTYPE_MAP|LOD_THRESHOLD|MODE|IGNORE|IS_BISULFITE_SEQUENCED)|Required|^--[A-Z_]+,-[A-Z]' | head -14
done
echo "### ValidateSamFile IGNORE types"; picard ValidateSamFile --help 2>&1 | sed -n '/--IGNORE </,/--IGNORE_WARNINGS/p' | head -20
echo "### Rscript on picard env?"; which Rscript; ls /home/sci/micromamba/envs/af-picard3/bin | grep -i -E '^R(script)?$'
