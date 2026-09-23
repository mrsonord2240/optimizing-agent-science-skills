#!/usr/bin/env bash
# Final-pass Phase 2 execution for bio-reference-operations.
set -euo pipefail

ROOT=/mnt/openscience/audits/bio-reference-operations/run
SRC=/mnt/openscience/wt/reference-operations/alignment-files/reference-operations
WORK="$ROOT/work"
DATA="$ROOT/data"
mkdir -p "$WORK" "$DATA" "$ROOT/copied_skill"
rm -rf "$WORK" "$ROOT/copied_skill"
mkdir -p "$WORK" "$ROOT/copied_skill/scripts" "$ROOT/copied_skill/examples"
cp "$SRC/scripts/pysam_consensus.py" "$ROOT/copied_skill/scripts/"
cp "$SRC/scripts/rename_contigs.sh" "$ROOT/copied_skill/scripts/"
cp "$SRC/examples/prepare_reference.sh" "$ROOT/copied_skill/examples/"
python "$ROOT/make_fixture.py"
cd "$WORK"

assert_eq() { [ "$1" = "$2" ] || { echo "ASSERT_FAIL: $3 expected=$2 actual=$1" >&2; exit 1; }; }
assert_file() { [ -s "$1" ] || { echo "ASSERT_FAIL: missing/nonempty $1" >&2; exit 1; }; }

echo 'INPUT 1 regression: prepare-reference workflow'
bash "$ROOT/copied_skill/examples/prepare_reference.sh" "$DATA/toy.fa" > input1.log
assert_file "$DATA/toy.fa.fai"; assert_file "$DATA/toy.dict"; assert_file "$DATA/toy.chrom.sizes"
samtools dict "$DATA/toy.fa" | diff - "$DATA/toy.dict"
assert_eq "2" "$(wc -l < "$DATA/toy.chrom.sizes")" 'two chrom sizes'

echo 'INPUT 2 regression: faidx extraction, strand, and subset failure handling'
samtools faidx "$DATA/toy.fa" chr1:2-10 > input2_region.fa
assert_eq "9" "$(tail -n +2 input2_region.fa | tr -d '\n' | wc -c)" 'inclusive faidx length'
samtools faidx -i "$DATA/toy.fa" chr1:2-10 > input2_rc.fa
grep -q '/rc$' <(head -1 input2_rc.fa)
set +e
samtools faidx "$DATA/toy.fa" chr1 chr404 > bad_subset.fa 2> input2_bad.err
rc=$?
set -e
assert_eq "$rc" "1" 'missing contig exits one'

echo 'INPUT 3 regression: header-only contig renaming and reference check'
printf 'chr1\t1\nchr2\t2\n' > map.tsv
samtools faidx "$DATA/toy_numeric.fa"
bash "$ROOT/copied_skill/scripts/rename_contigs.sh" "$DATA/toy.bam" map.tsv renamed.bam "$DATA/toy_numeric.fa" > input3.log
assert_eq "14" "$(samtools view -c renamed.bam)" 'renamed BAM retains records'
samtools view -H renamed.bam | grep -q $'SN:1\tLN:120'

echo 'INPUT 4 regression: samtools consensus mode produces padded reference length'
samtools consensus -m simple -d 3 -a --show-del yes --show-ins no "$DATA/toy.bam" -o input4.fa
assert_eq "120" "$(tail -n +2 input4.fa | tr -d '\n' | wc -c)" 'padded consensus length'
grep -q 'N' <(tail -n +2 input4.fa)

