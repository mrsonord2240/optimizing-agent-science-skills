#!/bin/bash
# SQANTI3 on REAL FLAIR-collapsed isoforms (LRGASP cDNA, hg38 chr12/17/20, FLAIR-test annotation); plus determinism (T3) re-runs and IsoQuant dependency claim.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/flair_test
O=$R/out/real_flair; cd $O
cp $P/genome.fa $P/genome.fa.fai .
SQ="micromamba run -n as-sqanti"; LR="micromamba run -n as-lr"
mkdir -p sq; cd sq
$SQ sqanti3_qc.py --isoforms ../rkcoll.isoforms.gtf --refGTF ../basic.annotation.gtf --refFasta ../genome.fa --output real --aligner_choice minimap2 --cpus 8 --report skip > qc.log 2>&1; echo "sqanti qc rc=$?"
cut -f8 sqanti3_results/real_classification.txt | tail -n +2 | sort | uniq -c
cut -f8,9 sqanti3_results/real_classification.txt | tail -n +2 | sort | uniq -c | sort -rn | head -8
cd ..
echo "### determinism: repeat flair collapse and IsoQuant, md5 compare"
$LR flair collapse --query rk_all_corrected.bed --reads basic.reads.fa --genome genome.fa --gtf basic.annotation.gtf --output rkcoll2 --threads 8 > rkcoll2.log 2>&1
md5sum rkcoll.isoforms.bed rkcoll2.isoforms.bed | awk '{print $1}' | uniq | wc -l | sed 's/^/distinct md5 of flair collapse bed over 2 runs (1=identical): /'
rm -f genome.fa genome.fa.fai
D=$R/data/synth
for i in 1 2; do $LR isoquant --reference $D/chrS1.fa --genedb $D/ref.gtf --bam $R/out/flair/ctrl1.bam --data_type pacbio_ccs --output $R/out/det_iq$i --prefix d --threads 4 > /dev/null 2>&1; done
md5sum $R/out/det_iq1/d/d.transcript_counts.tsv $R/out/det_iq2/d/d.transcript_counts.tsv | awk '{print $1}' | uniq | wc -l | sed 's/^/distinct md5 of IsoQuant counts over 2 runs (1=identical): /'
echo "### IsoQuant dependency claim (ssw-py)"; $LR pip show isoquant 2>/dev/null | grep -i requires; $LR pip list 2>/dev/null | grep -i -E "ssw|edlib|parasail"
