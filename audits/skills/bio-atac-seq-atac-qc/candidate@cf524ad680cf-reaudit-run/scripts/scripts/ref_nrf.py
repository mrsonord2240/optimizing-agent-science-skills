import pysam,sys,collections
c=collections.Counter()
for r in pysam.AlignmentFile(sys.argv[1]).fetch(until_eof=True):
    if r.is_unmapped or r.is_secondary or r.is_supplementary or not r.is_proper_pair or not r.is_read1: continue
    if r.reference_name in('chrM','MT') or r.mapping_quality<30 or r.template_length==0: continue
    s=min(r.reference_start,r.next_reference_start); c[(r.reference_name,s,s+abs(r.template_length))]+=1
h=collections.Counter(c.values()); t=sum(c.values()); d=len(c)
print(t,d,round(d/t,4),round(h[1]/d,4),round(h[1]/h[2],3))
