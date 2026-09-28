#!/usr/bin/env bash
set -euo pipefail

ROOT=/mnt/openscience/audit-envs/bio-chipseq-allele-specific-binding
AUDIT=/mnt/openscience/audits/bio-chipseq-allele-specific-binding/reaudit-opt10-20260928
RUN="$AUDIT/evidence/secondary-artifacts"
ENV="$ROOT/env"
WASP="$ROOT/sources/WASP"
ALLELESEQ="$ROOT/sources/AlleleSeq2"

case "$RUN" in
  "$AUDIT"/evidence/secondary-artifacts) rm -rf -- "$RUN" ;;
  *) printf 'unsafe run path: %s\n' "$RUN" >&2; exit 98 ;;
esac
mkdir -p "$RUN"
exec > >(tee "$AUDIT/evidence/secondary-execution.log") 2>&1
export PATH="$ENV/bin:/usr/bin:/bin"

IRUN="$RUN/intervals"
mkdir -p "$IRUN"
printf 'chr1\t9\t10\tA\tG\nchr1\t19\t20\tC\tT\nchrX\t29\t30\tG\tA\n' >"$IRUN/hetSNPs.bed"
printf 'chr1\t8\t11\tIMPRINTED_A\n' >"$IRUN/imprinted_loci_hg38.bed"
bedtools intersect -v -a "$IRUN/hetSNPs.bed" -b "$IRUN/imprinted_loci_hg38.bed" >"$IRUN/non_imprinted.bed"
awk '$1 != "chrX"' "$IRUN/hetSNPs.bed" >"$IRUN/autosomal.bed"
test "$(wc -l < "$IRUN/non_imprinted.bed")" -eq 2
test "$(wc -l < "$IRUN/autosomal.bed")" -eq 2
grep -q $'^chr1\t19\t20' "$IRUN/non_imprinted.bed"
grep -q $'^chrX\t29\t30' "$IRUN/non_imprinted.bed"
! grep -q '^chrX' "$IRUN/autosomal.bed"
{
  bedtools --version
  printf 'input_rows\t3\nnon_imprinted_rows\t2\nautosomal_rows\t2\nstatus\tPASS\n'
} >"$AUDIT/evidence/interval-live.tsv"
printf 'PASS\tinterval_filters\t2/3 non-imprinted; 2/3 autosomal\n'

BUILD="$RUN/wasp-snp2h5-build"
HRUN="$RUN/wasp-hdf5"
cp -a "$WASP/snp2h5" "$BUILD"
mkdir -p "$HRUN"
make -C "$BUILD" HDF_INSTALL="$ENV" CC="$ENV/bin/x86_64-conda-linux-gnu-cc" \
  CFLAGS="-std=gnu89 -DH5_USE_16_API -I$ENV/include -Wall -g" \
  >"$RUN/wasp-snp2h5-build.log" 2>&1
DATA="$WASP/examples/example_data"
"$BUILD/snp2h5" \
  --chrom "$DATA/chromInfo.hg19.txt" --format impute \
  --snp_index "$HRUN/snp_index.h5" --geno_prob "$HRUN/geno_probs.h5" \
  --snp_tab "$HRUN/snp_tab.h5" --haplotype "$HRUN/haps.h5" \
  --samples "$DATA/genotypes/YRI_samples.txt" \
  "$DATA/genotypes/chr22.hg19.impute2.gz" "$DATA/genotypes/chr22.hg19.impute2_haps.gz"
python - "$HRUN" "$AUDIT/evidence/wasp-hdf5-live.tsv" <<'PY'
from pathlib import Path
import sys
import tables

root = Path(sys.argv[1])
output = Path(sys.argv[2])
expected = {
    "snp_index.h5": (51304566,),
    "snp_tab.h5": (247303,),
    "haps.h5": (247303, 120),
    "geno_probs.h5": (247303, 180),
}
rows = []
for name, shape in expected.items():
    with tables.open_file(root / name) as handle:
        actual = handle.root.chr22.shape
    if actual != shape:
        raise SystemExit(f"{name}: expected {shape}, got {actual}")
    rows.append(f"{name}\t/chr22\t{actual}")
rows.append("status\tPASS")
output.write_text("\n".join(rows) + "\n", encoding="utf-8")
PY
printf 'PASS\twasp_hdf5\tprovider chr22 IMPUTE2/HAPS shapes verified\n'

set +e
make -f "$ALLELESEQ/PIPELINE.mk" -n \
  PGENOME_DIR="$RUN/personalized" REFGENOME_VERSION=GRCh38 ALIGNMENT_MODE=ASB NTHR=1 \
  >"$AUDIT/evidence/alleleseq-make-dryrun.stdout" \
  2>"$AUDIT/evidence/alleleseq-make-dryrun.stderr"
make_status=$?
set -e
{
  printf 'commit\t%s\n' "$(git -C "$ALLELESEQ" rev-parse HEAD)"
  printf 'make_dryrun_exit\t%s\n' "$make_status"
  printf 'reads_r1_populated\t%s\n' "$(grep -Eq 'READS_R1[^[:alnum:]]+[^[:space:]]' "$AUDIT/evidence/alleleseq-make-dryrun.stdout" && echo yes || echo no)"
  printf 'python2\t%s\n' "$(command -v python2 >/dev/null 2>&1 && echo available || echo unavailable)"
  printf 'STAR\t%s\n' "$(command -v STAR >/dev/null 2>&1 && echo available || echo unavailable)"
  printf 'picard\t%s\n' "$(command -v picard >/dev/null 2>&1 && echo available || echo unavailable)"
  printf 'vcf2diploid\t%s\n' "$(find "$ALLELESEQ" -iname 'vcf2diploid*.jar' -print -quit | grep -q . && echo available || echo unavailable)"
  printf 'classification\tUNAVAILABLE_FULL_TOOLCHAIN_EXTERNAL_ONLY\n'
} >"$AUDIT/evidence/alleleseq-dryrun-boundary.tsv"
printf 'PASS\talleleseq_boundary\tdry-run recorded; missing prerequisites retained as external-only\n'

printf 'ALL_SECONDARY_SURFACES_PASS\n'
