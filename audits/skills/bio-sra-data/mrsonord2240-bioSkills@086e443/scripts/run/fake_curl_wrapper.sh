#!/bin/bash
# Fake curl wrapper for regression testing: intercepts specific synthetic accessions
# and returns crafted ENA filereport TSV; passes everything else through to real curl.
REAL_CURL="/mingw64/bin/curl"
ARGS="$*"

if [[ "${ARGS}" == *"accession=CONTROLLEDTEST1"* ]]; then
    # Independently-built fixture: based on ERR10419972's REAL TSV shape
    # (run_accession, fastq_ftp, fastq_md5, read_count -- 4 real columns, captured live),
    # with fastq_ftp entirely stripped, exactly as ENA does for a controlled-access run.
    printf 'run_accession\tfastq_md5\tread_count\nCONTROLLEDTEST1\t0976d39fb1c22e0c8005bb85dc743895;a8cf684044728c175d7ae8f27198249a\t20898\n'
    exit 0
elif [[ "${ARGS}" == *"accession=CONTROLLEDTEST2"* ]]; then
    # Reverse case: fastq_ftp present, fastq_md5 genuinely absent (not tested by the fixer).
    printf 'run_accession\tfastq_ftp\tread_count\nCONTROLLEDTEST2\tftp.sra.ebi.ac.uk/vol1/fastq/ERR104/072/ERR10419972/ERR10419972_1.fastq.gz;ftp.sra.ebi.ac.uk/vol1/fastq/ERR104/072/ERR10419972/ERR10419972_2.fastq.gz\t20898\n'
    exit 0
elif [[ "${ARGS}" == *"accession=EMPTYRESP1"* ]]; then
    # Malformed/empty response: server returns nothing at all (e.g. transient ENA hiccup
    # or a totally invalid accession that doesn't even get a header row back).
    printf ''
    exit 0
else
    exec "${REAL_CURL}" "$@"
fi
