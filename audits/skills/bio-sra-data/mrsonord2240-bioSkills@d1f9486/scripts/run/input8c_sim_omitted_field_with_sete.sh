#!/bin/bash
set -euo pipefail
OUT=./sim_out2
mkdir -p "${OUT}"
RESPONSE=$(printf 'run_accession\trun_alias\nERR_CONTROLLED\twhatever')
HEADER=$(echo "${RESPONSE}" | head -1)
ROW=$(echo "${RESPONSE}" | tail -1)
FTP_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_ftp' | cut -d: -f1)
MD5_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_md5' | cut -d: -f1)
URLS=$(echo "${ROW}" | cut -f"${FTP_COL}" | tr ';' '\n')
MD5S=$(echo "${ROW}" | cut -f"${MD5_COL}" | tr ';' '\n')
echo "reached after URLS/MD5S assignment -- should not print if set -e caught the cut failure"
