import hashlib,os,sys,json
root=sys.argv[1]
fs={}
for r,_,f in os.walk(root):
    for n in f:
        p=os.path.join(r,n); fs[os.path.relpath(p,root).replace(os.sep,'/')]=open(p,'rb').read()
rows=[{"path":k,"bytes":len(fs[k]),"sha256":hashlib.sha256(fs[k]).hexdigest()} for k in sorted(fs,key=lambda v:v.encode())]
lines="\n".join(f"{r['path']}\t{r['bytes']}\t{r['sha256']}" for r in rows)
print(json.dumps({"manifest_sha256":hashlib.sha256(lines.encode()).hexdigest(),"files":rows},indent=1))
