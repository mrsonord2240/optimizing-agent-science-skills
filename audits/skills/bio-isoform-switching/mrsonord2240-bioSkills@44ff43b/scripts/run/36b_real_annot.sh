#!/bin/bash
# CPC2 + hmmscan on the ISAR-extracted sequences of the REAL chrX switching genes
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
W=/mnt/openscience/audits/bio-isoform-switching/run/work/annot_real; rm -rf $W; mkdir -p $W
SEQ=/mnt/openscience/audits/bio-isoform-switching/run/work/seq_real
[ -d /tmp/CPC2_isw/libs/libsvm/libsvm-3.18 ] || { rm -rf /tmp/CPC2_isw; cp -r $AS/tools/src/CPC2_standalone /tmp/CPC2_isw; cd /tmp/CPC2_isw/libs/libsvm; tar zxf libsvm-3.18.tar.gz; cd libsvm-3.18; make clean > /dev/null 2>&1; make > $W/libsvm.log 2>&1; }
[ -f /tmp/pf/Pfam-A.hmm.h3m ] || { mkdir -p /tmp/pf; for e in h3f h3i h3m h3p; do cp $AS/public-data/reference_dbs/Pfam-A.hmm.$e /tmp/pf/; done; head -c 1000000 $AS/public-data/reference_dbs/Pfam-A.hmm > /tmp/pf/Pfam-A.hmm; }
cd $W
micromamba run -n as-cpc2 python /tmp/CPC2_isw/bin/CPC2.py -i $SEQ/isoformSwitchAnalyzeR_isoform_nt.fasta -o cpc2_result > cpc2.log 2>&1; echo "CPC2 rc=$?"; awk 'NR>1{c[$NF]++} END{for(k in c) print k, c[k]}' cpc2_result.txt
micromamba run -n as-annot hmmscan --cpu 8 --cut_ga --domtblout pfam_domtbl.txt -o hmmscan_stdout.txt /tmp/pf/Pfam-A.hmm $SEQ/isoformSwitchAnalyzeR_isoform_AA.fasta; echo "hmmscan rc=$?"
echo "domain rows: $(grep -vc '^#' pfam_domtbl.txt); sequences: $(grep -c '>' $SEQ/isoformSwitchAnalyzeR_isoform_AA.fasta)"
