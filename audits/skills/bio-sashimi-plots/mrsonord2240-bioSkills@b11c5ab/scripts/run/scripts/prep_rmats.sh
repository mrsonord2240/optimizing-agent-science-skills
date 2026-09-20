# Generate rMATS-turbo 4.4.0 output for (a) the planted 3v3 set and (b) real chrX 2 GBR v 2 YRI (Ensembl contig X). Output: data/rmats_planted, data/rmats_real
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
P=$AS/public-data/planted; D=$AS/public-data/rnasplice
T=$RUN/out/rmats_tmp; rm -rf $T; mkdir -p $T
cd $T
micromamba run -n as-core rmats.py --b1 $P/b1.txt --b2 $P/b2.txt --gtf $P/planted.gtf -t single --readLength 50 --nthread 4 --od $RUN/data/rmats_planted --tmp $T/tp --libType fr-unstranded > planted.log 2>&1; echo "planted rc=$?"
echo "$D/bam/ERR188383.Aligned.out.bam,$D/bam/ERR188428.Aligned.out.bam" > b1.txt
echo "$D/bam/ERR188454.Aligned.out.bam,$D/bam/ERR204916.Aligned.out.bam" > b2.txt
micromamba run -n as-core rmats.py --b1 b1.txt --b2 b2.txt --gtf $D/reference/genes_chrX.gtf -t paired --readLength 75 --nthread 4 --od $RUN/data/rmats_real --tmp $T/tr --libType fr-unstranded > real.log 2>&1; echo "real rc=$?"
rm -rf $T
wc -l $RUN/data/rmats_planted/SE.MATS.JC.txt $RUN/data/rmats_real/*.MATS.JC.txt
rm -rf $RUN/data/rmats_planted/tmp $RUN/data/rmats_real/tmp
ls $RUN/data/rmats_real | head -30
