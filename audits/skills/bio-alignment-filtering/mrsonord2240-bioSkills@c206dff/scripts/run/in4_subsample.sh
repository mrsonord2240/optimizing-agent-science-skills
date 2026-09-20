#!/bin/bash
# Input 4: subsampling snippets, run literally as written in SKILL.md / usage-guide.md.
# usage: in4_subsample.sh <workdir>
set -u
W=$1; mkdir -p $W; cd $W
cp $AFDATA/1000g/HG00349.chr20_1400000-1500000.bam input.bam
cp $AFDATA/human/test.paired_end.sorted.bam normal.bam
cp input.bam tumor.bam
cnt() { samtools view -c "$1"; }
echo "full records: $(cnt input.bam)  distinct templates: $(samtools view input.bam | cut -f1 | sort -u | wc -l)"

echo "--- SKILL.md: 10% with seed 42 (twice)"
samtools view -s 42.1 -b -o subset.bam input.bam
samtools view -s 42.1 -b -o subset_b.bam input.bam
echo "subset records: $(cnt subset.bam)  identical rerun: $(cmp <(samtools view subset.bam) <(samtools view subset_b.bam) && echo yes)"

echo "--- SKILL.md/usage-guide claim: bare -s 0.1 is non-reproducible"
samtools view -s 0.1 -b -o bare1.bam input.bam
samtools view -s 0.1 -b -o bare2.bam input.bam
echo "bare -s 0.1 records: $(cnt bare1.bam) / $(cnt bare2.bam)  identical: $(cmp <(samtools view bare1.bam) <(samtools view bare2.bam) && echo yes || echo NO)"
echo "bare -s 0.1 vs -s 42.1 same reads? $(cmp -s <(samtools view bare1.bam) <(samtools view subset.bam) && echo yes || echo no)"

echo "--- SKILL.md: sequential cuts with INDEPENDENT seeds"
samtools view -s 1.5 -b input.bam > half1.bam
samtools view -s 2.25 -b half1.bam > quarter.bam
echo "half1=$(cnt half1.bam) quarter(seed2.25 of half1)=$(cnt quarter.bam) (12.5% of $(cnt input.bam) = $(( $(cnt input.bam) / 8 )))"
echo "--- SKILL.md: SAME seed nested claim (-s 1.5 then -s 1.25 -> 25% of original)"
samtools view -s 1.25 -b half1.bam > nested.bam
samtools view -s 1.25 -b input.bam > direct25.bam
echo "nested=$(cnt nested.bam) direct -s 1.25 on original=$(cnt direct25.bam) same reads: $(cmp -s <(samtools view nested.bam) <(samtools view direct25.bam) && echo yes || echo no)"

echo "--- SKILL.md: coverage-matching snippet, target < total (target=3000)"
total=$(samtools view -c -F 2304 input.bam)
target=3000
frac=$(awk -v t=$target -v n=$total 'BEGIN{printf "%.6f", t/n}')
echo "total(-F 2304)=$total target=$target frac=$frac -> -s 1.${frac#*.}"
samtools view -s "1.${frac#*.}" -b -o matched.bam input.bam
echo "matched records = $(cnt matched.bam)  (target $target)"
echo "--- same snippet, target > total (target=20000)"
target=20000
frac=$(awk -v t=$target -v n=$total 'BEGIN{printf "%.6f", t/n}')
echo "frac=$frac -> -s 1.${frac#*.}"
samtools view -s "1.${frac#*.}" -b -o matched_big.bam input.bam
echo "matched_big records = $(cnt matched_big.bam)  (input $(cnt input.bam); user wanted 20000 => keep-all)"

echo "--- SKILL.md: tumor-normal coverage matching (tumor=1000g slice, normal=human slice)"
normal_reads=$(samtools view -c -F 2308 normal.bam)
tumor_reads=$(samtools view -c -F 2308 tumor.bam)
if [ "$tumor_reads" -gt "$normal_reads" ]; then
    frac=$(awk -v n=$normal_reads -v t=$tumor_reads 'BEGIN{printf "%.6f", n/t}')
    samtools view -s "1.${frac#*.}" -b -o tumor_matched.bam tumor.bam
fi
echo "normal=$normal_reads tumor=$tumor_reads tumor_matched(-F 2308 count)=$(samtools view -c -F 2308 tumor_matched.bam) all=$(cnt tumor_matched.bam)"

echo "--- usage-guide.md: downsample-to-target snippet (bc), target 1000000"
total=$(samtools view -c input.bam)
frac=$(echo "scale=6; 1000000 / $total" | bc)
echo "total=$total frac='$frac' -> -s \"42${frac}\""
samtools view -s "42${frac}" -o subset_ug.bam input.bam
echo "usage-guide result records = $(cnt subset_ug.bam) of $total (wanted 1,000,000 => all)"
echo "--- usage-guide.md snippet with feasible target 2000"
frac=$(echo "scale=6; 2000 / $total" | bc)
echo "frac='$frac' -> -s \"42${frac}\""
samtools view -s "42${frac}" -o subset_ug2.bam input.bam
echo "records = $(cnt subset_ug2.bam) (target 2000)"
echo "--- usage-guide 'samtools view -s 42.1 -o subset.bam' (no -b) is BAM? magic:"
samtools view -s 42.1 -o ug_nob.bam input.bam; head -c 2 ug_nob.bam | xxd -p
