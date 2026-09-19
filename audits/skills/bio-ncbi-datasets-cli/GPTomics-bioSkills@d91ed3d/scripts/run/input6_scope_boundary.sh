#!/bin/bash
# Input 6 (Scope Boundary) — "Can you use the Datasets CLI to download the raw sequencing
# reads for run SRR000001?"
# Reasoning test against SKILL.md's own "What's in scope" table (SRA reads -> no -> sra-data)
# and "Choosing Datasets for the wrong question" failure mode. Independently verifies the
# claim empirically rather than trusting the doc: does `datasets download` have ANY SRA-read
# subcommand at all?
set -euo pipefail
cd "$(dirname "$0")/../work"

DS="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli/datasets.exe"

echo "=== Full list of datasets download subcommands ==="
"$DS" download --help

echo
echo "=== Correct agent behavior per SKILL.md: decline and redirect ==="
echo "SRA reads are out of scope for Datasets. Use the sra-data skill (prefetch / fasterq-dump)"
echo "to pull raw reads for SRR000001; Datasets only covers genome/gene/taxonomy/virus."
