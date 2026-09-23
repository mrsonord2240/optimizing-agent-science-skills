cd /mnt/openscience/audits/bio-sam-bam-basics/run
export PYTHONDONTWRITEBYTECODE=1
D=$AFDATA/human
echo "--- view_bam.py BAM + reference arg"; python skill/examples/view_bam.py $D/test.paired_end.sorted.bam 2 $D/genome.fasta; echo rc=$?
echo "--- view_bam.py SAM + reference arg"; python skill/examples/view_bam.py data/in7/hand.sam 2 data/in7/ref.fa; echo rc=$?
echo "--- view_bam.py nonexistent reference for BAM"; python skill/examples/view_bam.py $D/test.paired_end.sorted.bam 2 /nonexistent.fa 2>&1 | head -4; echo rc=$?
echo "--- convert leftover on failure (SAM w/o SQ)"; printf 'r1\t0\tchr22\t100\t60\t4M\t*\t0\t0\tACGT\tFFFF\n' > data/nosq.sam; rm -f data/nosq.bam; bash skill/examples/convert_formats.sh data/nosq.sam data/nosq.bam; echo rc=$?; ls -la data/nosq.bam 2>&1
echo "--- CRAM out w/o reference leftover"; rm -f data/x.cram; bash skill/examples/convert_formats.sh $D/test.paired_end.sorted.bam data/x.cram; echo rc=$?; ls data/x.cram 2>&1
echo "--- CRAM in, wrong reference"; rm -f data/y.bam; bash skill/examples/convert_formats.sh $D/test.paired_end.sorted.cram data/y.bam data/in7/ref.fa; echo rc=$?; ls -la data/y.bam 2>&1
rm -rf skill/examples/__pycache__ data/nosq.sam data/nosq.bam data/y.bam
