import json,shutil
r=json.load(open('../reaudit-10x/report.json',encoding='utf-8'))
c=r['static_score']['categories']
c['functional_suitability']['score']=12; c['functional_suitability']['note']="Covers ATAC 1.x/2.x and ARC inputs, three ecosystems, WNN and both AMULET routes; ARC blacklist QC limitation is now stated with measured numbers"
r['static_score']['subtotal']=sum(v['score'] for v in c.values())
a=r['dynamic_score']['inputs'][1]
a['assertions'][3]={"text":"ARC-substituted blacklist QC is documented with its sensitivity","result":"PASS","note":"Delta: SKILL.md now states the ratio stays near 0 (max 0.004 on PBMC 3k vs up to 0.18 from ATAC singlecell.csv) and the 0.05 cut removes no cells; numbers reproduced from reaudit-10x evidence"}
a['assertions_passed']=4
a['note']="exit 0 in 14m (reused identity-matched run: signac_workflow.R bytes unchanged); 2392/2687 cells, 8 clusters; blacklist limitation now documented"
d=r['dynamic_score']; d['assertion_pass_rate']={"passed":31,"total":31}
sw=round(r['static_score']['subtotal']*0.4,1); dw=round(d['execution_avg']*0.6,1)
r['final'].update(static_weighted=sw,dynamic_weighted=dw,score=round(sw+dw))
r['recommendations']=[]
json.dump(r,open('report.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
pass
n=json.load(open('logs/identity_new.json'))
s=json.load(open('../reaudit-10x/source-identity.json'))
s['phase']='final re-audit (delta, RA-1 sentence)'; s['independent_auditor']=True
s['candidate'].update(manifest_sha256=n['manifest_sha256'],file_count=n['file_count'],byte_total=n['byte_total'],status='untracked, uncommitted; identity verified live; diff vs d12a77c4 is exactly one 179-byte SKILL.md insertion; no __pycache__')
s['files']=n['files']; s['supersedes_audit_identity']='d12a77c466ddc748e86d80ac482766aa212e3b31aa1d6bd3388a827bf59dbec0'
json.dump(s,open('source-identity.json','w',encoding='utf-8'),indent=2)
