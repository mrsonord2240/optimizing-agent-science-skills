source /mnt/openscience/audits/bio-atac-seq-atac-qc/reaudit-run/scripts/env.sh; cd $O; mkdir -p agg; cd agg
cat > multi.json <<J
{"A":{"nuclear_reads_M":60,"mt_fraction":0.03,"NRF":0.95,"PBC1":0.95,"PBC2":4,"TSS_enrichment":9,"FRiP":0.4},
 "B":{"nuclear_reads_M":30,"mt_fraction":0.3,"NRF":0.8,"PBC1":0.8,"PBC2":2,"TSS_enrichment":6,"FRiP":0.25},
 "C":{"nuclear_reads_M":10,"mt_fraction":0.6,"NRF":0.5,"PBC1":0.5,"PBC2":null,"TSS_enrichment":3,"FRiP":0.1},
 "D":{"nuclear_reads_M":60,"mt_fraction":0.03,"NRF":0.95,"PBC1":0.95,"PBC2":4,"TSS_enrichment":9}}
J
echo '{"NRF":0.95,"junk":1}' > flat.json; echo '{"NRF":"high"}' > bad.json; echo '{"NRF":true}' > bool.json
python $S/aggregate_qc.py multi.json --output multi_mqc.tsv; echo exit=$?; cat multi_mqc.tsv
python $S/aggregate_qc.py flat.json --sample S1 --output flat_mqc.tsv; echo exit=$?; cat flat_mqc.tsv
python $S/aggregate_qc.py bad.json; echo exit=$?
python $S/aggregate_qc.py bool.json; echo exit=$?
python - <<'P'
import pandas as pd
d=pd.read_csv('multi_mqc.tsv',sep='\t',comment='#',index_col=0); print(d[['NRF_grade','TSS_enrichment_grade','mt_fraction_grade','overall_grade']])
P
# lib complexity JSON from real -> could feed
multiqc . -o mq -f -q 2>&1 | tail -2; python - <<'P'
import json;d=json.load(open('mq/multiqc_data/multiqc_data.json'));print([k for k in d['report_data_sources'] ] if 'report_data_sources' in d else list(d)[:8])
import glob;print(glob.glob('mq/multiqc_data/*'))
P
grep -c . mq/multiqc_data/multiqc_atac_encode_qc.txt 2>/dev/null; head -6 mq/multiqc_data/multiqc_atac_encode_qc.txt 2>/dev/null
