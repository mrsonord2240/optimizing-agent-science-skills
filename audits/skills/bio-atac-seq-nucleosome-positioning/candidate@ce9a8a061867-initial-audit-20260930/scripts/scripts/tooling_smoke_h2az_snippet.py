"""Verbatim region_frag_size snippet from references/method-reference.md (needs np, pysam imported by caller)."""
import os, numpy as np, pysam
D=os.environ['ATACDATA']; bam=pysam.AlignmentFile(f'{D}/encode/GM12878_rep1_filtered.chr1_1-30000000.bam','rb')
def region_frag_size(bam, region):
    sizes = [abs(r.template_length) for r in bam.fetch(*region)
             if r.is_proper_pair and r.is_read1 and 100 < abs(r.template_length) < 300]
    return np.mean(sizes) if sizes else np.nan
tss=[l.split('\t') for l in open(f'{D}/annotation/gencode_v29_protein_coding_tss.chr1.bed')]
tss=[t for t in tss if 1.2e6<int(t[1])<29e6][:200]
m=[region_frag_size(bam,(t[0],int(t[1])-500,int(t[1])+500)) for t in tss]
m=np.array(m); print('regions',len(m),'nan',int(np.isnan(m).sum()),'mean of means %.1f sd %.1f'%(np.nanmean(m),np.nanstd(m)))
assert 150<np.nanmean(m)<220
print('PASS h2az snippet runs; mean fragment 100-300 bp at TSS windows plausible')
