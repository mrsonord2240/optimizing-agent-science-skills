# Independent output assertions on reaudit-run/work/<case>. Planted truth: K562-only = k.narrowPeak peaks not overlapping GM1/GM2 peaks.
import csv,glob,os,bisect,sys
W=os.path.join(os.path.dirname(__file__),'..','work'); P=r'F:\OpenScience\audits\bio-atac-seq-differential-accessibility\initial-20260930\work'
def bed(fn):
    return [(l.split('\t')[0],int(l.split('\t')[1]),int(l.split('\t')[2])) for l in open(fn) if l.strip()]
gm=bed(P+r'\gm1.narrowPeak')+bed(P+r'\gm2.narrowPeak'); k=bed(P+r'\k.narrowPeak')
def ov(a,b): return a[0]==b[0] and a[1]<b[2] and b[1]<a[2]
byc={}
for g in gm: byc.setdefault(g[0],[]).append(g)
kon=[x for x in set(k) if not any(ov(x,g) for g in byc.get(x[0],[]))]
print('planted K562-only peaks:',len(kon))
def hits(sites):
    n=0;op=0
    for c,s,e,f in sites:
        if any(ov((c,s,e),x) for x in kon if x[0]==c): n+=1; op+= f>0
    return n,op
for case,pfx in [('default','d'),('native','n'),('args','mypfx'),('edger','e'),('design','des'),('sva','s'),('sva1','s1'),('sva4','s4'),('notxdb','nt'),('labels_ok','lo')]:
    d=os.path.join(W,case)
    try: rows=list(csv.DictReader(open(f'{d}/{pfx}_annotated.csv')))
    except Exception as ex: print(case,'NO CSV',ex); continue
    op=sum(1 for _ in open(f'{d}/{pfx}_opened.bed')); cl=sum(1 for _ in open(f'{d}/{pfx}_closed.bed'))
    sites=[(r['seqnames'],int(r['start']),int(r['end']),float(r['Fold'])) for r in rows]
    fd=max(float(r['FDR']) for r in rows); mf=min(abs(s[3]) for s in sites)
    h=hits(sites); pdfs=sorted(os.path.basename(x) for x in glob.glob(f'{d}/*.pdf'))
    print(f'{case}: rows={len(rows)} opened={op} closed={cl} sum_ok={op+cl==len(rows)} maxFDR={fd:.4f} min|Fold|={mf:.2f} K562only_hits={h[0]} frac_opened={h[1]/max(h[0],1):.3f} pdfs={pdfs} annot_cols={"annotation" in rows[0]}')
for case,pfx in [('args','mypfx'),('svanull','sn'),('null','nl')]:
    d=os.path.join(W,case); print(case,'files:',sorted(os.listdir(d)), 'bed sizes', [os.path.getsize(x) for x in glob.glob(f'{d}/*.bed')])
