#!/bin/bash
# The SHIPPED example (clean copy) with PLATFORM=ont on REAL LRGASP WTC-11 cDNA reads (FLAIR test set, 1883 reads, hg38 chr12/17/20), without and with SR_JUNCTIONS (real short-read junctions).
R=/mnt/openscience/audits/bio-long-read-splicing/run; P=/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/flair_test
export PYTHONDONTWRITEBYTECODE=1
for V in nosj sj; do
  O=$R/out/ex_realont_$V; rm -rf $O; mkdir -p $O; cd $O
  cp $P/genome.fa reference.fa; cp $P/input/basic.annotation.gtf annotation.gtf; gzip -c $P/input/basic.reads.fa > reads.fa.gz
  if [ $V = sj ]; then export SR_JUNCTIONS=$P/input/basic.shortread_junctions.tab; else unset SR_JUNCTIONS; fi
  PLATFORM=ont REFERENCE=reference.fa GTF=annotation.gtf FASTQ=reads.fa.gz SAMPLE=lrgasp THREADS=8 OUTPUT_DIR=$O/out bash $R/skill_copy/examples/longread_splicing_pipeline.sh > example.log 2>&1
  echo "== real ONT cDNA, $V: example exit code $?"; grep -a -E "ts:A:\+|intron next to a soft clip" example.log
  cd out
  echo "IsoQuant models: $(awk '$3=="transcript"' isoquant/lrgasp/lrgasp.transcript_models.gtf | wc -l); counted to annotated transcripts: $(awk 'NR>1 && $1 !~ /^__/ {s+=$2} END{print s}' isoquant/lrgasp/lrgasp.transcript_counts.tsv); __ rows: $(grep '^__' isoquant/lrgasp/lrgasp.transcript_counts.tsv | tr '\t\n' '= ')"
  echo "FLAIR isoforms: $(grep -c '>' flair_collapsed_lrgasp.isoforms.fa); corrected $(wc -l < flair_corrected_lrgasp_all_corrected.bed) inconsistent $(wc -l < flair_corrected_lrgasp_all_inconsistent.bed)"
  python3 - <<'PY'
import csv, collections
r = list(csv.DictReader(open("sqanti3/sqanti3_classification.txt"), delimiter="\t"))
print("SQANTI3 rows", len(r), dict(collections.Counter(x["structural_category"] for x in r)))
PY
  echo "filter: pass $(wc -l < sqanti3_filtered/sqanti3_filtered_pass_isoforms.txt), filtered.gtf $(wc -l < sqanti3_filtered/sqanti3_filtered.filtered.gtf)"
done
