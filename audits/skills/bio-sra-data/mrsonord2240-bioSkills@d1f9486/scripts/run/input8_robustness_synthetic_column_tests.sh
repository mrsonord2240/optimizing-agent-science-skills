#!/bin/bash
set -uo pipefail

test_case() {
    local name="$1"
    local RESPONSE="$2"
    echo "--- ${name} ---"
    HEADER=$(echo "${RESPONSE}" | head -1)
    ROW=$(echo "${RESPONSE}" | tail -1)
    FTP_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_ftp' | cut -d: -f1)
    MD5_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_md5' | cut -d: -f1)
    echo "  header=[${HEADER}]"
    echo "  row=[${ROW}]"
    echo "  FTP_COL=${FTP_COL}  MD5_COL=${MD5_COL}"
    if [ -z "${FTP_COL}" ]; then
        echo "  URLS: (empty -- FTP_COL not found)"
    else
        URLS=$(echo "${ROW}" | cut -f"${FTP_COL}")
        echo "  URLS=${URLS}"
    fi
    if [ -z "${MD5_COL}" ]; then
        echo "  MD5S: (empty -- MD5_COL not found)"
    else
        MD5S=$(echo "${ROW}" | cut -f"${MD5_COL}")
        echo "  MD5S=${MD5S}"
    fi
    echo
}

nl=$'\n'

# Case B: reordered -- fastq_md5 before fastq_ftp, run_accession last
RESP_B="fastq_md5${nl/  /}"
RESP_B=$(printf 'fastq_md5\tfastq_ftp\trun_accession\naaa;bbb\tftp.example/1.fastq.gz;ftp.example/2.fastq.gz\tERR999')
test_case "B: reordered columns (2-line, correct construction)" "${RESP_B}"

# Case F: ENA-like order but with an ADDITIONAL leading unexpected column (e.g. a future API version)
RESP_F=$(printf 'study_accession\trun_accession\tfastq_ftp\tfastq_md5\nPRJ999\tERR999\tftp.example/1.fastq.gz;ftp.example/2.fastq.gz\taaa;bbb')
test_case "F: extra leading column, real 2-line TSV" "${RESP_F}"

# Case G: tab-separated but fastq_ftp column present, fastq_md5 truly absent (server didn't return it), still 2 lines
RESP_G=$(printf 'run_accession\tfastq_ftp\nERR999\tftp.example/1.fastq.gz;ftp.example/2.fastq.gz')
test_case "G: fastq_md5 absent, 2-line TSV" "${RESP_G}"

# Case H: whitespace/case variation in header name (defensive test - grep -nx is exact match, case sensitive)
RESP_H=$(printf 'run_accession\tFastq_Ftp\tfastq_md5\nERR999\tftp.example/1.fastq.gz\taaa')
test_case "H: header name case mismatch" "${RESP_H}"
