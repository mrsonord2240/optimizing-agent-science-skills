#!/bin/bash
set -uo pipefail
OUT=./sim_out
mkdir -p "${OUT}"
# Simulates ENA's real response when fastq_ftp is omitted for a run (controlled-access-like)
RESPONSE=$(printf 'run_accession\trun_alias\nERR_CONTROLLED\twhatever')
HEADER=$(echo "${RESPONSE}" | head -1)
ROW=$(echo "${RESPONSE}" | tail -1)
FTP_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_ftp' | cut -d: -f1)
MD5_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_md5' | cut -d: -f1)
URLS=$(echo "${ROW}" | cut -f"${FTP_COL}" | tr ';' '\n')
MD5S=$(echo "${ROW}" | cut -f"${MD5_COL}" | tr ';' '\n')
echo "FTP_COL=[${FTP_COL}] MD5_COL=[${MD5_COL}]"
echo "URLS=[${URLS}]"
echo "MD5S=[${MD5S}]"

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
    echo "  md5 OK"
    i=$((i+1))
done <<< "${URLS}"
echo "SCRIPT COMPLETED, exit 0"
