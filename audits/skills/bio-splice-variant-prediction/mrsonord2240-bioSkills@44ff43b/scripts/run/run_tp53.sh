#!/bin/bash
# INPUT 2b: usage-guide TP53 example variant + SKILL.md TP53 c.673-2A>G on GRCh38 (hg38 chr17 from the FLAIR test set; SpliceAI -A grch38).
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
FA=$AS/public-data/longread/flair_test/genome.fa
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
printf '##fileformat=VCFv4.2\n##contig=<ID=chr17,length=83257441>\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nchr17\t7674292\tTP53_c.673-2A>G\tT\tC\t.\t.\t.\nchr17\t7676154\tusage_guide_as_written_A>G\tA\tG\t.\t.\t.\nchr17\t7676154\tTP53_c.215C>G_P72R\tG\tC\t.\t.\t.\n' > data/tp53_grch38.vcf
$AS/tools/bin/asenv as-spliceai python -c "
import pyfaidx; fa=pyfaidx.Fasta('$FA'); print('hg38 chr17:7674292 =', fa['chr17'][7674291:7674292].seq.upper(), ' (expect T = complement of transcript-strand A)')"
$AS/tools/bin/spliceai -I data/tp53_grch38.vcf -O out/sai_tp53.vcf -R $FA -A grch38 -D 50 -M 0 > out/sai_tp53.log 2>&1; echo "rc=$?"
grep -a "WARNING\|ERROR" out/sai_tp53.log | cut -c1-200
grep -v '^##' out/sai_tp53.vcf | cut -f2-5,8
