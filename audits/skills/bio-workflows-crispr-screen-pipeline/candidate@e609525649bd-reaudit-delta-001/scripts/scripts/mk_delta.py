import json,hashlib,os,sys
S,R=sys.argv[1],sys.argv[2]
r=json.load(open(S+'/report.json',encoding='utf-8'))
r['meta']['evaluated_on']='2026-10-04'
pb=r['veto_gates']['research_veto']['practice_boundaries']
pb['detail']="Failed gates must be stated, not hidden; core-essential PR-AUC gate blocks novel hits. N-01 resolved: qc.py now prints QC INCOMPLETE and exits 1 when replicates cannot be grouped."
sc=r['static_score']['categories']
sc['functional_suitability'].update(score=11,note="Gini matches MAGeCK (F-12 fixed). N-01 resolved: the default pattern groups A375 C902R1_P1D14 names (Pearson 0.780, QC FAIL) and ungroupable names give QC INCOMPLETE, exit 1. Re-scored in delta mode.")
sc['agent_usability'].update(score=15,note="Rule 1 restates stated commitments and runs the route command (cn-correction 3/3, rra 2/3 under Haiku, carried). F-16 resolved: qc.md sources 0.8 as the MAGeCK-VISPR guideline and gives outlier advice only when one replicate is clearly lower.")
r['static_score']['subtotal']=sum(c['score'] for c in sc.values())
d=r['dynamic_score']
i=d['inputs'][0]
i['status_flag']='✅'
i['note']="Gini equals MAGeCK on real HAP1 and A375; real replicate Pearson 0.789 and 0.780 fails the 0.8 gate as the Skill states; rra.py on the QC-passing table ran (carried). N-01 resolved: default pattern on A375 groups the replicates, QC FAIL exit 1."
a=i['assertions'][-1]
a['result']='PASS'
a['note']="Delta run: A375 default pattern groups to one condition (0.780, QC FAIL, exit 1); ungroupable names print QC INCOMPLETE, exit 1; a failed gate still reports QC FAIL; pattern= override gives QC PASS exit 0"
i['specialized']=56;i['total']=92;i['assertions_passed']=5
d['assertions_passed']=28
d['assertion_pass_rate']=round(28/29*100,1)
n=len(d['inputs'])
d['execution_avg']=round(sum(x['total'] for x in d['inputs'])/n,1)
d['layer1_avg']=round(sum(x['basic'] for x in d['inputs'])/n,1)
d['layer2_avg']=round(sum(x['specialized'] for x in d['inputs'])/n,1)
f=r['final']
f['static_weighted']=round(r['static_score']['subtotal']*0.4,1)
f['dynamic_weighted']=round(d['execution_avg']*0.6,1)
f['score']=round(f['static_weighted']+f['dynamic_weighted'])
r['key_strengths'].append("Delta re-audit (e609525649bd): qc.py cannot report QC PASS with the replicate check skipped; old default-pattern names still group")
r['recommendations']=[x for x in r['recommendations'] if not (x['title'].startswith('qc.py prints QC PASS') or x['title'].startswith('Replicate-Pearson gate has no action'))]
json.dump(r,open(R+'/report.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
print(r['static_score']['subtotal'],d['execution_avg'],d['layer1_avg'],d['layer2_avg'],d['assertion_pass_rate'],f)
# source identity
s=json.load(open(S+'/source-identity.json',encoding='utf-8'))
root=s['candidate']['path'];files=[]
for dd,_,fs in os.walk(root):
    for x in fs:
        p=os.path.join(dd,x);b=open(p,'rb').read()
        files.append({'path':os.path.relpath(p,root).replace(os.sep,'/'),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
files.sort(key=lambda z:z['path'])
s['files']=files
s['candidate']['content_sha256']='e609525649bd5394ec66676a9025250ab8c27db23039968d44c6dfeb0c872c81'
s['candidate']['status_before']='uncommitted; delta over certified 05e557c86e77: routes/qc.md and scripts/qc.py only (sha256 manifest diff)'
s['candidate']['status_after_execution']='unchanged; skill_preflight --offline --shape PASS, 19 files'
s['tooling']={'routing_cases':'not rerun: route table, route names and script arguments unchanged (delta mode); routing evidence carried from reaudit-002'}
s.pop('routing_model',None)
json.dump(s,open(R+'/source-identity.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
