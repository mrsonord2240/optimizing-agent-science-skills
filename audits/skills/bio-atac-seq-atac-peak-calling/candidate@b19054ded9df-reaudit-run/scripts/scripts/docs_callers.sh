source /mnt/openscience/audits/bio-atac-seq-atac-peak-calling/reaudit-run/scripts/env.sh
W=$R/docs; rm -rf $W; mkdir -p $W/hmm; cd $W; cp $BL hg38-blacklist.v2.bed
echo LD_PRELOAD=${LD_PRELOAD:-none}; macs3 --version; Genrich --version
# usage-guide Genrich commands verbatim (rep1.filt.dedup.bam -> real inputs)
samtools sort -n -o rep1.nsort.bam $E1; samtools sort -n -o rep2.nsort.bam $E2
Genrich -t rep1.nsort.bam,rep2.nsort.bam -o joint.narrowPeak -j -e chrM -E hg38-blacklist.v2.bed -q 0.05 > genrich.log 2>&1; echo genrich_rc=$?
Genrich -t rep1.nsort.bam,rep2.nsort.bam -o joint_noE.narrowPeak -j -e chrM -q 0.05 > genrich2.log 2>&1; echo genrich_noE_rc=$?
echo genrich_peaks_with_blacklist=$(wc -l < joint.narrowPeak) without=$(wc -l < joint_noE.narrowPeak)
echo "genrich coordinate-sorted (should abort):"; Genrich -t $E1 -o bad.narrowPeak -j -e chrM 2>&1 | tail -2
# hmmratac verbatim
macs3 hmmratac -i $E1 -f BAMPE -n rep1_hmm --outdir hmm/ > hmm.log 2>&1; echo hmm_rc=$?; ls hmm
awk 'BEGIN{OFS="\t"}{w=$3-$2; s+=w; n++} END{print "hmm regions="n" mean_width="s/n}' hmm/rep1_hmm_accessible_regions.narrowPeak
head -2 hmm/rep1_hmm_accessible_regions.narrowPeak
# NFR-only recipe (method-reference), GSIZE substituted
GSIZE=2.806e9
samtools view -h $E1 | awk 'substr($0,1,1)=="@" || ($9 > 0 && $9 < 100) || ($9 < 0 && $9 > -100)' | samtools view -b > nfr.bam; samtools index nfr.bam
echo nfr_reads=$(samtools view -c nfr.bam)
macs3 callpeak -t nfr.bam -f BAM -g $GSIZE -n sample_nfr --nomodel --shift -37 --extsize 75 --keep-dup all -p 0.01 --outdir nfr > nfr.log 2>&1; echo nfr_rc=$?
wc -l nfr/sample_nfr_peaks.narrowPeak
# overlap with ENCODE IDR conservative peaks in slice
ls $D | grep -i -E "917REN|346CZA"
