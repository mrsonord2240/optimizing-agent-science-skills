#!/bin/bash
SRR="${1:-SRR12345678}"
OUT="${2:-./fastq}"
mkdir -p "${OUT}"

# Get FASTQ URLs + md5 from ENA portal API. Locate columns by their documented field
# name, not a fixed index: ENA's filereport ALWAYS prepends run_accession as column 1,
# regardless of what `fields=` lists, so fields=fastq_ftp,fastq_md5 puts the real data
# in columns 2 and 3, not 1 and 2 (cut -f1/-f2 silently grabs the accession and the URL,
# one column short -- confirmed against the live API).
RESPONSE=$(curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=${SRR}&result=read_run&fields=fastq_ftp,fastq_md5&format=tsv")
HEADER=$(echo "${RESPONSE}" | head -1)
ROW=$(echo "${RESPONSE}" | tail -1)
FTP_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_ftp' | cut -d: -f1)
MD5_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_md5' | cut -d: -f1)
URLS=$(echo "${ROW}" | cut -f"${FTP_COL}" | tr ';' '\n')
MD5S=$(echo "${ROW}" | cut -f"${MD5_COL}" | tr ';' '\n')

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
