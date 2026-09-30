S=$1; O=$2; cd $O
python $S/library_complexity.py lc_single.bam > lc_single.json
python $S/aggregate_qc.py lc_single.json --output agg_single.tsv; cat agg_single.tsv
echo '--- python json.loads strict vs Infinity'; python -c "
import json;t=open('lc_single.json').read();print(t.replace(chr(10),' '))
try: json.loads(t,parse_constant=lambda c:(_ for _ in ()).throw(ValueError('non-standard JSON constant '+c)))
except Exception as e: print('STRICT PARSE FAIL:',e)
"
echo '--- jq'; which jq && jq . lc_single.json
echo '--- string value'; echo '{"NRF":"0.9","FRiP":0.25,"mt_fraction":null,"TSS_enrichment":"nan"}' > s.json; python $S/aggregate_qc.py s.json 2>&1 | tail -4
echo '--- realistic combined metrics input (library_complexity keys + tss key)'; echo '{"NRF":0.78,"PBC1":0.80,"PBC2":5.1,"total":606652,"distinct":472514,"TSS_enrichment":11.4,"FRiP":0.67,"mt_fraction":0.12,"nuclear_reads_M":30}' > m.json; python $S/aggregate_qc.py m.json --output agg_m.tsv; cat agg_m.tsv
echo '--- MultiQC treat as custom content'; mkdir -p mqc; cp agg_m.tsv mqc/report_mqc.tsv; multiqc mqc -o mqc_out -f 2>&1 | tail -5; ls mqc_out; grep -c . mqc_out/multiqc_data/multiqc_sources.txt 2>/dev/null; cat mqc_out/multiqc_data/multiqc_sources.txt 2>/dev/null; ls mqc_out/multiqc_data
