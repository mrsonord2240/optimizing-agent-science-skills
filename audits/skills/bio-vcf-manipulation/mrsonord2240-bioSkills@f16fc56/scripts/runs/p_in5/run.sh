#!/bin/bash
# Input 5 (stress): two batches to merge - batch2 uses Ensembl contig names (1,2) and reuses a sample name;
# a third file arrives unsorted. Follow SKILL.md: harmonize names/contigs with reheader, then merge; sort.
set -uo pipefail
bgzip -c ../../data/cohort.vcf > joint.vcf.gz; bcftools index -f joint.vcf.gz
bcftools view -s SYN_S1,SYN_S2,SYN_S3,SYN_S4 joint.vcf.gz -Oz -o batch1.vcf.gz; bcftools index -f batch1.vcf.gz
# batch2: samples S5..S8 renamed so one collides (SYN_S5 -> SYN_S1), contigs renamed chr1->1, chr2->2
printf 'chr1\t1\nchr2\t2\n' > to_ensembl.txt; printf 'SYN_S5\tSYN_S1\n' > collide.txt
bcftools view -s SYN_S5,SYN_S6,SYN_S7,SYN_S8 joint.vcf.gz | bcftools annotate --rename-chrs to_ensembl.txt | bcftools reheader -s collide.txt | bgzip -c > batch2.vcf.gz; bcftools index -f batch2.vcf.gz
echo "batch2 CHROMs: $(bcftools query -f '%CHROM\n' batch2.vcf.gz | tr -d '\r' | sort -u | tr '\n' ' ') samples: $(bcftools query -l batch2.vcf.gz | tr -d '\r' | tr '\n' ' ')"
echo "== naive merge =="; bcftools merge batch1.vcf.gz batch2.vcf.gz -Oz -o m0.vcf.gz 2>&1 | tail -1
echo "== SKILL.md fix: reheader -s (names) and reheader -f ref.fa.fai (contigs) =="
printf 'SYN_S1\tSYN_S5\n' > uncollide.txt
bcftools reheader -s uncollide.txt batch2.vcf.gz -o b2_names.vcf.gz; bcftools reheader -f ../../data/ref.fa.fai b2_names.vcf.gz -o b2_fai.vcf.gz 2>&1 | tail -1
echo "after reheader -f: header contigs $(bcftools view -h b2_fai.vcf.gz | grep -c '^##contig'), body CHROMs: $(bcftools view -H b2_fai.vcf.gz 2>&1 | cut -f1 | tr -d '\r' | sort -u | head -3 | tr '\n' ' ')"
bcftools index -f b2_fai.vcf.gz 2>&1 | tail -1
bcftools merge batch1.vcf.gz b2_fai.vcf.gz -Oz -o m1.vcf.gz 2>&1 | tail -1; echo "merge after reheader -f: exit=$?"
echo "== what actually renames records: annotate --rename-chrs =="
printf '1\tchr1\n2\tchr2\n' > to_ucsc.txt
bcftools annotate --rename-chrs to_ucsc.txt b2_names.vcf.gz -Oz -o b2_ucsc.vcf.gz; bcftools index -f b2_ucsc.vcf.gz
bcftools merge batch1.vcf.gz b2_ucsc.vcf.gz -Oz -o m2.vcf.gz; bcftools index -f m2.vcf.gz
echo "merged: $(bcftools view -H m2.vcf.gz | wc -l) sites x $(bcftools query -l m2.vcf.gz | wc -l) samples; equals joint: $(bcftools view -H m2.vcf.gz | cut -f1-5 | md5sum | cut -c1-8) vs $(bcftools view -H joint.vcf.gz | cut -f1-5 | md5sum | cut -c1-8)"
echo "== --force-samples on the collision =="
bcftools merge --force-samples batch1.vcf.gz b2_ucsc.vcf.gz -Oz -o m3.vcf.gz 2>&1 | tail -1; bcftools query -l m3.vcf.gz | tr -d '\r' | tr '\n' ' '; echo
echo "== unsorted third file -> sort -> index =="
( bcftools view -h joint.vcf.gz; bcftools view -H joint.vcf.gz | shuf --random-source=<(yes) ) > unsorted.vcf
bgzip -c unsorted.vcf > unsorted.vcf.gz; bcftools index unsorted.vcf.gz 2>&1 | tail -1
bcftools sort -T ./tmp -m 100M unsorted.vcf.gz -Oz -o sorted.vcf.gz 2>&1 | tail -1; bcftools index -f sorted.vcf.gz && echo "sorted+indexed records: $(bcftools view -H sorted.vcf.gz | wc -l)"
