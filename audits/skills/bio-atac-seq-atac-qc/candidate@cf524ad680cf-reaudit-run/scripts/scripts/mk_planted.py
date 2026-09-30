"""SYNTHETIC fixtures with planted truth (reaudit, independent of fixer's).
PE BAM: chr1 fragments: 100 positions x1, 50 x2, 10 x5 (=250 pairs, 160 distinct) MAPQ60;
 plus 300 chrM pairs MAPQ60 (excluded), plus 80 chr1 pairs MAPQ5 (excluded by mapq30).
 Expect defaults: total 250 distinct 160 NRF .64 PBC1 .625 PBC2 2.0. --min-mapq 0 --exclude-contigs '': total 630.
SE BAM: same 250 reads with 5' positions (fwd/rev mix) -> same counts in single mode.
bigWig+BED: 3 chroms; TSS peak planted 21x at + and - strand TSS (flank 1, center 21)."""
import pysam,random,sys,pyBigWig,os
random.seed(11); O=sys.argv[1]
hdr={'HD':{'VN':'1.6','SO':'coordinate'},'SQ':[{'SN':'chr1','LN':50_000_000},{'SN':'chrM','LN':16569}]}
def mk(name,paired):
    recs=[]; n=0
    def add(chrom,pos,ins,mq,rev=False):
        nonlocal n; n+=1
        a=pysam.AlignedSegment(); a.query_name=f'q{n}'; a.query_sequence='A'*50; a.query_qualities=pysam.qualitystring_to_array('I'*50)
        a.cigarstring='50M'; a.mapping_quality=mq; tid=0 if chrom=='chr1' else 1; a.reference_id=tid
        if paired:
            b=pysam.AlignedSegment(); b.query_name=a.query_name; b.query_sequence='A'*50; b.query_qualities=a.query_qualities
            b.cigarstring='50M'; b.mapping_quality=mq; b.reference_id=tid
            a.reference_start=pos; b.reference_start=pos+ins-50
            a.flag=1|2|32|64; b.flag=1|2|16|128
            a.next_reference_id=tid; b.next_reference_id=tid; a.next_reference_start=b.reference_start; b.next_reference_start=pos
            a.template_length=ins; b.template_length=-ins; recs.extend([a,b])
        else:
            a.reference_start=pos; a.flag=16 if rev else 0; recs.append(a)
    p=1_000_000
    for mult,cnt in ((1,100),(2,50),(5,10)):
        for _ in range(cnt):
            p+=random.randrange(500,900); ins=random.choice([60,200,210,400])
            for _ in range(mult): add('chr1',p,ins,60)
    for _ in range(300): add('chrM',random.randrange(100,16000),200,60)
    for _ in range(80): add('chr1',random.randrange(20_000_000,21_000_000),200,5)
    recs.sort(key=lambda r:(r.reference_id,r.reference_start))
    with pysam.AlignmentFile(name,'wb',header=hdr) as f:
        for r in recs: f.write(r)
    pysam.index(name)
mk(f'{O}/planted_pe.bam',True); mk(f'{O}/planted_se.bam',False)
# TSS bigWig
bw=pyBigWig.open(f'{O}/planted.bw','w'); bw.addHeader([('chr1',5_000_000),('chr2',5_000_000)])
import numpy as np
tss=[('chr1',1_000_000,'+'),('chr1',2_000_000,'-'),('chr2',3_000_000,'+')]
for chrom in ('chr1','chr2'):
    v=np.ones(5_000_000)
    for c,t,s in tss:
        if c==chrom:
            # asymmetric: signal high just upstream of TSS in TSS orientation; center 21, flank 1
            v[t-50:t+50]=21.0
    bw.addEntries(chrom,0,values=[float(x) for x in v[:5_000_000]],span=1,step=1) if False else None
    # use bedGraph-style entries for speed
    starts=[0];ends=[];vals=[]
    segs=sorted([t for c,t,s in tss if c==chrom]); prev=0
    ch=[];st=[];en=[];va=[]
    for t in segs:
        ch.append(chrom);st.append(prev);en.append(t-50);va.append(1.0)
        ch.append(chrom);st.append(t-50);en.append(t+50);va.append(21.0); prev=t+50
    ch.append(chrom);st.append(prev);en.append(5_000_000);va.append(1.0)
    bw.addEntries(ch,st,ends=en,values=va)
bw.close()
open(f'{O}/tss_bed6.bed','w').write('chr1\t1000000\t1000001\tg1\t0\t+\nchr1\t2000000\t2000001\tg2\t0\t-\nchr2\t3000000\t3000001\tg3\t0\t+\n')
# gene intervals: minus strand TSS = end-1
open(f'{O}/gene_bed6.bed','w').write('chr1\t999000\t1004000\tg1\t0\t+\nchr1\t1996000\t2000001\tg2\t0\t-\n')
open(f'{O}/absent_chrom.bed','w').write('chrZ\t1000000\t1000001\tg1\t0\t+\n')
open(f'{O}/empty.bed','w').write('')
open(f'{O}/bed3.bed','w').write('chr1\t1000000\t1000001\n')
open(f'{O}/mixed.bed','w').write('chr1\t1000000\t1000001\tg1\t0\t+\nchrZ\t1000000\t1000001\tg1\t0\t+\nchr1\t10\t11\tg4\t0\t+\n')
