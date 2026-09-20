#!/bin/bash
# hmmscan on ISAR AA fasta with the pressed Pfam-A copied to WSL tmpfs (9p reads made each query cost ~40 s of sys time)
AS=/mnt/openscience/audit-envs/alternative-splicing
W=/mnt/openscience/audits/bio-isoform-switching/run/work/annot
SEQ=/mnt/openscience/audits/bio-isoform-switching/run/work/sequences
mkdir -p /tmp/pf; for e in h3f h3i h3m h3p; do cp $AS/public-data/reference_dbs/Pfam-A.hmm.$e /tmp/pf/; done
head -c 1000000 $AS/public-data/reference_dbs/Pfam-A.hmm > /tmp/pf/Pfam-A.hmm   # stub head so the base file exists; pressed files carry the models
cd $W
time micromamba run -n as-annot hmmscan --cpu 8 --cut_ga --domtblout pfam_domtbl.txt -o hmmscan_stdout.txt /tmp/pf/Pfam-A.hmm $SEQ/isoformSwitchAnalyzeR_isoform_AA.fasta; echo "hmmscan rc=$?"
grep -v '^#' pfam_domtbl.txt | awk '{print $1, $2, $4, $7}' | sort -k3 | head -40
echo "domain hits: $(grep -vc '^#' pfam_domtbl.txt)"
