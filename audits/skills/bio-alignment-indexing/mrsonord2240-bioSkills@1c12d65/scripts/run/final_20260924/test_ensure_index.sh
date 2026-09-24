#!/usr/bin/env bash
# Exercise the final-pass documented ensure_index implementation on real audit fixtures.
set -euo pipefail
ROOT=/mnt/openscience/audits/bio-alignment-indexing/run/final_20260924
DATA=/mnt/openscience/audit-envs/alignment-files/public-data/human
WORK="$ROOT/work/ensure"
rm -rf "$WORK"
mkdir -p "$WORK/empty"

ensure_index() {   # ensure_index file.bam|file.cram [extra samtools-index options, e.g. -@ 4]
    local f=$1; shift
    local stem=${f%.*} idx have=0 stale=0 csi=0 min_shift=14
    local -a candidates
    case $f in
        *.bam)  candidates=("$f.csi" "$stem.csi" "$f.bai" "$stem.bai") ;;
        *.cram) candidates=("$f.crai" "$stem.crai") ;;
        *) printf 'Expected a .bam or .cram file: %s\n' "$f" >&2; return 2 ;;
    esac
    for idx in "${candidates[@]}"; do
        [ -e "$idx" ] || continue
        have=1
        [ "$f" -nt "$idx" ] && stale=1
        case $idx in
            *.csi) csi=1
                    min_shift=$(bgzip -cd "$idx" | od -An -j4 -N4 -tu4 | tr -d '[:space:]')
                    [ -n "$min_shift" ] || min_shift=14 ;;
        esac
    done
    if [ $have = 0 ] || [ $stale = 1 ]; then
        rm -f "${candidates[@]}"
        if [ $csi = 1 ]; then
            samtools index -c -m "$min_shift" "$@" "$f"
        else
            samtools index "$@" "$f"
        fi
    fi
}

cp "$DATA/test.paired_end.sorted.bam" "$WORK/sample.bam"
samtools index -c -m 12 "$WORK/sample.bam"
sleep 1
touch "$WORK/sample.bam"
ensure_index "$WORK/sample.bam"
test -f "$WORK/sample.bam.csi"
test ! -e "$WORK/sample.bam.bai"
test "$(bgzip -cd "$WORK/sample.bam.csi" | od -An -j4 -N4 -tu4 | tr -d '[:space:]')" = 12
test "$(samtools view -c "$WORK/sample.bam" chr22:1952-4700)" = 5642

cp "$DATA/test.paired_end.sorted.cram" "$WORK/sample.cram"
samtools index "$WORK/sample.bam" "$WORK/sample.bai"
ensure_index "$WORK/sample.cram"
test -f "$WORK/sample.bai"
test -f "$WORK/sample.cram.crai"
ensure_index "$WORK/sample.bam"
test -f "$WORK/sample.cram.crai"

(cd "$WORK/empty" && shopt -s nullglob && for f in *.bam; do ensure_index "$f"; done)
printf 'PASS CSI min_shift=12 preserved; BAM/CRAM sibling indices retained; empty batch is a no-op\n'
