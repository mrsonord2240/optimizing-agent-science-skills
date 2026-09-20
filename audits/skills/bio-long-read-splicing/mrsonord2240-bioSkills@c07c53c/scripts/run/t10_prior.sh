#!/bin/bash
# REGRESSION legs re-run on the FIRST auditor's data (archived in _pre-fix-20260920): (a) fixer's 10-nt chrM microexon set with a skip-read control,
# (b) shipped example on the old synthetic reads, scored with the first auditor's junction_check.py, (c) SQANTI3 block on the 10 planted query isoforms with known categories.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/prior; B=$R/out/blocks; O=$R/out/prior; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
echo "########## (a) 10-nt microexon (fixer's set, 150 inc + 150 skip): inclusion kept / skip exact"
for P in hifi ont; do
  FQ=$D/synth_micro/$P.fastq; if [ $P = hifi ]; then PRE="splice:hq"; else PRE="splice -k14"; fi
  for V in "plain|" "juncbed|--junc-bed $D/synth_micro/ref.bed12" "juncbed+bonus20|--junc-bed $D/synth_micro/ref.bed12 --junc-bonus 20"; do
    N=${V%%|*}; A=${V#*|}
    minimap2 -ax $PRE --secondary=no $A -t 8 $D/synth_micro/chrM.fa $FQ 2>/dev/null | samtools sort -o t.bam - 2>/dev/null; samtools index t.bam
    asenv as-lr python $R/micro_table.py t.bam $D/synth_micro/truth_chains.tsv "prior10nt $P $N"
  done
done
echo "########## (b) shipped example, first auditor's synthetic reads (annotation has no gene/CDS rows), PLATFORM=hifi and ont"
for PL in hifi ont; do
  if [ $PL = hifi ]; then FQ=$D/synth/hifi/ctrl1.fastq; else FQ=$D/synth/ontunstr/ctrl1.fastq; fi
  mkdir -p ex_$PL; ( cd ex_$PL; cp $D/synth/chrS1.fa reference.fa; cp $D/synth/ref.gtf annotation.gtf; gzip -c $FQ > s.fastq.gz
    PLATFORM=$PL REFERENCE=reference.fa GTF=annotation.gtf FASTQ=s.fastq.gz SAMPLE=s THREADS=6 OUTPUT_DIR=$PWD/out bash $R/skill_copy/examples/longread_splicing_pipeline.sh > example.log 2>&1; echo "example PLATFORM=$PL exit code $?"
    asenv as-lr python $R/prior_junction_check.py out/s_aligned.bam $D/synth/read_tx.gtf "prior-data example PLATFORM=$PL" | tail -6
    echo "  filtered.gtf lines: $(wc -l < out/sqanti3_filtered/sqanti3_filtered.filtered.gtf)  pass isoforms: $(wc -l < out/sqanti3_filtered/sqanti3_filtered_pass_isoforms.txt)" ); done
echo "########## (c) SQANTI3 block (verbatim, minus the 2 optional CAGE/polyA lines) on the first auditor's 10 planted query isoforms"
mkdir -p sq; cd sq; cp $D/synth/chrS1.fa reference.fa; cp $D/synth/ref.gtf gencode.v45.annotation.gtf; cp $D/synth/query_isoforms.gtf isoforms.gtf
grep -v -E "CAGE_peak|polyA_motif_list" $B/sqanti3-classification_1.sh > sq_block.sh
cat sq_block.sh
bash sq_block.sh > sq.log 2>&1; echo "rc=$?"; grep -a -i -E "Traceback|ERROR" sq.log | head -3
cut -f1,8 sqanti3_qc/sqanti3_classification.txt | column -t > got.txt; cat got.txt; echo "--- expected:"; cat $D/synth/query_truth.tsv
python3 - <<'PY'
import csv
exp = {r["isoform"]: r["expected_category"] for r in csv.DictReader(open("/mnt/openscience/audits/bio-long-read-splicing/run/data/prior/synth/query_truth.tsv"), delimiter="\t")}
got = {r["isoform"]: r["structural_category"] for r in csv.DictReader(open("sqanti3_qc/sqanti3_classification.txt"), delimiter="\t")}
ok = sum(1 for k, v in exp.items() if got.get(k) == v)
print("SQANTI3 categories matching the planted truth: %d/%d" % (ok, len(exp)), {k: (v, got.get(k)) for k, v in exp.items() if got.get(k) != v})
PY
wc -l sqanti3_filtered/*pass_isoforms.txt sqanti3_filtered/sqanti3_filtered.filtered.gtf 2>&1 | head
