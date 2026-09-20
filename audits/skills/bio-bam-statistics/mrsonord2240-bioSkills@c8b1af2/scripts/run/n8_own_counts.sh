#!/bin/bash
# NEW: qc_report.py and block 027 vs flagstat -O tsv and hand counts on my own planted BAMs, and flagstat/qc_report vs the counts planted by construction (own_ctg.truth.json)
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; N=$R/data/new; cd $R/work
python $R/t3_qc_vs_flagstat.py $N/own_ctg.bam $N/own_insert.bam $N/own_del.bam
python - <<'PY'
import json, subprocess, re
N='/mnt/openscience/audits/bio-bam-statistics/run/data/new'; t=json.load(open(N+'/own_ctg.truth.json'))['flagstat']
fs={}
for l in subprocess.run(['samtools','flagstat','-O','tsv',N+'/own_ctg.bam'],capture_output=True,text=True).stdout.splitlines():
    a=l.split('	')
    if a[0].isdigit() and a[1].isdigit(): fs[a[2]]=(int(a[0]),int(a[1]))
q=subprocess.run(['python','/mnt/openscience/audits/bio-bam-statistics/run/skill/examples/qc_report.py',N+'/own_ctg.bam'],capture_output=True,text=True).stdout
g=lambda p:int(re.search(p,q).group(1).replace(',',''))
checks={'records':(g(r'Total records:\s+([\d,]+)'),t['records']),'secondary':(g(r'secondary ([\d,]+)'),t['secondary']),'supplementary':(g(r'supplementary ([\d,]+)'),t['supplementary']),
 'qcfail primary':(g(r'QC-failed primary:\s+([\d,]+)'),t['qcfail_primary']),'passed primary':(g(r'QC-passed primary:\s+([\d,]+)'),t['passed_primary']),
 'mapped (passed primary)':(g(r'Mapped:\s+([\d,]+)'),t['primary_mapped_passed']),'primary duplicates':(g(r'Duplicates:\s+([\d,]+)'),t['primary_dup'])}
checks['flagstat total pass+fail']=(sum(fs['total (QC-passed reads + QC-failed reads)']),t['records'])
bad=0
for k,(o,e) in checks.items():
    print(('PASS' if o==e else 'FAIL'),'qc_report/flagstat vs planted truth:',k,'observed',o,'planted',e); bad+=(o!=e)
print('PLANTED_TRUTH_MISMATCHES',bad)
PY
