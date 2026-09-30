import os,numpy as np,pysam
D=os.environ['ATACDATA']
for nm in ['GM12878_rep1','GM12878_rep2']:
    L=[]
    with pysam.AlignmentFile(f'{D}/encode/{nm}_filtered.chr1_1-30000000.bam') as b:
        for r in b.fetch():
            if r.is_proper_pair and r.is_read1 and 0<abs(r.template_length)<1500: L.append(abs(r.template_length))
    h,e=np.histogram(L,bins=300,range=(0,1500))
    print(nm,len(L)); print({int(e[i]):int(h[i]) for i in range(24,60)})
