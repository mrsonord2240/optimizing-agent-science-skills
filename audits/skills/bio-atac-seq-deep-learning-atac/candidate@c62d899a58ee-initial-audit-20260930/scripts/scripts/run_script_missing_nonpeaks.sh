# Run the UNMODIFIED-but-for-contig-names Skill script with NONPEAKS pointing at a file that does not exist
# (the script never generates it and the Skill never says how). Bounded by timeout 600.
source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
export PATH=/home/sci/micromamba/envs/dlatac-tf/bin:$PATH
P=$ME/public-cache/pseudo; R=/mnt/openscience/audits/bio-atac-seq-deep-learning-atac/initial-audit-20260930/runs/nonpeaks; rm -rf $R; mkdir -p $R; cd $R
export TMPDIR=$R/tmp; mkdir -p $TMPDIR
SK=/mnt/openscience/wt/atac-deep-learning-atac/skills/bio-atac-seq-deep-learning-atac/scripts/chrombpnet_pipeline.sh
sha256sum $SK
python $ME/scripts/adapt_skill_script.py $SK adapted.sh
( time timeout 600 bash adapted.sh $P/pseudo.bam $P/pseudo.narrowPeak nonpeaks.bed $P/pseudo.fa $P/pseudo.chrom.sizes $R/out ATAC 0.5 ) 2>&1 | grep -v -E "it/s\]|^[0-9]+it \[" | tail -25
echo "exit=${PIPESTATUS[0]}"
ls out/bias out/model 2>&1 | head
