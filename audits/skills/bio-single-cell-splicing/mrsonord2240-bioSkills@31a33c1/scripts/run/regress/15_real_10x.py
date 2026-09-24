"""Input 3b: REAL 10x v3 neuron subset (brie-tutorials, mouse) through brie-count droplet mode; quantify junction-read yield per cell per event and
cross-check with pysam (CB-tagged spliced reads whose N-gap equals a junction of the event)."""
import subprocess, gzip, numpy as np, pandas as pd, scanpy as sc, pysam
R='/mnt/openscience/audits/bio-single-cell-splicing/run'; D=f'/mnt/openscience/audit-envs/alternative-splicing/public-data/singlecell'; O=f'{R}/out/real_10x'
subprocess.run(['rm','-rf',O])
p=subprocess.run(['brie-count','-a',f'{D}/mouse_SE.lenient_50events.gff3','-s',f'{D}/10xData/neuron_1k_v3_possorted_genome_bam.50events.bam','-b',f'{D}/10xData/barcodes.tsv.gz','-o',O,'-p','8'],capture_output=True,text=True)
print('brie-count rc',p.returncode, (p.stdout+p.stderr).replace('\r','\n').strip().split('\n')[-3:])
a=sc.read_h5ad(f'{O}/brie_count.h5ad'); print(a)
dense=lambda m: np.asarray(m.todense() if hasattr(m,'todense') else m)
i1,i2,amb=[dense(a.layers[k]) for k in ['isoform1','isoform2','ambiguous']]
u=i1+i2
print('cells',a.n_obs,'events',a.n_vars)
print('mean unique reads / cell / event: %.4f ; median %.1f ; frac cell-event with >=1: %.4f ; >=5: %.5f'%(u.mean(), np.median(u),(u>=1).mean(),(u>=5).mean()))
print('mean skip(isoform2) / cell / event: %.4f ; incl(isoform1): %.4f; ambiguous: %.3f'%(i2.mean(), i1.mean(), amb.mean()))
print('events with total unique reads over all cells >=100:', int((u.sum(0)>=100).sum()),'of',a.n_vars)
# pysam: junction reads (N in CIGAR) with a valid CB
bc=set(l.strip() for l in gzip.open(f'{D}/10xData/barcodes.tsv.gz','rt'))
gff=pd.read_csv(f'{D}/mouse_SE.lenient_50events.gff3',sep='\t',comment='#',header=None)
bam=pysam.AlignmentFile(f'{D}/10xData/neuron_1k_v3_possorted_genome_bam.50events.bam')
nsp=0; ncb=0; ntot=0
for r in bam.fetch(until_eof=True):
    ntot+=1
    if r.has_tag('CB') and r.get_tag('CB') in bc:
        ncb+=1
        if any(op==3 for op,_ in r.cigartuples or []): nsp+=1
print('BAM records',ntot,'with whitelisted CB',ncb,'spliced (N) among those',nsp, 'frac %.3f'%(nsp/max(ncb,1)))
bam.close(); bam=pysam.AlignmentFile(f'{D}/10xData/neuron_1k_v3_possorted_genome_bam.50events.bam'); print('read length example', next(bam.fetch(until_eof=True)).query_length)
