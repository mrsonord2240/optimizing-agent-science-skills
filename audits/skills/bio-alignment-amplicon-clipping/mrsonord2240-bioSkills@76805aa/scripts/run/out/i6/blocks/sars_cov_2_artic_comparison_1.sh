# iVar needs a coordinate-sorted, indexed BAM. -q 0 -m 1 turns the quality/length filters off so only
# primer logic acts; reads with no primer are dropped unless -e is given.
samtools index input.bam
ivar trim -i input.bam -b primers.bed -p ivar_trimmed -q 0 -m 1   # writes ivar_trimmed.bam
