source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
D=$AS/public-data/rnasplice/bam
printf "g1\t$D/ERR188383.Aligned.out.bam\tGBR\ng2\t$D/ERR188428.Aligned.out.bam\tGBR\ny1\t$D/ERR188454.Aligned.out.bam\tYRI\ny2\t$D/ERR204916.Aligned.out.bam\tYRI\n" > $RUN/data/real_groups.tsv
echo "TAZ (rmats2sashimiplot PDF shows GBR: 2,1  YRI: 2,0,1)"
micromamba run -n as-core python $RUN/scripts/jtruth.py X:153647882-153648412 $RUN/data/real_groups.tsv 2>&1 | grep -v hts_idx
echo "PDZD11 (PDF text check)"
micromamba run -n as-core python $RUN/scripts/jtruth.py X:69509105-69509795 $RUN/data/real_groups.tsv 2>&1 | grep -v hts_idx
