"""Delta qualification: reverse the fix-log text edits on scratch copies, check certified identity + diff classes.
Edit pairs (old,new) were taken from the text-only fixer's edit scripts; the sha256 oracle (certified file hashes from the fix logs) validates them."""
import hashlib,json,os,shutil,subprocess,sys,difflib
SP=sys.argv[1]
edits={}
def cap(p,o,n): edits.setdefault(p,[]).append((o,n))
src=''.join(open(os.path.join(SP,f),encoding='utf-8').read() for f in('e1.py','e2.py'))
src=src.replace('from ed import ed','')
exec(src,{'ed':cap})
W='F:/OpenScience/wt/normalize-dv-lane1/skills/'
CERT={ # certified identity per skill
 'bio-data-visualization-volcano-and-ma-plots':'fa3ec8783a79b7c7a36fcf2d941d4fcc1aca6ab2ec3a8925e72fe6fa3a9af008',
 'bio-data-visualization-ggplot2-fundamentals':'be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120',
 'bio-data-visualization-matplotlib-fundamentals':'f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a'}
FILEHASH={'references/reconciliation-thresholds-pushback.md':'146c307647f145d91c059f339079ed488402ef91134b7eaeb53151a4d29e47c0','references/failure-modes.md':'edace425e0a4f7cd3a4644c856cc0243b026bbf3a28f12c98ddb214f3fc84826'}
for sid,cert in CERT.items():
    run=f'F:/OpenScience/audits/{sid}/delta-dv1-20261003'
    dst=f'{run}/scratch/{sid}'
    shutil.rmtree(dst,ignore_errors=True); shutil.copytree(W+sid,dst)
    cnt=0
    for p,l in edits.items():
        if f'/{sid}/' not in p: continue
        rel=p.split(f'/{sid}/')[1]; q=f'{dst}/{rel}'
        s=open(q,'rb').read().decode('utf-8')
        for old,new in l:
            assert s.count(new)==1,(rel,new[:60],s.count(new)); s=s.replace(new,old); cnt+=1
        open(q,'wb').write(s.encode('utf-8'))
    r=subprocess.run([sys.executable,'tools/skill_preflight.py','--offline',dst],cwd='F:/optimizing-agent-science-skills',capture_output=True,text=True)
    print(sid,'reversed edits:',cnt); print(r.stdout.strip().splitlines()[0])
    print('  CERT MATCH' if cert in r.stdout else '  CERT MISMATCH')
    # per-file diff summary candidate vs reverted
    for root,_,fs in os.walk(dst):
        for f in fs:
            a=os.path.join(root,f); rel=os.path.relpath(a,dst).replace(chr(92),'/'); b=f'{W}{sid}/{rel}'
            x=open(a,encoding='utf-8',newline='').read(); y=open(b,encoding='utf-8',newline='').read()
            if x!=y:
                ds=[l for l in difflib.unified_diff(x.splitlines(),y.splitlines(),'certified','candidate',lineterm='',n=0) if l[:1] in '+-' and l[:3] not in('+++','---')]
                print('  CHANGED',rel,len(ds),'diff lines')
                open(f'{run}/scripts/diff_{rel.replace("/","_")}.txt','w',encoding='utf-8').write('\n'.join(ds))
