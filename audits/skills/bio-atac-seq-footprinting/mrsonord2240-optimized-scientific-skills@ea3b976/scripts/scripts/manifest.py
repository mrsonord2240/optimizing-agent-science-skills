import hashlib,os,sys,json
root=sys.argv[1]; rows=[]
for r,d,f in os.walk(root):
    for n in f:
        full=os.path.join(r,n); p=os.path.relpath(full,root).replace(os.sep,'/'); b=open(full,'rb').read()
        rows.append((p,len(b),hashlib.sha256(b).hexdigest()))
rows.sort(key=lambda x:x[0].encode())
print(hashlib.sha256("\n".join(f"{p}\t{n}\t{h}" for p,n,h in rows).encode()).hexdigest(),len(rows),sum(r[1] for r in rows))
if len(sys.argv)>2: json.dump([dict(path=p,bytes=n,sha256=h) for p,n,h in rows],open(sys.argv[2],'w'),indent=1)
