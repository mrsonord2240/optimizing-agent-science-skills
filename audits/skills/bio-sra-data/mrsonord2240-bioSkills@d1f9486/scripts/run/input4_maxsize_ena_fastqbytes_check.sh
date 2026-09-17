#!/bin/bash
# Edge input regression: ENA fastq_bytes path (live, works). pysradb total_size path
# blocked today by a live NCBI eutils backend outage (HTTP 500 from esearch.fcgi/efetch.fcgi,
# confirmed 3x across eutils101/102/201) -- see input9 for the static source-code
# confirmation used in its place.
SRR="${1:-ERR10015134}"
curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=${SRR}&result=read_run&fields=fastq_bytes&format=tsv"
