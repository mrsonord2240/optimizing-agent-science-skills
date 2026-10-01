import hashlib, os, sys, json
def manifest(root):
    rows=[]
    for dp,dn,fn in os.walk(root):
        for f in fn:
            p=os.path.join(dp,f); rel=os.path.relpath(p,root).replace(os.sep,'/')
            b=open(p,'rb').read()
            rows.append((rel,len(b),hashlib.sha256(b).hexdigest()))
    rows.sort(key=lambda r:r[0].encode('utf-8'))
    s='\n'.join(f"{r}\t{n}\t{h}" for r,n,h in rows)
    return hashlib.sha256(s.encode('utf-8')).hexdigest(), rows
if __name__=='__main__':
    for root in sys.argv[1:]:
        h,rows=manifest(root); print(h, len(rows), sum(r[1] for r in rows), root)
