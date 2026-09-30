import hashlib,json,os,subprocess
SK=r'F:\OpenScience\wt\atac-enhancer-gene-linking\skills\bio-atac-seq-enhancer-gene-linking'
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows=[]
for d,_,fs in os.walk(SK):
    for n in fs:
        p=os.path.join(d,n); b=open(p,'rb').read()
        rows.append({"path":os.path.relpath(p,SK).replace(os.sep,'/'),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
rows.sort(key=lambda r:r["path"].encode())
man="\n".join(f'{r["path"]}\t{r["bytes"]}\t{r["sha256"]}' for r in rows).encode()
ident=hashlib.sha256(man).hexdigest()
assert ident=="44385431f01902a0e18e305b483538009282bb44c5f19de4b53d5facd2b38976",ident
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
o=json.load(open(os.path.join(R,'..','initial-audit-20260930','source-identity.json'),encoding='utf-8'))
o["phase"]="final re-audit"; o["independent_auditor"]=True
o["candidate"].update({"content_sha256":ident,"status_before":"untracked Skill subtree only","status_after_execution":"untracked Skill subtree only; candidate files unchanged (identity recomputed after execution)",
 "content_manifest":{"file_count":len(rows),"bytes":sum(r["bytes"] for r in rows),"recipe":o["candidate"]["content_manifest"]["recipe"],"manifest_bytes":len(man)},"files":rows})
o["prior_audit_identity"]="67cda9c355b93f584f3d6628f847e8c0ba610059e102866e3d8e42096afd9cef"
o["tooling"].update({"tools_md_sha256":sha(os.path.join(R,'..','TOOLS.md')),"rubric_zip_sha256":sha(r'F:\optimizing-agent-science-skills\skill-auditor.zip'),
 "environment":o["tooling"]["environment"]+"; usage-guide create-command env egl-delta-tmp fingerprint 3f3bd2ef448b7b3130d28bbb918ed40077be9e2be4802f4b4590cd8b74f073a2 (tooling delta evidence, reused; not rebuilt)"})
o["candidate_cache_artifacts_after_execution"]=[]
open(os.path.join(R,'source-identity.json'),'w',encoding='utf-8').write(json.dumps(o,indent=2)+"\n")
print(ident,len(rows),sum(r["bytes"] for r in rows))
