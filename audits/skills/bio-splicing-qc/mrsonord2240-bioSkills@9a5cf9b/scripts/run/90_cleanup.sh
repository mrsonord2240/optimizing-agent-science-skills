R=/mnt/openscience/audits/bio-splicing-qc/run
cd $R/work
rm -rf in5e/*_STARgenome in5e/*_STARtmp in5e/ERR188383.Aligned.out.bam* in5e/noidx.bam in5e/g.bed
find . -name '*.bam' -size +200k -delete; find . -name '*.bai' -delete
find . -name '*_screen.html' -delete; find . -name '*.junction.Interact.bed' -delete
find $R -name __pycache__ -prune -exec rm -rf {} \;
du -sh $R $R/work $R/data
