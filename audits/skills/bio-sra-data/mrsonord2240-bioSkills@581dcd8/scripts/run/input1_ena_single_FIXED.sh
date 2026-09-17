#!/bin/bash
# Corrected version of SKILL.md's ENA snippet, to confirm root cause: ENA's filereport API
# always prepends run_accession as column 1, regardless of the `fields` param, so with
# fields=fastq_ftp,fastq_md5 the real columns are (1=run_accession, 2=fastq_ftp, 3=fastq_md5)
# -- not (1=fastq_ftp, 2=fastq_md5) as SKILL.md's cut -f1/-f2 assumes.
set -euo pipefail

SRR="${1:-ERR10419835}"
OUT="${2:-./out_input1_fixed}"
mkdir -p "${OUT}"

META=$(curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=${SRR}&result=read_run&fields=fastq_ftp,fastq_md5&format=tsv" | tail -1)
URLS=$(echo "${META}" | cut -f2 | tr ';' '\n')
MD5S=$(echo "${META}" | cut -f3 | tr ';' '\n')

i=0
while read url; do
    fname="${OUT}/$(basename ${url})"
    expected_md5=$(echo "${MD5S}" | sed -n "$((i+1))p")
    echo "Downloading ${fname}"
    curl -sL -o "${fname}" "https://${url}"
    actual_md5=$(md5sum "${fname}" | awk '{print $1}')
    if [ "${actual_md5}" != "${expected_md5}" ]; then
        echo "MD5 MISMATCH ${fname}: expected ${expected_md5}, got ${actual_md5}"
        exit 1
    fi
    echo "  md5 OK (${actual_md5})"
    i=$((i+1))
done <<< "${URLS}"
