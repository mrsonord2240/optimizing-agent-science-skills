"""Independent fragment-level NRF/PBC (ENCODE-style: distinct (chr,start,end,strand-of-read1) fragments). Reference implementation for audit comparison."""
import pysam,sys,json
from collections import Counter
bam=sys.argv[1]
c=Counter();tot=0;q30=Counter();t30=0
with pysam.AlignmentFile(bam,'rb') as bf:
    for r in bf.fetch():
        if r.is_unmapped or r.is_secondary or r.is_supplementary or not r.is_paired or not r.is_read1 or r.mate_is_unmapped: continue
        s=min(r.reference_start,r.next_reference_start); e=max(r.reference_end, r.next_reference_start+1) if r.template_length==0 else s+abs(r.template_length)
        k=(r.reference_name,s,e); c[k]+=1; tot+=1
        if r.mapping_quality>=30: q30[k]+=1; t30+=1
def m(c,tot):
    h=Counter(c.values());d=len(c)
    return dict(total_fragments=tot,distinct=d,NRF=d/tot,PBC1=h[1]/d,PBC2=(h[1]/h[2] if h[2] else None))
print(json.dumps({'all':m(c,tot),'mapq30':m(q30,t30)},indent=1))
