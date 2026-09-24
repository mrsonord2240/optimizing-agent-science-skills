# Input 5 setup: STAR index for the real chrX (GRCh37) set, sjdbOverhang 149 (as SKILL.md's 2x150 example; reads are 2x75)
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
S=/mnt/openscience/as-qc-reaudit-scratch; mkdir -p $S/star && cd $S/star
P=$ASDATA/rnasplice
[ -d genome_index ] && { echo "index exists"; exit 0; }
mkdir genome_index
STAR --runMode genomeGenerate --runThreadN 12 --genomeDir genome_index --genomeFastaFiles $ASDATA/derived/X.fa --sjdbGTFfile $P/reference/genes_chrX.gtf --sjdbOverhang 149 --genomeSAindexNbases 12 --outFileNamePrefix idx_ > idx.stdout 2>&1
echo rc=$?; tail -3 idx.stdout; ls genome_index | head
