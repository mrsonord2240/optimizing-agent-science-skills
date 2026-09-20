#!/bin/bash
# Input 2/7: IsoQuant recipes from SKILL.md / example pipeline on SYNTHETIC HiFi-like reads (planted truth) and on REAL ONT direct-RNA (bambu extdata).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
D=$R/data/synth
O=$R/out/isoquant; rm -rf $O; mkdir -p $O; cd $O
G=$D/chrS1.fa
LR="micromamba run -n as-lr"
echo "##### A. SKILL verbatim command name isoquant.py"
$LR isoquant.py --reference $G --genedb $D/ref.gtf --fastq $D/hifi/ctrl1.fastq --data_type pacbio_ccs --output iq_skill --threads 4 --model_construction_strategy default_pacbio > skill_isoquantpy.log 2>&1
echo "rc=$?"; tail -2 skill_isoquantpy.log
echo "##### B. Same command with the entry point that exists (isoquant), 6 FASTQ = 6 samples, --data_type pacbio_ccs"
$LR isoquant --reference $G --genedb $D/ref.gtf --fastq $D/hifi/ctrl1.fastq $D/hifi/ctrl2.fastq $D/hifi/ctrl3.fastq $D/hifi/trt1.fastq $D/hifi/trt2.fastq $D/hifi/trt3.fastq --data_type pacbio_ccs --output iq_hifi --threads 4 --model_construction_strategy default_pacbio > iq_hifi.log 2>&1
echo "rc=$?"; tail -3 iq_hifi.log | cut -c1-200
find iq_hifi -maxdepth 3 -type f | sed 's|^|  |' | head -40
echo "##### C. example-pipeline path: BAM input + --prefix sample; where does transcript_models.gtf land?"
$LR minimap2 -ax splice:hq -uf --secondary=no -t 4 $G $D/hifi/ctrl1.fastq 2>/dev/null | $LR samtools sort -o ctrl1.bam - 2>/dev/null; $LR samtools index ctrl1.bam
$LR isoquant --reference $G --genedb $D/ref.gtf --bam ctrl1.bam --data_type pacbio_ccs --output iq_bam --threads 4 --prefix sample > iq_bam.log 2>&1
echo "rc=$?"; find iq_bam -maxdepth 3 -type f | sed 's|^|  |' | head -30
echo "example-script path exists? iq_bam/sample/sample.transcript_models.gtf -> $([ -f iq_bam/sample/sample.transcript_models.gtf ] && echo YES || echo NO)"
echo "##### D. de novo (no --genedb) as SKILL Decision Tree"
$LR isoquant --reference $G --fastq $D/hifi/ctrl1.fastq --data_type pacbio_ccs --output iq_denovo --threads 4 --prefix dn > iq_denovo.log 2>&1
echo "rc=$?"; tail -2 iq_denovo.log | cut -c1-200
echo "##### E. ONT unstranded reads: --data_type nanopore default strandness; and --data_type ont alias"
$LR isoquant --reference $G --genedb $D/ref.gtf --fastq $D/ontunstr/ctrl1.fastq --data_type nanopore --output iq_ont --threads 4 --prefix ont > iq_ont.log 2>&1; echo "nanopore rc=$?"
$LR isoquant --reference $G --genedb $D/ref.gtf --fastq $D/ontstr/ctrl1.fastq --data_type nanopore --stranded forward --output iq_ontstr --threads 4 --prefix ontstr > iq_ontstr.log 2>&1; echo "nanopore stranded rc=$?"
echo "##### F. REAL ONT direct RNA (SG-NEx A549 chr9:1-1e6; bambu extdata) - annotated (Ensembl 91) run"
B=/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/bambu_extdata
cp $B/*.bam $B/*.bam.bai $B/*.gtf $B/*.fa $B/*.fai .
$LR isoquant --reference Homo_sapiens.GRCh38.dna_sm.primary_assembly_chr9_1_1000000.fa --genedb Homo_sapiens.GRCh38.91_chr9_1_1000000.gtf --bam SGNex_A549_directRNA_replicate5_run1_chr9_1_1000000.bam --data_type nanopore --stranded forward --output iq_real --threads 4 --prefix real > iq_real.log 2>&1
echo "rc=$?"; tail -3 iq_real.log | cut -c1-200; find iq_real -maxdepth 3 -type f | head -30
rm -f *.bam *.bai *.fa *.fai Homo_*.gtf 2>/dev/null; ls
