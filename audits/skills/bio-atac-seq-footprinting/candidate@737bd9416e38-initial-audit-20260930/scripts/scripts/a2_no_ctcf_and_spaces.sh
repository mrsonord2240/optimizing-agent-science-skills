#!/bin/bash
# A2: (i) motif file without CTCF -> does the script's CTCF validation step fail loudly or vanish silently?
#     (ii) output directory containing a space (unquoted vars in run_tobias.sh).
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
R=$W/${A2DIR:-a2}; rm -rf $R; mkdir -p $R; prep_inputs $R; cd $R
awk 'BEGIN{keep=0} /^>/{n=$2; keep=(n=="GATA1"||n=="IRF4"||n=="EBF1")} keep{print}' $D/motifs/JASPAR2024_CORE_vertebrates_non-redundant_pfms.txt > motifs_noctcf.pfm
grep '>' motifs_noctcf.pfm
bash $SKILL/scripts/run_tobias.sh cond1.bam cond2.bam peaks.bed $D/reference/hg38.chr1.fa hg38-blacklist.v2.bed motifs_noctcf.pfm out 6 > run.log 2>&1
echo "(i) no-CTCF motif set: run_tobias.sh rc=$?"
ls out/validation; echo "validation files: $(ls out/validation | wc -l)"
grep -ci "ctcf\|validation plot\|warn" run.log | sed 's/^/log lines mentioning ctcf|validation plot|warn: /'
tail -8 run.log | cut -c1-160
# (ii) space in outdir; fail fast, one core
mkdir -p sp && cd sp
timeout 120 bash $SKILL/scripts/run_tobias.sh ../cond1.bam ../cond2.bam ../peaks.bed $D/reference/hg38.chr1.fa ../hg38-blacklist.v2.bed ../motifs_noctcf.pfm "out dir" 1 > run.log 2>&1
echo "(ii) outdir with space: rc=$?"; tail -5 run.log | cut -c1-200; echo "stray dirs created:"; ls -d out* dir* 2>/dev/null
