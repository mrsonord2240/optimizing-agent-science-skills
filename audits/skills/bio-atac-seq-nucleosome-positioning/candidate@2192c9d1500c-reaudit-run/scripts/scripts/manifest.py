import hashlib,os,sys
r=sys.argv[1];ls=[]
for dp,_,fs in os.walk(r):
    for f in fs:
        p=os.path.join(dp,f);b=open(p,'rb').read()
        ls.append((os.path.relpath(p,r).replace(chr(92),'/'),len(b),hashlib.sha256(b).hexdigest()))
ls.sort(key=lambda x:x[0].encode())
print(hashlib.sha256('\n'.join(f'{p}\t{n}\t{h}' for p,n,h in ls).encode()).hexdigest(),len(ls),sum(n for _,n,_ in ls))
