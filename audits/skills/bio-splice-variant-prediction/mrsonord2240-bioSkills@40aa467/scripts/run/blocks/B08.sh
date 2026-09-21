pip install torch sinkhorn-transformer "axial-positional-embedding==0.2.1" "PyVCF3==1.0.0" pyensembl gffutils pyfaidx pandas tqdm gdown
# axial-positional-embedding 0.2.1 is required: newer versions rename pos_emb weights and load_state_dict fails
# put a chr-prefixed hg38.fa and GENCODE hg38.annotation.gtf.gz in data/data_package/, then index the GTF once
# (the annotation name is hard-coded in sptransformer.py, whatever GENCODE release the GTF is):
pyensembl install --reference-name hg38 --annotation-name gencode.v38 --gtf data/data_package/hg38.annotation.gtf.gz
python sptransformer.py -I input.vcf -O out.csv --reference hg38
