# Audit run of the Skill's nucleosome_analysis.R: (A) verbatim, (B) with the minimal fixes needed to get past the two API breaks (scratch copy, Skill untouched)
export PATH=$NPR/bin:$PATH
D=/mnt/openscience/audits/bio-atac-seq-nucleosome-positioning/initial-audit-20260930
W=$NP/work/a2; rm -rf $W; mkdir -p $W/A $W/B
BAM=$ATACDATA/encode/GM12878_rep1_filtered.chr1_1-30000000.bam
cd $W/A; Rscript $SKILL/scripts/nucleosome_analysis.R $BAM gm > run.log 2>&1; echo "A verbatim rc=$?"; tail -4 run.log; ls
cd $W/B; Rscript $D/scripts/a2_patched_nucleosome_analysis.R $BAM gm > run.log 2>&1; echo "B patched rc=$?"; tail -25 run.log | cut -c1-240; ls -la
