source /mnt/openscience/audits/bio-alignment-indexing/run/work/r5/ei_func.sh
cd work/r5/emptydir
for f in *.bam; do ensure_index "$f"; done     # an empty directory is a successful no-op
