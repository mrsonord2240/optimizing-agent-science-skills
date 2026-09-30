import hashlib,os,sys
r=sys.argv[1];fs=[]
for d,_,f in os.walk(r):
    for x in f: fs.append(os.path.relpath(os.path.join(d,x),r).replace(chr(92),'/'))
fs.sort(key=lambda s:s.encode())
lines=[];tot=0
for f in fs:
    b=open(os.path.join(r,f),'rb').read();tot+=len(b)
    lines.append(f"{f}\t{len(b)}\t{hashlib.sha256(b).hexdigest()}")
print(len(fs),tot);print(hashlib.sha256("\n".join(lines).encode()).hexdigest())
print("\n".join(lines))
