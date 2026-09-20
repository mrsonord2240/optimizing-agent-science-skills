source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data
printf 'GBR1\t/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR188383.Aligned.out.bam\tGBR\nGBR2\t/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR188428.Aligned.out.bam\tGBR\nYRI1\t/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR188454.Aligned.out.bam\tYRI\nYRI2\t/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR204916.Aligned.out.bam\tYRI\n' > sashimi_groups.tsv
cat sashimi_groups.tsv
cp /mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/reference/genes_chrX.gtf annotation.gtf; ls -la annotation.gtf
