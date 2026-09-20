awk 'BEGIN{OFS="\t"} $4>0 {print $1,$2-1,$3,"sj"NR,$7,($4==1?"+":"-")}' SJ.out.tab > sr_junctions.bed
minimap2 -ax splice:hq --secondary=no --junc-bed sr_junctions.bed --junc-bonus 20 -t 16 reference.fa isoseq.fastq.gz | samtools sort -o isoseq_aligned.bam
# annotation-guided alternative (uLTRA 0.1; --ont for ONT); writes uLTRA_out/reads.sam
uLTRA pipeline --isoseq --t 16 reference.fa annotation.gtf isoseq.fastq.gz uLTRA_out