echo 'INPUT 5 regression: pedagogical pysam consensus and 1-based comparison'
python "$ROOT/copied_skill/scripts/pysam_consensus.py" consensus "$DATA/toy.bam" chr1 0 120 --min-depth 3 > input5.consensus
assert_eq "120" "$(tr -d '\n' < input5.consensus | wc -c)" 'python consensus window length'
python "$ROOT/copied_skill/scripts/pysam_consensus.py" compare "$DATA/toy.bam" "$DATA/toy.fa" chr1 0 120 --min-depth 3 > input5.compare
assert_eq "1" "$(wc -l < input5.compare)" 'one planted majority difference'
assert_eq "10" "$(cut -f1 input5.compare)" 'comparison coordinates are one based'
REAL=/mnt/openscience/audit-envs/alignment-files/public-data/human
python "$ROOT/copied_skill/scripts/pysam_consensus.py" consensus "$REAL/test.paired_end.sorted.bam" chr22 1951 4617 --min-depth 3 > input5.real.consensus
python "$ROOT/copied_skill/scripts/pysam_consensus.py" compare "$REAL/test.paired_end.sorted.bam" "$REAL/genome.fasta" chr22 1951 4617 --min-depth 3 > input5.real.compare
assert_eq "2666" "$(tr -d '\n' < input5.real.consensus | wc -c)" 'real chr22 window length'
assert_eq $'3266\tT\tC' "$(tr -d '\n' < input5.real.compare)" 'real chr22 comparison reproduces the documented difference'

echo 'INPUT 6 regression: reference dictionary M5 and pysam header facts'
python - "$DATA/toy.fa" <<'PY'
import hashlib, sys, pysam
fasta=sys.argv[1]
with pysam.FastaFile(fasta) as ref:
    assert list(ref.references) == ['chr1','chr2']
    assert ref.get_reference_length('chr1') == 120
for line in open(fasta.rsplit('.',1)[0]+'.dict', encoding='ascii'):
    if line.startswith('@SQ'):
        fields=dict(x.split(':',1) for x in line.rstrip().split('\t')[1:])
        with pysam.FastaFile(fasta) as ref:
            assert fields['M5'] == hashlib.md5(ref.fetch(fields['SN']).upper().encode()).hexdigest()
print('dict-and-pysam assertions passed')
PY

echo 'INPUT 7 regression: documented bgzip requirement and cache-safe failure'
gzip -c "$DATA/toy.fa" > "$DATA/plain.fa.gz"
set +e
bash "$ROOT/copied_skill/examples/prepare_reference.sh" "$DATA/plain.fa.gz" > input7_plain.log 2>&1
rc=$?
set -e
assert_eq "$rc" "1" 'plain gzip is rejected'
grep -qi 'bgzip' input7_plain.log
bgzip -c "$DATA/toy.fa" > "$DATA/bgzip.fa.gz"
bash "$ROOT/copied_skill/examples/prepare_reference.sh" "$DATA/bgzip.fa.gz" > input7_bgzip.log
assert_file "$DATA/bgzip.dict"

echo 'INPUT 8 regression: script error path leaves no final renamed BAM'
set +e
bash "$ROOT/copied_skill/scripts/rename_contigs.sh" "$DATA/toy.bam" absent.tsv broken.bam > input8.log 2>&1
rc=$?
set -e
assert_eq "$rc" "2" 'missing map exits with shell file error'
[ ! -e broken.bam ] || { echo 'ASSERT_FAIL: failed reheader left final output' >&2; exit 1; }

echo 'INPUT 9 fresh: invalid region and outside-window boundary behaviour'
set +e
python "$ROOT/copied_skill/scripts/pysam_consensus.py" consensus "$DATA/toy.bam" chr1 121 130 --min-depth 3 > input9.out 2> input9.err
rc=$?
set -e
assert_eq "0" "$rc" 'outside BAM window returns successfully'
assert_eq "NNNNNNNNN" "$(tr -d '\n' < input9.out)" 'outside BAM window returns an all-N sequence'

echo 'INPUT 10 fresh: no shell evaluation through a hostile reference filename'
HOSTILE="$DATA/odd;\$(touch SHOULD_NOT_EXIST).fa"
cp "$DATA/toy.fa" "$HOSTILE"
bash "$ROOT/copied_skill/examples/prepare_reference.sh" "$HOSTILE" > input10.log
[ ! -e SHOULD_NOT_EXIST ] || { echo 'ASSERT_FAIL: shell expansion occurred' >&2; exit 1; }
assert_file "$DATA/odd;\$(touch SHOULD_NOT_EXIST).dict"

echo 'ALL_ASSERTIONS_PASS 10 input classes'
