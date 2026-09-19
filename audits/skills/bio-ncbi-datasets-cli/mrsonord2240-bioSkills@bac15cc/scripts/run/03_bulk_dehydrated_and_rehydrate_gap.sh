#!/bin/bash
# Re-audit inputs 3/5 (Edge + Stress, regression) — bac15cc
# PLUS a new finding: `datasets rehydrate` does not verify pre-existing files, even
# though SKILL.md and bulk_dehydrated.sh's own "Step 3: verify" comment claim it does.
#
# WSL calls use: MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc '...'
# aria2c lives in the WSL science distro's bio env; only F:\OpenScience is mounted there,
# so the aria2c leg was run from a scratch dir under the shared tools\ncbi-datasets-cli\
# folder (deleted after use, same convention the fixer used).
set -euo pipefail
export PATH="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli:$PATH"

echo "=== regression: single-accession dehydrate + fetch.txt column check ==="
datasets.exe download genome accession GCF_000819615.1 --dehydrated \
    --filename phix_dehy.zip --no-progressbar
unzip -q phix_dehy.zip -d phix_dehy/
cat phix_dehy/ncbi_dataset/fetch.txt
awk -F'\t' '{print NF}' phix_dehy/ncbi_dataset/fetch.txt   # expect 3

echo "=== NEW species (not the fixer's Deinococcus): fresh bulk dehydrated + rehydrate ==="
datasets.exe download genome taxon "Mycoplasma genitalium" \
    --reference --annotated --assembly-source RefSeq --include genome,gff3,protein \
    --dehydrated --filename myco_dehy.zip --no-progressbar
unzip -q myco_dehy.zip -d myco_dehy/
FETCH=myco_dehy/ncbi_dataset/fetch.txt
wc -l "$FETCH"
awk -F'\t' '{print $1"\n  out="$3}' "$FETCH" > myco_aria2_input.txt
grep -c '^  out=0$' myco_aria2_input.txt && echo "CORRUPTION" || echo "no out=0 corruption (fix holds)"
datasets.exe rehydrate --directory myco_dehy/ --max-workers 4
find myco_dehy/ncbi_dataset/data/ -type f | sort
# All real files, correct paths, no file literally named "0".

echo
echo "=== NEW FINDING: does 'datasets rehydrate' (the script's documented Step 3 'verify')"
echo "    actually catch a corrupted/wrong-size pre-existing file? ==="
python -c "import json; d=json.load(open('myco_dehy/ncbi_dataset/data/dataset_catalog.json')); [print(f['filePath'], f['uncompressedLengthBytes']) for a in d['assemblies'] for f in a['files']]"
# genomic.gff catalog-recorded size: 373156 bytes

echo "THIS IS NOT REAL GFF DATA - CORRUPTED FOR TESTING" > myco_dehy/ncbi_dataset/data/GCF_040556925.1/genomic.gff
ls -la myco_dehy/ncbi_dataset/data/GCF_040556925.1/genomic.gff   # 50 bytes, catalog expects 373156

datasets.exe rehydrate --directory myco_dehy/ --max-workers 4
# Output: "All 3 files already rehydrated" -- no re-fetch, no error, no warning.

cat myco_dehy/ncbi_dataset/data/GCF_040556925.1/genomic.gff
# Still the 50-byte corrupted placeholder text, unchanged. rehydrate reported success anyway.

# CONCLUSION: `datasets rehydrate` treats a file's mere presence on disk at the expected
# path as "already rehydrated" -- it does not check the file's size (despite recording the
# correct expected size in its own dataset_catalog.json) or checksum. This directly
# contradicts SKILL.md's "Checksum verification (automatic)... Rehydrate workflows also
# verify" claim and bulk_dehydrated.sh's own Step 3 comment ("datasets rehydrate validates
# checksums of all files") for the exact compound aria2c+rehydrate HPC pattern the Skill
# recommends for bulk pulls. Reproduced live twice (once via a real NCBI bot-block through
# WSL aria2c that silently wrote the misuse.ncbi.nlm.nih.gov abuse page as if it were real
# genome data, and once via manual byte-for-byte corruption) -- not an artifact of the WSL
# network issue.
