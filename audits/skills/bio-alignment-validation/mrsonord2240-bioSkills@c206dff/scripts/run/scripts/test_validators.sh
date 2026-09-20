#!/bin/bash
# The two "comprehensive" validators (SKILL.md 'Comprehensive Validation Script' = SKILL_19, shipped examples/*.sh and *.py):
# run on good, edge and broken inputs; judge by what they print AND by what a pipeline would see (exit status).
RUN=/mnt/openscience/audits/bio-alignment-validation/run
PD=/mnt/openscience/audit-envs/alignment-files/public-data
I=$RUN/data/idx
D=$RUN/data
W=$RUN/out/work2; rm -rf $W; mkdir -p $W; cd $W
cp $RUN/snip/SKILL_19_bash.txt $W/comprehensive.sh       # verbatim copy of the SKILL.md script
SH=$RUN/skill/examples/validate_alignment.sh
PY=$RUN/skill/examples/validate_alignment.py
REF=$PD/human/genome.fasta
samtools view -b -f 4 $I/real_human_PE.bam > $W/all_unmapped.bam 2>/dev/null; samtools index $W/all_unmapped.bam 2>/dev/null
echo "all_unmapped.bam: $(samtools view -c $W/all_unmapped.bam) records (SYNTHETIC: the 2 unmapped reads of the real human BAM, header kept)"

run_comp() { # label bam
  rm -rf $W/qc_$1; bash $W/comprehensive.sh $2 $REF $W/qc_$1 > $W/comp_$1.out 2> $W/comp_$1.err; rc=$?
  echo "  [$1] rc=$rc | report lines=$(wc -l < $W/qc_$1/report.txt 2>/dev/null) | stderr lines=$(grep -c . $W/comp_$1.err) | pass/warn/fail words in report: $(grep -ciE 'pass|warn|fail' $W/qc_$1/report.txt 2>/dev/null)"
  grep -E 'Mapping rate|Proper pairing:|Forward:' $W/comp_$1.out | sed 's/^/      /'
  head -2 $W/comp_$1.err | cut -c1-150 | sed 's/^/      ERR: /'
}
echo "=========== V1 SKILL_19 comprehensive script (verbatim) ==========="
run_comp humanPE $I/real_human_PE.bam
run_comp rna $I/real_human_RNA.bam
run_comp se $I/real_sars_SE.bam
run_comp lowmap_unplaced $I/planted_lowmap_unplaced.bam
run_comp lowmap_placed $I/planted_lowmap_placed.bam
run_comp empty $D/empty_records.bam
run_comp missing /nonexistent.bam
run_comp trunc $D/trunc_tail.bam
echo "  truth for the two low-map fixtures: mapped 70.0%"

echo "=========== V2 shipped validate_alignment.sh ==========="
for pair in "humanPE $I/real_human_PE.bam" "se $I/real_sars_SE.bam" "empty $D/empty_records.bam" "missing /nonexistent.bam" "trunc $D/trunc_tail.bam" "lowmap_unplaced $I/planted_lowmap_unplaced.bam"; do
  set -- $pair
  bash $SH $2 > $W/sh_$1.out 2> $W/sh_$1.err; rc=$?
  echo "  [$1] rc=$rc | Mapped line: $(grep '^Mapped' $W/sh_$1.out | head -1) | stderr lines: $(grep -c . $W/sh_$1.err) | first err: $(head -1 $W/sh_$1.err | cut -c1-110)"
done

echo "=========== V3 shipped validate_alignment.py, edge inputs ==========="
for pair in "se $I/real_sars_SE.bam" "nanopore $I/real_sars_nanopore.bam" "empty $I/planted_empty_records.bam" "all_unmapped $W/all_unmapped.bam" "missing /nonexistent.bam" "rna $I/real_human_RNA.bam"; do
  set -- $pair
  python $PY $2 > $W/py_$1.out 2> $W/py_$1.err; rc=$?
  echo "  [$1] rc=$rc | verdict: $(grep -E 'WARNINGS|All metrics' $W/py_$1.out | head -1) | last stderr: $(tail -1 $W/py_$1.err | cut -c1-110)"
done

echo "=========== V4 does a failing QC stop a pipeline? (python validator on the 70%-mapped fixture) ==========="
python $PY $I/planted_lowmap_placed.bam > $W/v4.out 2>&1 && echo "  PIPELINE CONTINUES (rc=0) although: $(grep -E 'WARNINGS' $W/v4.out)"
bash $SH $I/planted_lowmap_placed.bam > $W/v4b.out 2>&1 && echo "  shell validator rc=0; it prints no verdict at all: pass/warn/fail words = $(grep -ciE 'pass|warn|fail' $W/v4b.out)"

echo "=========== V5 SKILL 'Comprehensive validation' vs its own stated Approach ==========="
echo "  Approach text: 'outputs pass/warn/fail calls'; count of pass/warn/fail in script body: $(grep -ciE 'pass|warn|fail' $W/comprehensive.sh)"
