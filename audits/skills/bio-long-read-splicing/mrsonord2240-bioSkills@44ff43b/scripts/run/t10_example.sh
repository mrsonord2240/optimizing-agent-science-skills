#!/bin/bash
# Input 5/7: run the SHIPPED examples/longread_splicing_pipeline.sh from a COPY on SYNTHETIC data, verbatim first, then patch one failure class at a time (patch_example.py).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
D=$R/data/synth
O=$R/out/example; rm -rf $O; mkdir -p $O; cd $O
cp $D/chrS1.fa reference.fa; cp $D/ref.gtf gencode.v45.annotation.gtf
gzip -c $D/hifi/ctrl1.fastq > hifi.fastq.gz
gzip -c $D/ontunstr/ctrl1.fastq > ont.fastq.gz
which minimap2 samtools bedtools isoquant.py isoquant flair sqanti3_qc.py sqanti3_filter.py 2>&1 | sed 's/^/which: /'
for STAGE in 0 1 2 3; do
  asenv as-core python $R/patch_example.py $R/skill_copy/examples/longread_splicing_pipeline.sh ex$STAGE.sh $STAGE
done
diff ex0.sh ex3.sh > ex_patch.diff; cat ex_patch.diff
for STAGE in 0 1 2 3; do
  echo "################ STAGE $STAGE (PLATFORM=hifi) ################"
  rm -rf longread_output_sample; cp hifi.fastq.gz sample.fastq.gz
  PLATFORM=hifi THREADS=4 timeout 900 bash ex$STAGE.sh > run$STAGE.log 2>&1; echo "exit code: $?"
  tail -4 run$STAGE.log | cut -c1-260
  ls longread_output_sample 2>/dev/null | tr '\n' ' '; echo
done
echo "################ STAGE 3 with PLATFORM=ont on UNSTRANDED ONT cDNA (example uses splice -uf -k14) ################"
rm -rf longread_output_sample; cp ont.fastq.gz sample.fastq.gz
PLATFORM=ont THREADS=4 timeout 900 bash ex3.sh > run3_ont.log 2>&1; echo "exit code: $?"; tail -3 run3_ont.log | cut -c1-200
micromamba run -n as-lr python $R/junction_check.py longread_output_sample/sample_aligned.bam $D/read_tx.gtf "example PLATFORM=ont bam (unstranded ONT cDNA)"
echo "### stage-3 hifi outputs sanity"
rm -rf longread_output_sample; cp hifi.fastq.gz sample.fastq.gz; PLATFORM=hifi THREADS=4 bash ex3.sh > run3b.log 2>&1
ls longread_output_sample longread_output_sample/sqanti3 longread_output_sample/sqanti3_filtered 2>&1 | head -40
cut -f1,8 longread_output_sample/sqanti3/sqanti3_classification.txt 2>/dev/null | head -12
wc -l longread_output_sample/sqanti3_filtered/*pass_isoforms.txt 2>/dev/null
