#!/bin/bash
# A4: ABC main (92ac503) official chr22 Snakemake test, rerun in audit (FORCE regenerates test_output)
source /mnt/openscience/audits/bio-atac-seq-enhancer-gene-linking/initial-audit-20260930/scripts/common.sh
FORCE=1 ABC_DIR=abc-head bash $EG/run_abc_official.sh
