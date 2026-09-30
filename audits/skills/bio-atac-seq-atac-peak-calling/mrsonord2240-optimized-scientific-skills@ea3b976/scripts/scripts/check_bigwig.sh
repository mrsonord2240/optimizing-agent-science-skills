source /mnt/openscience/audits/bio-atac-seq-atac-peak-calling/reaudit-run/scripts/env.sh
python3 - <<'PY'
import struct,os
R=os.environ['R']
f=open(R+'/pass_macs3/final/pooled.bw','rb'); h=f.read(56)
magic,ver,zl,ctO,dO,idxO,fc,dc,asO,tsO,unc=struct.unpack('<IHHQQQHHQQI',h)
print('magic',hex(magic),'version',ver,'zoomLevels',zl,'fieldCount',fc)
f.seek(tsO); bc,mn,mx,sd,ssq=struct.unpack('<Qdddd',f.read(8+32))
print('basesCovered',bc,'min',mn,'max',round(mx,2),'mean',round(sd/bc,3))
# compare to bedGraph
bases=0;m=0;s=0.0
for l in open(R+'/pass_macs3/final/pooled.sorted.bdg'):
    c,a,b,v=l.split(); v=float(v); L=int(b)-int(a); bases+=L; s+=v*L; m=max(m,v)
print('bedGraph bases',bases,'max',round(m,2),'mean',round(s/bases,3))
PY
