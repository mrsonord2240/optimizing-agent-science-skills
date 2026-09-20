#!/bin/bash
# External annotators for INPUT 4 (synthetic sequences written by ISAR extractSequence): CPC2 (as-cpc2) + HMMER hmmscan/Pfam-A (as-annot)
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
W=/mnt/openscience/audits/bio-isoform-switching/run/work/annot; rm -rf $W; mkdir -p $W
SEQ=/mnt/openscience/audits/bio-isoform-switching/run/work/sequences
rm -rf /tmp/CPC2_isw; cp -r $AS/tools/src/CPC2_standalone /tmp/CPC2_isw
cd /tmp/CPC2_isw/libs/libsvm; tar zxf libsvm-3.18.tar.gz; cd libsvm-3.18; make clean > /dev/null 2>&1; make > $W/libsvm.log 2>&1; echo "libsvm rc=$?"
cd $W
micromamba run -n as-cpc2 python /tmp/CPC2_isw/bin/CPC2.py -i $SEQ/isoformSwitchAnalyzeR_isoform_nt.fasta -o cpc2_result > cpc2.log 2>&1; echo "CPC2 rc=$?"
ls -la cpc2_result.txt; head -4 cpc2_result.txt
# hmmscan on the AA fasta. pfam_scan.pl is not installed; hmmscan --domtblout is the documented tool in the Skill ("HMMER hmmscan against Pfam-A")
micromamba run -n as-annot hmmscan --cut_ga --domtblout pfam_domtbl.txt -o hmmscan_stdout.txt $AS/public-data/reference_dbs/Pfam-A.hmm $SEQ/isoformSwitchAnalyzeR_isoform_AA.fasta; echo "hmmscan rc=$?"
grep -v '^#' pfam_domtbl.txt | awk '{print $1, $2, $4, $7}' | sort | head -30
echo "domain hits: $(grep -vc '^#' pfam_domtbl.txt)"
