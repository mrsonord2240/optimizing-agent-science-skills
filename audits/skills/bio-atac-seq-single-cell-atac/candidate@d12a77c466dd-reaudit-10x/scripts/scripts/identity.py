import hashlib,os,json,sys
root=sys.argv[1]; rows=[]
for r,d,f in os.walk(root):
    for n in f:
        p=os.path.join(r,n); rel=os.path.relpath(p,root).replace(chr(92),'/'); b=open(p,'rb').read()
        rows.append((rel.encode(),len(b),hashlib.sha256(b).hexdigest()))
rows.sort()
m=hashlib.sha256("\n".join(f"{a.decode()}\t{b}\t{c}" for a,b,c in rows).encode()).hexdigest()
print(json.dumps({"manifest_sha256":m,"file_count":len(rows),"byte_total":sum(b for _,b,_ in rows),"files":[{"path":a.decode(),"bytes":b,"sha256":c} for a,b,c in rows]}))
