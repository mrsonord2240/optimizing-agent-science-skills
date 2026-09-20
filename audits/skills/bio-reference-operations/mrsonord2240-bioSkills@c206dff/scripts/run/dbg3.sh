cd /mnt/openscience/audits/bio-reference-operations/run/work/in3
picard ValidateSamFile I=h.bam R=hs_num.fa MODE=SUMMARY 2>&1 | grep -v -i -E "setlocale|^\*|^$|Picked|INFO" | head
echo ---- diff BAM vs CRAM
samtools view h.bam > a.sam; samtools view -T hs.fa h.cram > b.sam; wc -l a.sam b.sam; diff <(cut -f1-9,11 a.sam) <(cut -f1-9,11 b.sam) | head -3; diff <(cut -f12- a.sam) <(cut -f12- b.sam) | head -4 | cut -c1-300
