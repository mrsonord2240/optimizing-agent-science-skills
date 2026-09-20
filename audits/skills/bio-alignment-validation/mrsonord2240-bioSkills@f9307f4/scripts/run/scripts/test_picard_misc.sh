#!/bin/bash
# Picard claims in the fixed SKILL.md: (1) IGNORE recipe effect, (2) noise on valid files, (3) R dependency of chart outputs.
RUN=/mnt/openscience/audits/bio-alignment-validation/run; PD=/mnt/openscience/audit-envs/alignment-files/public-data
D=$RUN/data; REF=$PD/human/genome.fasta; W=$RUN/out/work_pm; rm -rf $W; mkdir -p $W; cd $W
sumry() { picard ValidateSamFile I=$1 MODE=SUMMARY $2 $3 $4 $5 2>&1 | grep -E '^(ERROR|WARNING):[A-Z_]+[[:space:]]+[0-9]+|No errors found|Exception' | grep -v 'NM validation' | tr '\n' ';' | cut -c1-260; echo; }
echo "== (1) IGNORE recipe on planted files"
for f in flag_mate_neg_strand unmapped_mapq60 strand_all_forward; do
  echo "  $f plain : $(sumry $D/$f.bam R=$REF)"
  echo "  $f IGNORE=INVALID_MAPPING_QUALITY IGNORE=MISMATCH_FLAG_MATE_NEG_STRAND : $(sumry $D/$f.bam R=$REF IGNORE=INVALID_MAPPING_QUALITY IGNORE=MISMATCH_FLAG_MATE_NEG_STRAND)"
done
echo "== (2) Picard on the real valid files that it flags"
echo "  name-sorted : $(sumry $PD/human/test.paired_end.name.sorted.bam R=$REF)"
echo "  RNA         : $(sumry $PD/human/test.rna.paired_end.sorted.bam R=$REF)"
echo "  1000G slice : $(sumry $PD/1000g/HG00349.chr20_1400000-1500000.bam)"
echo "  nanopore    : $(sumry $PD/sarscov2/sars-cov-2_v5.3.2.nanopore.bam R=$PD/sarscov2/MN908947.3.fasta)"
echo "== (3) chart outputs need R: strip every PATH dir that has Rscript"
NOR=$(echo "$PATH" | tr ':' '\n' | while read p; do [ -x "$p/Rscript" ] || echo "$p"; done | paste -sd:)
echo "  Rscript visible with stripped PATH: '$(env PATH="$NOR" which Rscript 2>&1 | head -1)'; with normal PATH: '$(which Rscript | head -1)'"
H=$PD/human/test.paired_end.sorted.bam
rm -f m1.txt h1.pdf; env PATH="$NOR" picard CollectInsertSizeMetrics I=$H O=m1.txt H=h1.pdf > p1.log 2>&1; echo "  --- InsertSize no-R log tail:"; grep -a -v -E '^\*|setlocale|restricted|^$' p1.log | tail -4 | cut -c1-200
echo "  InsertSize with H=, no R : rc=$? metrics file exists: $([ -s m1.txt ] && echo yes || echo NO) pdf: $([ -s h1.pdf ] && echo yes || echo NO) | $(grep -E 'Exception|ERROR' p1.log | head -2 | cut -c1-160 | tr '\n' ';')"
rm -f m2.txt; env PATH="$NOR" picard CollectInsertSizeMetrics I=$H O=m2.txt H=h2.pdf > p2.log 2>&1; 
rm -f g1.txt g1s.txt g1.pdf; env PATH="$NOR" picard CollectGcBiasMetrics I=$H O=g1.txt CHART=g1.pdf S=g1s.txt R=$REF > p3.log 2>&1; echo "  GcBias with CHART=, no R : rc=$? metrics: $([ -s g1.txt ] && echo yes || echo NO) summary: $([ -s g1s.txt ] && echo yes || echo NO) | $(grep -E 'Exception|ERROR' p3.log | head -2 | cut -c1-160 | tr '\n' ';')"
echo "  SKILL.md text about R for these commands: $(grep -c -i 'rscript\|requires R\|needs R' $RUN/skill/SKILL.md) mentions"
echo "== done"
