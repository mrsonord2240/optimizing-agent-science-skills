source /mnt/openscience/audits/bio-atac-seq-atac-qc/reaudit-run/scripts/env.sh; cd $O
python $R/mk_planted.py $O && echo built
j(){ tr -d '\n ' ; echo; }
echo "## planted PE defaults (truth total250 distinct160 NRF.64 PBC1.625 PBC2 2.0; excl chrM 300 recs, mapq 160 recs)"; python $S/library_complexity.py planted_pe.bam | j
echo "## PE no filters truth total 630"; python $S/library_complexity.py planted_pe.bam --min-mapq 0 --exclude-contigs '' | j
echo "## SE planted"; python $S/library_complexity.py planted_se.bam | j
echo "## SE forced single on PE (reads by 5' pos)"; python $S/library_complexity.py planted_pe.bam --mode single | j
echo "## empty result"; python $S/library_complexity.py planted_pe.bam --min-mapq 61 >/dev/null; echo exit=$?
U=$ATACDATA/encode/GM12878_rep1_unfiltered.chr1_1-30000000.bam; F=$ATACDATA/encode/GM12878_rep1_filtered.chr1_1-30000000.bam
echo "## real unfiltered default"; python $S/library_complexity.py $U | j
echo "## independent reference (own code, proper pair read1 mapq>=30 nonchrM, key by TLEN)"; python $R/ref_nrf.py $U
echo "## real filtered dedup"; python $S/library_complexity.py $F | j
echo "## PBC2 null strict json"; python $S/library_complexity.py planted_se.bam >/dev/null; python - <<P
import json,subprocess,os
o=subprocess.run(['python',os.environ['S']+'/library_complexity.py',os.environ['O']+'/planted_pe.bam','--mode','single'],capture_output=True,text=True).stdout
json.loads(o,parse_constant=lambda c:1/0); print('strict ok')
P
