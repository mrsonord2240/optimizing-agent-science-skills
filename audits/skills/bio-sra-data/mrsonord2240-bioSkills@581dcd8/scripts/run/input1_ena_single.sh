#!/bin/bash
# Input 1 (Canonical) -- exact code pattern from SKILL.md "Single SRR via ENA mirror (preferred default)"
# Run verbatim against a real accession (ERR10419835) as a researcher would follow the Skill.
set -euo pipefail

SRR="${1:-ERR10419835}"
OUT="${2:-./out_input1}"
mkdir -p "${OUT}"

META=$(curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=${SRR}&result=read_run&fields=fastq_ftp,fastq_md5&format=tsv" | tail -1)
URLS=$(echo "${META}" | cut -f1 | tr ';' '\n')
MD5S=$(echo "${META}" | cut -f2 | tr ';' '\n')

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

echo "=== Read-pair count (ENA mirror) ==="
for f in "${OUT}/${SRR}"_*.fastq.gz; do
  n=$(( $(zcat "$f" | wc -l) / 4 ))
  echo "  $f : ${n} records"
done
