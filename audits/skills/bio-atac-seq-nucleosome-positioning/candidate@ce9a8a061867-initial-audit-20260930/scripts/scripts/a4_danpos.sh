# Audit run of the Skill's DANPOS3 differential recipe on a planted-shift pair (see a4_make_planted_shift.py). Shared atac-danpos env, read-only.
export PATH=$NPENV/bin:$PATH
D=/mnt/openscience/audits/bio-atac-seq-nucleosome-positioning/initial-audit-20260930
W=$NP/work/a4; rm -rf $W; mkdir -p $W; cd $W
python $D/scripts/a4_make_planted_shift.py
for x in ctl trt; do samtools sort -@4 -o $x.bam $x.unsorted.bam && samtools index $x.bam; done
export PATH=$SHARED/tools/bin:$PATH
( time danpos dpos $W/trt.bam:$W/ctl.bam -o diff --paired 1 --smooth_width 80 ) > diff.log 2>&1; echo "diff rc=$?"; tail -3 diff.log | cut -c1-200
python $D/scripts/a4_check.py 2>&1 | tail -30
