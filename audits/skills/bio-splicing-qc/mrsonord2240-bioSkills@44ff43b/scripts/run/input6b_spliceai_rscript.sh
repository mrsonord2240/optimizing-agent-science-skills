#!/bin/bash
# Input 6 extension: (a) SpliceAI CLI on a canonical donor variant, flags as in SKILL.md; (b) RSeQC without Rscript (hidden dependency)
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run
W=$R/work/in6b; mkdir -p $W; cd $W
printf '##fileformat=VCFv4.2\n##contig=<ID=X,length=155270560>\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nX\t193062\t.\tG\tA\t.\t.\t.\n' > donor.vcf
echo "== SpliceAI (SKILL.md failure-mode row: use -D 50 for screening)"
asenv as-spliceai spliceai -I donor.vcf -O donor.out.vcf -R $ASDATA/derived/X.fa -A grch37 -D 50 -M 0 2>&1 | grep -v -i -E "warning|pkg_resources|tensorflow|cuda|oneDNN|rebuild|^$|E0000|I0000|W0000" | tail -3
grep -v '^##' donor.out.vcf
echo "== RSeQC without Rscript on PATH: junction_annotation.py --rscript /nonexistent"
junction_annotation.py -i $R/data/synthetic/se_clean.bam -r $R/data/synthetic/synth.bed12 -o noR --rscript /nonexistent > noR.log 2>&1; echo "rc=$?"; tail -2 noR.log; ls noR.* | head
junction_saturation.py -i $R/data/synthetic/se_clean.bam -r $R/data/synthetic/synth.bed12 -o noRs --rscript /nonexistent > noRs.log 2>&1; echo "saturation rc=$?"; tail -1 noRs.log; ls noRs.*
echo "== referenced Related Skills exist in the staging repo?"
for d in splicing-quantification differential-splicing splice-variant-prediction long-read-splicing; do ls -d /mnt/openscience/external/mrsonord2240__bioSkills/alternative-splicing/$d 2>&1 | head -1; done
for d in read-alignment/star-alignment read-qc/quality-reports read-qc/contamination-screening; do ls -d /mnt/openscience/external/mrsonord2240__bioSkills/$d 2>&1 | head -1; done
