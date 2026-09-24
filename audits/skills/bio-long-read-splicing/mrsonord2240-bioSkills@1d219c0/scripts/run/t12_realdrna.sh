#!/bin/bash
# REAL ONT direct RNA (SG-NEx A549 replicate5 run1, chr9:1-1e6; from the bambu package extdata): BAM -> FASTQ (samtools fastq restores read orientation),
# then the shipped example with PLATFORM=drna from a clean copy. Real annotation = Ensembl 91 GTF (gene/transcript/exon/CDS/UTR/codon rows), contig "9".
R=/mnt/openscience/audits/bio-long-read-splicing/run; P=/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/bambu_extdata
O=$R/out/ex_realdrna; rm -rf $O; mkdir -p $O; cd $O; export PYTHONDONTWRITEBYTECODE=1
cp $P/Homo_sapiens.GRCh38.dna_sm.primary_assembly_chr9_1_1000000.fa reference.fa; cp $P/Homo_sapiens.GRCh38.91_chr9_1_1000000.gtf annotation.gtf
samtools fastq -F 0x900 $P/SGNex_A549_directRNA_replicate5_run1_chr9_1_1000000.bam 2>/dev/null | gzip > a549.fastq.gz
echo "reads in fastq: $(( $(zcat a549.fastq.gz | wc -l) / 4 ))  ; BAM primary reads: $(samtools view -c -F 0x904 $P/SGNex_A549_directRNA_replicate5_run1_chr9_1_1000000.bam)"
cut -f3 annotation.gtf | grep -v '^#' | sort | uniq -c | sort -rn | head -8 | tr '\n' ' '; echo
PLATFORM=drna REFERENCE=reference.fa GTF=annotation.gtf FASTQ=a549.fastq.gz SAMPLE=a549 THREADS=8 OUTPUT_DIR=$O/out bash $R/skill_copy/examples/longread_splicing_pipeline.sh > example.log 2>&1
echo "example exit code: $?"; tail -6 example.log | cut -c1-200
cd out
echo "--- content checks"
echo "aligned primary mapped reads: $(samtools view -c -F 0x904 a549_aligned.bam), spliced (N in CIGAR): $(samtools view -F 0x904 a549_aligned.bam | awk '$6 ~ /N/' | wc -l)"
echo "IsoQuant transcript models: $(awk '$3=="transcript"' isoquant/a549/a549.transcript_models.gtf | wc -l) ; rows by type in IsoQuant GTF: $(cut -f3 isoquant/a549/a549.transcript_models.gtf | grep -v '^#' | sort | uniq -c | tr '\n' ' ')"
echo "IsoQuant reads counted to transcripts: $(awk 'NR>1 && $1 !~ /^__/ {s+=$2} END{print s}' isoquant/a549/a549.transcript_counts.tsv) ; __ rows: $(grep '^__' isoquant/a549/a549.transcript_counts.tsv | tr '\n' ' ')"
echo "FLAIR isoforms: $(grep -c '>' flair_collapsed_a549.isoforms.fa) ; corrected reads $(wc -l < flair_corrected_a549_all_corrected.bed) inconsistent $(wc -l < flair_corrected_a549_all_inconsistent.bed)"
python3 - <<'PY'
import csv, collections
r = list(csv.DictReader(open("sqanti3/sqanti3_classification.txt"), delimiter="\t"))
print("SQANTI3 rows", len(r), dict(collections.Counter(x["structural_category"] for x in r)))
PY
echo "filter: pass $(wc -l < sqanti3_filtered/sqanti3_filtered_pass_isoforms.txt), filtered.gtf $(wc -l < sqanti3_filtered/sqanti3_filtered.filtered.gtf)"
