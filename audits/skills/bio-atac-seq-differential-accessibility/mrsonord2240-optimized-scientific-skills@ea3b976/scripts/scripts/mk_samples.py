import csv,sys
D='/mnt/openscience/audit-envs/atac-seq/public-data/encode/'
P='/mnt/openscience/audits/bio-atac-seq-differential-accessibility/initial-20260930/work/'
b=[D+f'{s}_filtered.chr1_1-30000000.bam' for s in ('GM12878_rep1','GM12878_rep2','K562_rep1','K562_rep2')]
pk=[P+'gm1.narrowPeak',P+'gm2.narrowPeak',P+'k.narrowPeak',P+'k.narrowPeak']
def w(fn,cond,tissue=None):
    with open(fn,'w',newline='') as f:
        c=csv.writer(f); h=['SampleID','Condition','Replicate']+(['Tissue'] if tissue else [])+['bamReads','Peaks','PeakCaller']; c.writerow(h)
        for i,s in enumerate(['GM1','GM2','K1','K2']):
            c.writerow([s,cond[i],[1,2,1,2][i]]+([tissue[i]] if tissue else [])+[b[i],pk[i],'narrow'])
w('work/samples.csv',['control','control','treated','treated'])
w('work/samples_tissue.csv',['control','control','treated','treated'],['A','B','A','B'])
w('work/samples_labels.csv',['GM12878','GM12878','K562','K562'])
