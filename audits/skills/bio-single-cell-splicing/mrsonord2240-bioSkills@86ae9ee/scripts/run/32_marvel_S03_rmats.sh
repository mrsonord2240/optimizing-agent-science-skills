#!/bin/bash
# INPUT 4 (real data): produce rMATS fromGTF.*.txt from the real chrX BAMs (2 v 2), stage two GTF variants for SKILL.md block S03:
#   annotation.gtf  = Ensembl chrX GTF as shipped (gene_biotype attribute)  ;  annotation_gencode.gtf = built by 34_make_gencode_style_gtf.py (gene rows + gene_type)
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run; P=$ASDATA/rnasplice
W=$R/out/in4_s03; rm -rf $W; mkdir -p $W; cd $W
echo -n "$P/bam/ERR188383.Aligned.out.bam,$P/bam/ERR188428.Aligned.out.bam" > b1.txt
echo -n "$P/bam/ERR188454.Aligned.out.bam,$P/bam/ERR204916.Aligned.out.bam" > b2.txt
cp $P/reference/genes_chrX.gtf annotation.gtf
grep -c $'\tgene\t' annotation.gtf; grep -m1 $'\tgene\t' annotation.gtf | cut -c1-250
rmats.py --b1 b1.txt --b2 b2.txt --gtf annotation.gtf -t paired --readLength 75 --nthread 8 --od rmats_out --tmp tmp --task both 2>&1 | tail -3
wc -l rmats_out/fromGTF.*.txt | grep -v novel
rm -rf tmp
