#!/bin/bash
# Reference: sra-tools 3.0+, aws-cli 2+ | Verify API if version differs
# Cloud-native SRA pull via AWS STRIDES (zero egress from EC2 in us-east-1) + 10x technical-reads support.

set -euo pipefail

SRR="${1:-SRR12345678}"
OUT="${2:-./fastq}"
THREADS="${3:-8}"
TENX="${4:-no}"  # 'yes' to keep technical reads (barcode/UMI/index) for 10x records

mkdir -p "${OUT}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=ena_fallback.sh
source "${SCRIPT_DIR}/ena_fallback.sh"

fallback_to_ena_or_die() {
    echo "SRA Toolkit/STRIDES route could not complete ${SRR}; no partial toolkit FASTQ was published."
    if run_ena_fallback "${SRR}" "${OUT}" "${SCRIPT_DIR}"; then
        echo "ENA fallback completed with MD5-verified FASTQ."
        exit 0
    fi
    echo "ENA fallback failed; no toolkit FASTQ was published." >&2
    exit 1
}

# Check if STRIDES (AWS Open Data) has the file
echo "=== Check STRIDES availability ==="
if command -v aws >/dev/null 2>&1 && aws s3 ls "s3://sra-pub-run-odp/sra/${SRR}/" --no-sign-request 2>/dev/null | grep -q "${SRR}"; then
    echo "  Available on AWS Open Data; pulling (free within us-east-1)"
    # STRIDES objects are unsuffixed (just SRR12345678); rename on copy.
    aws s3 cp "s3://sra-pub-run-odp/sra/${SRR}/${SRR}" "./${SRR}.sra" --no-sign-request
    SRA_PATH="./${SRR}.sra"
else
    echo "  AWS object unavailable (or aws CLI missing); trying NCBI prefetch"
    if ! prefetch "${SRR}" --max-size 200G -p; then
        fallback_to_ena_or_die
    fi
    SRA_PATH="${SRR}"
fi

echo
echo "=== Validate ==="
if ! vdb-validate "${SRA_PATH}"; then
    fallback_to_ena_or_die
fi

echo
echo "=== fasterq-dump ==="
TECH_FLAG="--skip-technical"
if [ "${TENX}" = "yes" ]; then
    TECH_FLAG="--include-technical"
    echo "  10x mode: keeping technical reads (R1=barcode+UMI, R2=cDNA, I1=index for 10x v3)"
fi

TOOLKIT_OUT=$(mktemp -d "${OUT%/}/.${SRR}.toolkit.XXXXXX")
if ! fasterq-dump "${SRA_PATH}" \
    -O "${TOOLKIT_OUT}" \
    -e "${THREADS}" \
    -p \
    --split-files \
    ${TECH_FLAG}; then
    rm -rf "${TOOLKIT_OUT}"
    fallback_to_ena_or_die
fi

echo
echo "=== Compress (fasterq-dump does NOT compress; pigz has no Windows build) ==="
if command -v pigz >/dev/null 2>&1; then
    pigz -p "${THREADS}" "${TOOLKIT_OUT}/${SRR}"_*.fastq
else
    gzip "${TOOLKIT_OUT}/${SRR}"_*.fastq
fi

for file in "${TOOLKIT_OUT}/${SRR}"_*.fastq.gz; do
    if [ -e "${OUT}/$(basename "${file}")" ]; then
        echo "Refusing to overwrite existing output: ${OUT}/$(basename "${file}")" >&2
        exit 1
    fi
done
mv "${TOOLKIT_OUT}/${SRR}"_*.fastq.gz "${OUT}/"
rmdir "${TOOLKIT_OUT}"

echo
echo "=== Cleanup ==="
rm -f "./${SRR}.sra"
rm -rf "${SRR}"  # SRA cache directory if prefetch used

echo
echo "Files:"
ls -lh "${OUT}/${SRR}"_*.fastq.gz
