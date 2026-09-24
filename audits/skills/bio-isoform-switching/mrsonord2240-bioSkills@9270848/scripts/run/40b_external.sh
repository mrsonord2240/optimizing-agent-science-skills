#!/bin/bash
# External annotators for INPUT 4, run in WSL `science` on the sequences ISAR wrote: CPC2 (as-cpc2), hmmscan --cut_ga vs Pfam-A (as-annot),
# then the Skill's converter examples/hmmscan_to_pfamscan.py with Pfam-A.clans.tsv.gz downloaded as the Skill's own command says.
# Run through wsl_run.sh:  wsl_run.sh 'bash /mnt/openscience/audits/bio-isoform-switching/run/40b_external.sh'
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
RUN=/mnt/openscience/audits/bio-isoform-switching/run
[ -d /tmp/CPC2_isw/libs/libsvm/libsvm-3.18 ] || { rm -rf /tmp/CPC2_isw; cp -r $AS/tools/src/CPC2_standalone /tmp/CPC2_isw; cd /tmp/CPC2_isw/libs/libsvm; tar zxf libsvm-3.18.tar.gz; cd libsvm-3.18; make clean > /dev/null 2>&1; make > /tmp/libsvm.log 2>&1; echo "libsvm rc=$?"; }
# pressed Pfam-A on tmpfs (reads over 9p were very slow); the .hmm stub only has to exist
[ -f /tmp/pf/Pfam-A.hmm.h3m ] || { mkdir -p /tmp/pf; for e in h3f h3i h3m h3p; do cp $AS/public-data/reference_dbs/Pfam-A.hmm.$e /tmp/pf/; done; head -c 1000000 $AS/public-data/reference_dbs/Pfam-A.hmm > /tmp/pf/Pfam-A.hmm; }
for set in w4s w3; do
  D=$RUN/work/$set/annot; rm -rf $D; mkdir -p $D; SEQ=$RUN/work/$set/sequences; cd $D
  [ "$set" = w3 ] && SEQ=$RUN/work/w3/sequences
  micromamba run -n as-cpc2 python /tmp/CPC2_isw/bin/CPC2.py -i $SEQ/isoformSwitchAnalyzeR_isoform_nt.fasta -o cpc2_result > cpc2.log 2>&1; echo "$set CPC2 rc=$? rows=$(wc -l < cpc2_result.txt)"
  # the Skill's bash block, verbatim apart from paths: hmmscan --cut_ga --domtblout, curl clans, converter
  micromamba run -n as-annot hmmscan --cpu 8 --cut_ga --domtblout pfam_domtbl.txt /tmp/pf/Pfam-A.hmm $SEQ/isoformSwitchAnalyzeR_isoform_AA.fasta > /dev/null; echo "$set hmmscan rc=$? domain rows=$(grep -vc '^#' pfam_domtbl.txt) seqs=$(grep -c '>' $SEQ/isoformSwitchAnalyzeR_isoform_AA.fasta)"
  cp $RUN/work/annot_dl/Pfam-A.clans.tsv.gz .
  python3 $RUN/skill/examples/hmmscan_to_pfamscan.py pfam_domtbl.txt pfam_scanfmt.txt Pfam-A.clans.tsv.gz; echo "$set converter rc=$?"
  head -3 pfam_scanfmt.txt
done
