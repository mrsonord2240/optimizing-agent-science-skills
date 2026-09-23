cd /mnt/openscience/audits/bio-sam-bam-basics/run/data/in7
export PYTHONDONTWRITEBYTECODE=1
python ../../skill/examples/view_bam.py unmapped_only.cram 5 2>&1 | head; echo "--- rc=$?"
samtools view unmapped_only.cram | head -2 | cut -f1-9
diff <(samtools view hand.sam | cut -f1-11 ) <(samtools view c3.sam | cut -f1-11) | head -20
echo ---; diff <(samtools view hand.sam | cut -f12-|sort ) <(samtools view c3.sam | cut -f12-|sort) | head
