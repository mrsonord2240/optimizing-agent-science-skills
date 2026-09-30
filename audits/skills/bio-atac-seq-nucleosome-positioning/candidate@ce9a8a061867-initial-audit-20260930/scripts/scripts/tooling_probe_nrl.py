import os, numpy as np, pysam
from scipy.signal import find_peaks
D=os.environ['ATACDATA']; bam=f'{D}/encode/GM12878_rep1_filtered.chr1_1-30000000.bam'
L=[abs(r.template_length) for r in pysam.AlignmentFile(bam,'rb').fetch() if r.is_proper_pair and r.is_read1 and 0<abs(r.template_length)<1500]
print('n',len(L))
h,e=np.histogram(L,bins=300,range=(0,1500))
p,_=find_peaks(h,distance=50,prominence=h.max()*0.05)
print('peaks',(e[p]+2.5).tolist(),'max',h.max(),'argmax bin start',e[h.argmax()])
print('hist 100-300 by 5bp',h[20:60].tolist())
