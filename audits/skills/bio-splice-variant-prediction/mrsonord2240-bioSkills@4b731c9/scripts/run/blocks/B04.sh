# annotation DB: Pangolin's own script; default keeps only Ensembl_canonical transcripts (several minutes for the full GTF)
create_db.py gencode.v45.annotation.gtf          # -> gencode.v45.annotation.db   (add --filter None to keep every transcript)

pangolin input.vcf GRCh38.primary_assembly.genome.fa gencode.v45.annotation.db pangolin_output -d 50 -m False
pangolin input.vcf GRCh38.primary_assembly.genome.fa gencode.v45.annotation.db pangolin_d500 -d 500 -m False -s 0.2   # every site with |change| >= 0.2
