#!/bin/bash
# Input 3 (Edge): (a) every cell of the SKILL's synthetic 4x4 outcome table, (b) BED-format handling: the SKILL's own BED example,
# 5-column error, 7-column ARTIC, and BED variants a real user brings (space-delimited, track header, CRLF, blank lines) through
# samtools directly AND through the shipped example (false-positive check of the example's new hard-fail checks),
# (c) what --tolerance means. All data SYNTHETIC (data/).
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; D=$R/data; W=$R/out/i3; rm -rf $W; mkdir -p $W; cd $W
cp -r $R/skill $W/skillcopy; EX=$W/skillcopy/examples/ampliconclip_workflow.sh; CK=$W/skillcopy/examples/check_primer_residual.py
echo "=== (a) SKILL 4x4 table"
for spec in "default:" "strand:--strand" "both:--both-ends" "both_strand:--both-ends --strand"; do
  tag=${spec%%:*}; flags=${spec#*:}
  samtools ampliconclip $flags -b $D/synth_primers.bed $D/strand_cases.bam 2>/dev/null | samtools view - | awk '{print $1"\t"$2"\t"$4"\t"$6}' | sort > $tag.tsv
done
samtools view $D/strand_cases.bam | awk '{print $1"\t"$2"\t"$4":"$6}' | sort > orig.tsv
python $R/s3_table_assert.py
echo "--- SKILL prose: 'primers + [300,325) and - [325,350)' -> synth_primers.bed rows for that region:"; awk '$2>=300 && $3<=350' $D/synth_primers.bed

echo "=== (b) BED formats"
echo "-- SKILL.md BED example block, extracted verbatim:"
python - <<'PY'
import re
t = open("/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/skill/SKILL.md", encoding="utf-8").read()
i = t.index("## Primer BED Format"); m = re.search(r"```\n((?:.|\n)*?)```", t[i:])
open("skill_bed_example.bed", "w", newline="\n").write(m.group(1).replace("   ", "\t"))   # doc shows aligned columns; tabs are what BED needs
print(m.group(1))
PY
echo "(columns tab-separated for the run):"; cat -A skill_bed_example.bed | head -3
echo "-- samtools --strand with the SKILL BED example (contig chr1 not in the BAM):"
samtools ampliconclip --strand -b skill_bed_example.bed $D/synth_pe.bam -o /dev/null 2>&1 | head -4 | cut -c1-160; echo "   rc=${PIPESTATUS[0]}"
echo "-- 5-column BED with --strand (strand moved to column 5):"
awk 'BEGIN{OFS="\t"}{print $1,$2,$3,$4,$6}' $D/synth_primers.bed > b5.bed
samtools ampliconclip --strand -b b5.bed $D/synth_pe.bam -o /dev/null 2>&1 | head -3 | cut -c1-160; echo "   rc=${PIPESTATUS[0]}"
echo "-- 5-column BED WITHOUT --strand (should work):"
samtools ampliconclip -b b5.bed $D/synth_pe.bam -o /dev/null 2>&1 | grep -E 'TOTAL CLIPPED|rror'
echo "-- shipped example with the 5-column BED (default CLIP_OPTS has --strand):"
bash $EX $D/synth_pe.bam b5.bed $D/synth.fa $W/x5.bam > x5.out 2>&1; echo "   example rc=$?: $(tail -1 x5.out | cut -c1-160)"
echo "-- shipped example, 5-col BED, CLIP_OPTS=--both-ends (no --strand, so legitimate):"
CLIP_OPTS=--both-ends bash $EX $D/synth_pe.bam b5.bed $D/synth.fa $W/x5b.bam > x5b.out 2>&1; echo "   example rc=$?: $(tail -3 x5b.out | cut -c1-200 | tr '\n' '|')"
echo "   (checker needs 6 cols even then)"

echo "=== BED variants (legitimate inputs? does samtools accept them, and does the example)"
cp $D/synth_primers.bed v_tab.bed
sed 's/\t/ /g' $D/synth_primers.bed > v_space.bed
{ printf 'track name=primers description="amplicon primers"\n'; cat $D/synth_primers.bed; } > v_track.bed
{ printf 'browser position amp1:1-3000\n'; printf 'track name=primers\n'; cat $D/synth_primers.bed; } > v_browser_track.bed
sed 's/$/\r/' $D/synth_primers.bed > v_crlf.bed
{ cat $D/synth_primers.bed; printf '\n\n'; } > v_blank.bed
{ printf '# comment line\n'; cat $D/synth_primers.bed; } > v_comment.bed
for v in tab space track browser_track crlf blank comment; do
  echo "--- v_$v.bed"
  s=$(samtools ampliconclip --both-ends --strand -b v_$v.bed $D/synth_pe.bam -o /dev/null 2>&1 | grep -E 'TOTAL CLIPPED|rror|nvalid' | head -2 | tr '\n' ' ')
  echo "   samtools --both-ends --strand: $s"
  bash $EX $D/synth_pe.bam v_$v.bed $D/synth.fa $W/v_$v.bam > v_$v.out 2>&1; rc=$?
  echo "   example rc=$rc: $(grep -E 'ERROR|Error|rror|Clipped BAM|TOTAL CLIPPED' v_$v.out | head -2 | cut -c1-170 | tr '\n' '|')"
  python $CK $D/synth_pe.bam v_$v.bed --three-prime > ck_$v.out 2>&1; echo "   checker rc=$?: $(head -1 ck_$v.out | cut -c1-150)"
done

echo "=== (c) --tolerance semantics (fwd 60-bp reads starting at 300+d; '+' primer [300,325); 0-based)"
python $R/s3_tol_make.py
for t in 0 5 10; do
  samtools ampliconclip --tolerance $t -b $D/synth_primers.bed $D/tol_cases.bam 2>/dev/null | samtools view - | awk '{printf "%s:%s ", $1,($6 ~ /S/ ? "clip" : "-")}' > tol_$t.txt
  echo "tol=$t: $(cat tol_$t.txt)"
done
echo "default tolerance from help: $(samtools ampliconclip 2>&1 | grep -i -A1 tolerance | tr '\n' ' ' | cut -c1-200)"
