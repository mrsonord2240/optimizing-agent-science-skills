"""library_complexity.py edge tests with synthetic BAMs (pysam-built). Truth planted."""
import pysam,subprocess,sys,json,os
S=sys.argv[1]; O=sys.argv[2]
hdr={'HD':{'VN':'1.6','SO':'coordinate'},'SQ':[{'SN':'chr1','LN':1000000},{'SN':'chrM','LN':16569}]}
def mk(path,reads):
    with pysam.AlignmentFile(path,'wb',header=hdr) as f:
        for i,(chrom,pos,rev,mq) in enumerate(sorted(reads,key=lambda x:(x[0]!='chr1',x[1]))):
            a=pysam.AlignedSegment(f.header); a.query_name=f'r{i}'; a.query_sequence='A'*50; a.flag=16 if rev else 0
            a.reference_id=f.header.get_tid(chrom); a.reference_start=pos; a.mapping_quality=mq; a.cigarstring='50M'; a.query_qualities=pysam.qualitystring_to_array('I'*50); f.write(a)
# 100 unique nuclear MAPQ60 positions x1, 100 chrM reads at same position (MAPQ 60) and 100 MAPQ0 reads at one position
reads=[('chr1',1000+10*i,False,60) for i in range(100)]+[('chrM',500,False,60)]*100+[('chr1',900000,False,0)]*100
mk(f'{O}/lc_chrM_mq0.bam',reads)
def run(*a):
    r=subprocess.run([sys.executable,S,*a],capture_output=True,text=True); return r.returncode,r.stdout.replace('\n',' '),r.stderr.strip().splitlines()[-1:] 
print('truth if chrM & MAPQ0 excluded (as usage-guide says MAPQ>=30, and chrM is not nuclear): total 100 NRF 1.0 PBC1 1.0 PBC2 inf')
print('no index:',run(f'{O}/lc_chrM_mq0.bam'))
pysam.index(f'{O}/lc_chrM_mq0.bam')
print('indexed:',run(f'{O}/lc_chrM_mq0.bam'))
# all singletons -> PBC2 inf
mk(f'{O}/lc_single.bam',[('chr1',1000+10*i,False,60) for i in range(50)]); pysam.index(f'{O}/lc_single.bam')
print('all singletons:',run(f'{O}/lc_single.bam'))
