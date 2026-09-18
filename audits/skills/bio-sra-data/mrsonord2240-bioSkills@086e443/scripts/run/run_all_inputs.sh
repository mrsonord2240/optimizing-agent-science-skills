#!/bin/bash
# Re-audit driver: bio-sra-data, second fix round (commit 086e443, branch fix/db-sra2).
# Regression-tests the two P1 findings from the pre-fix report
# (F:\OpenScience\audits\_pre-fix-20260918b\bio-sra-data\) plus new inputs this re-audit
# added on its own initiative. Run from this directory.
#
# Requires: the Skill copied to ./skill-copy (never executed inside F:\OpenScience\external\),
# real network access to www.ebi.ac.uk / ftp.sra.ebi.ac.uk for the "good" accessions.
#
# Usage: bash run_all_inputs.sh

set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="${HERE}/skill-copy"
OUT="${HERE}/out"
mkdir -p "${OUT}"

echo "### Extracting the inline 'Single SRR via ENA mirror' snippet from the shipped SKILL.md ###"
PYTHONIOENCODING=utf-8 python "${HERE}/extract_snippet.py" "${SKILL}/SKILL.md" > "${HERE}/extracted_inline_snippet.sh"
bash -n "${HERE}/extracted_inline_snippet.sh" && echo "  syntax OK"
bash -n "${SKILL}/examples/download_batch.sh" && echo "  download_batch.sh syntax OK"

echo
echo "=========================================================="
echo "Input 1 (Canonical, regression) -- inline snippet happy path, real accession"
echo "=========================================================="
rm -rf "${OUT}/in1"; mkdir -p "${OUT}/in1"
bash "${HERE}/extracted_inline_snippet.sh" ERR10419835 "${OUT}/in1"
echo "exit=$?"; ls -la "${OUT}/in1"; md5sum "${OUT}/in1"/*.fastq.gz 2>/dev/null

echo
echo "=========================================================="
echo "Input 2 (Variant A, regression) -- shipped download_batch.sh, all-good 3-accession batch"
echo "=========================================================="
rm -rf "${OUT}/in2"; mkdir -p "${OUT}/in2"
bash "${SKILL}/examples/download_batch.sh" "${HERE}/input_regression_all_good_batch.txt" "${OUT}/in2"
echo "exit=$?"; cat "${OUT}/in2/failed.txt"; md5sum "${OUT}/in2"/*.fastq.gz 2>/dev/null

echo
echo "=========================================================="
echo "Input 3 (Edge, NEW) -- independent synthetic missing-fastq_ftp fixture, inline snippet"
echo "Fixture: CONTROLLEDTEST1, built from ERR10419972's REAL 4-column TSV shape with fastq_ftp"
echo "stripped -- an accession/shape the fixer never used."
echo "=========================================================="
rm -rf "${OUT}/in3"; mkdir -p "${OUT}/in3"
PATH="${HERE}/fakebin:${PATH}" bash "${HERE}/extracted_inline_snippet.sh" CONTROLLEDTEST1 "${OUT}/in3" 2>&1
echo "exit=$?"; ls -la "${OUT}/in3"

echo
echo "=========================================================="
echo "Input 4 (Stress -- THE CRUX) -- mixed batch: real good, synthetic bad (middle), real good"
echo "=========================================================="
rm -rf "${OUT}/in4"; mkdir -p "${OUT}/in4"
PATH="${HERE}/fakebin:${PATH}" bash "${SKILL}/examples/download_batch.sh" "${HERE}/input_mixed_batch_bad_middle.txt" "${OUT}/in4"
echo "exit=$?"; cat "${OUT}/in4/failed.txt"; md5sum "${OUT}/in4"/*.fastq.gz 2>/dev/null

echo
echo "=========================================================="
echo "Input 5 (Variant B, NEW) -- position robustness: bad accession FIRST, then LAST"
echo "=========================================================="
rm -rf "${OUT}/in5a"; mkdir -p "${OUT}/in5a"
PATH="${HERE}/fakebin:${PATH}" bash "${SKILL}/examples/download_batch.sh" "${HERE}/input_mixed_batch_bad_first.txt" "${OUT}/in5a"
echo "exit=$?"; cat "${OUT}/in5a/failed.txt"
rm -rf "${OUT}/in5b"; mkdir -p "${OUT}/in5b"
PATH="${HERE}/fakebin:${PATH}" bash "${SKILL}/examples/download_batch.sh" "${HERE}/input_mixed_batch_bad_last.txt" "${OUT}/in5b"
echo "exit=$?"; cat "${OUT}/in5b/failed.txt"

echo
echo "=========================================================="
echo "Input 6 (Adversarial, NEW) -- reverse case: fastq_ftp PRESENT, fastq_md5 genuinely absent"
echo "=========================================================="
rm -rf "${OUT}/in6"; mkdir -p "${OUT}/in6"
PATH="${HERE}/fakebin:${PATH}" bash "${HERE}/extracted_inline_snippet.sh" CONTROLLEDTEST2 "${OUT}/in6" 2>&1
echo "exit=$?"; ls -la "${OUT}/in6"

echo
echo "=========================================================="
echo "Input 7 (Verification, NEW) -- completely empty/malformed ENA response, inline + batch"
echo "=========================================================="
rm -rf "${OUT}/in7_inline"; mkdir -p "${OUT}/in7_inline"
PATH="${HERE}/fakebin:${PATH}" bash "${HERE}/extracted_inline_snippet.sh" EMPTYRESP1 "${OUT}/in7_inline" 2>&1
echo "exit=$?"; ls -la "${OUT}/in7_inline"
rm -rf "${OUT}/in7_batch"; mkdir -p "${OUT}/in7_batch"
PATH="${HERE}/fakebin:${PATH}" bash "${SKILL}/examples/download_batch.sh" "${HERE}/input_mixed_batch_empty_response.txt" "${OUT}/in7_batch"
echo "exit=$?"; cat "${OUT}/in7_batch/failed.txt"; md5sum "${OUT}/in7_batch"/*.fastq.gz 2>/dev/null

echo
echo "All inputs done."
