#!/bin/bash
# Git Bash on Windows. Set-up commands run once before the tests (recorded here because they only existed as tool calls).
# 1. clean run dir, copy the FIXED Skill (read-only worktree F:\OpenScience\wt\af-refops, commit 0d22089) into run/skill
# 2. copy the real public data used by the tests from the alignment-files env (public-data is never written to)
# 3. reuse the pre-fix audit's SYNTHETIC 3-contig reference/BAM (data/synthetic; built by its make_synth.py) for the regression input 2
# 4. fetch the public reference tables used to spot-check the SKILL tables (all unauthenticated)
set -e
AUD=/f/OpenScience/audits/bio-reference-operations
cd $AUD && rm -rf run && mkdir -p run/data/real run/data/synthetic run/ncbi run/logs
cp -r /f/OpenScience/wt/af-refops/alignment-files/reference-operations run/skill        # commit 0d22089b40e9195801f3980b64fcbb24ed4e278f
A=/f/OpenScience/audit-envs/alignment-files/public-data
P=/f/OpenScience/audits/_pre-fix-20260920/bio-reference-operations/run
cp -r $P/data/synthetic/* run/data/synthetic/
cp $A/human/genome.fasta $A/human/genome.fasta.fai $A/human/test.paired_end.sorted.bam $A/human/test.paired_end.sorted.bam.bai $A/human/test.paired_end.sorted.cram run/data/real/
mkdir -p run/data/real/sars run/data/real/g1000
cp $A/sarscov2/MN908947.3.fasta $A/sarscov2/test.paired_end.sorted.bam $A/sarscov2/genome.fasta $A/sarscov2/sars-cov-2_v5.3.2.nanopore.bam run/data/real/sars/
cp $A/1000g/HG00349*.bam* $A/1000g/chr20_padded_1500000.fa $A/1000g/chr20_1400001-1500000.seq.txt run/data/real/g1000/
cp $P/ncbi/{1kg.fai,GRCh38_report.txt,README_1000G.txt,genomic_fna_head.txt,SOURCES.txt} run/ncbi/       # fetched 2026-09-20 by the first audit (NCBI assembly report, 1000G fai/README)
cd run/ncbi
c(){ curl -sSL --max-time 120 -o "$1" "$2" && echo "$1 $(wc -c <"$1")" || echo "FAIL $1"; }
c hg38.chrom.sizes https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.chrom.sizes
c hg19.chrom.sizes https://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/hg19.chrom.sizes
c README_analysis_sets.txt https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/README_analysis_sets.txt
c broad38.fai https://storage.googleapis.com/gcp-public-data--broad-references/hg38/v0/Homo_sapiens_assembly38.fasta.fai
c hs37d5.fai https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz.fai
c ens_info.json "https://rest.ensembl.org/info/assembly/homo_sapiens?content-type=application/json"
c GRCh37_report.txt https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.25_GRCh37.p13/GCF_000001405.25_GRCh37.p13_assembly_report.txt
c samtools_NEWS.md https://raw.githubusercontent.com/samtools/samtools/develop/NEWS.md       # version notes: -T in 1.22, instrument --config in 1.17, -aa in 1.18
# then, inside WSL (wsl_run.sh): python extract_snippets.py skill snippets ; h1_help.sh ; make_planted.py data/planted ; the r*.py / r*.sh tests
