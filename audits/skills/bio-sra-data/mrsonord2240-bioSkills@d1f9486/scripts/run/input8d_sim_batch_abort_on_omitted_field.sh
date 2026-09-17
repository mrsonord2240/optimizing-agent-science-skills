#!/bin/bash
set -euo pipefail
OUT=./sim_batch_out
mkdir -p "${OUT}"
FAILED="${OUT}/failed.txt"
: > "${FAILED}"

ACCESSIONS="GOOD1 CONTROLLED GOOD2"
total=3
count=0
ok=0

get_response() {
    local acc="$1"
    if [ "${acc}" = "CONTROLLED" ]; then
        printf 'run_accession\trun_alias\nCONTROLLED\twhatever'
    else
        printf 'run_accession\tfastq_ftp\tfastq_md5\n%s\tftp.example/%s_1.fastq.gz;ftp.example/%s_2.fastq.gz\taaa;bbb' "${acc}" "${acc}" "${acc}"
    fi
}

for ACC in ${ACCESSIONS}; do
    count=$((count+1))
    echo
    echo "[${count}/${total}] ${ACC}"
    RESPONSE=$(get_response "${ACC}")
    HEADER=$(echo "${RESPONSE}" | head -1)
    ROW=$(echo "${RESPONSE}" | tail -1)
    FTP_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_ftp' | cut -d: -f1)
    MD5_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_md5' | cut -d: -f1)

    URLS=$(echo "${ROW}" | cut -f"${FTP_COL}" | tr ';' '\n')
    MD5S=$(echo "${ROW}" | cut -f"${MD5_COL}" | tr ';' '\n')
    echo "  URLS=${URLS}"
    ok=$((ok+1))
done
echo "=== Summary === OK: ${ok}/${total}"
