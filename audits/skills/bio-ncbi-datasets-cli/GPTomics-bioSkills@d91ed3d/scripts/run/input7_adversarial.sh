#!/bin/bash
# Input 7 (Adversarial) — "Get the assembly summary for GCF_999999999.1. If that doesn't
# work, try 'NOT_AN_ACCESSION'."
# Tests error-handling behavior for a well-formed-but-nonexistent accession vs. a
# malformed one, specifically checking exit codes (per the audit brief's "judge by output,
# never exit code" rule) rather than trusting a 0 exit code as success.
set -euo pipefail
cd "$(dirname "$0")/../work"

DS="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli/datasets.exe"

echo "=== Well-formed but nonexistent accession ==="
set +e
"$DS" summary genome accession GCF_999999999.1
echo "exit code: $?"
set -e

echo
echo "=== Malformed accession ==="
set +e
"$DS" summary genome accession NOT_AN_ACCESSION
echo "exit code: $?"
set -e
