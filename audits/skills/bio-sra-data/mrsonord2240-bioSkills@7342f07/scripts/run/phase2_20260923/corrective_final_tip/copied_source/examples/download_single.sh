#!/bin/bash
# Reference: sra-tools 3.0+ | Verify API if version differs
# Single-run SRA download via the toolkit path: prefetch (with explicit --max-size) + vdb-validate + fasterq-dump + pigz.

set -euo pipefail

SRR="${1:-SRR12345678}"
OUT="${2:-./fastq}"
THREADS="${3:-8}"
MAX_SIZE="${4:-100G}"  # Default 20G silently skips larger -- always set explicitly

mkdir -p "${OUT}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=ena_fallback.sh
source "${SCRIPT_DIR}/ena_fallback.sh"

fallback_to_ena_or_die() {
    echo "SRA Toolkit could not complete ${SRR}; no partial toolkit FASTQ was published."
    if run_ena_fallback "${SRR}" "${OUT}" "${SCRIPT_DIR}"; then
        echo "ENA fallback completed with MD5-verified FASTQ."
        exit 0
    fi
    echo "ENA fallback failed; no toolkit FASTQ was published." >&2
    exit 1
}

echo "=== prefetch ${SRR} (max-size ${MAX_SIZE}) ==="
if ! prefetch "${SRR}" --max-size "${MAX_SIZE}" -p; then
    fallback_to_ena_or_die
fi

echo
echo "=== vdb-validate ==="
if ! vdb-validate "${SRR}"; then
    fallback_to_ena_or_die
fi

echo
echo "=== fasterq-dump (writes uncompressed; needs ~3x final size in scratch) ==="
# --split-files: emit _1.fastq and _2.fastq for paired
# DROP --skip-technical if this is 10x or other single-cell data (need barcodes/UMIs)
TOOLKIT_OUT=$(mktemp -d "${OUT%/}/.${SRR}.toolkit.XXXXXX")
if ! fasterq-dump "${SRR}" \
    -O "${TOOLKIT_OUT}" \
    -e "${THREADS}" \
    -p \
    --split-files \
    --skip-technical; then
    rm -rf "${TOOLKIT_OUT}"
    fallback_to_ena_or_die
fi

echo
echo "=== compression (fasterq-dump does NOT compress; pigz has no Windows build) ==="
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
echo "Files:"
ls -lh "${OUT}/${SRR}"_*.fastq.gz

echo
echo "Optional cleanup:"
echo "  rm -rf \"${SRR}\"   # remove cached .sra after successful FASTQ extraction"
