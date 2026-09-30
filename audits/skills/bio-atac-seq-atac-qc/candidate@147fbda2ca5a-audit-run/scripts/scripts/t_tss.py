"""Planted-truth tests for encode_tss_enrichment.py. Synthetic bigWig: chrT 100kb; signal 1 background, 21 at [50000,50100) around plus-strand TSS at 50050."""
import pyBigWig,subprocess,sys,json,os
S=sys.argv[1]; O=sys.argv[2]
bw=pyBigWig.open(f'{O}/planted.bw','w'); bw.addHeader([('chrT',100000)])
# background 1 everywhere, peak 21 in [50000,50100)
bw.addEntries(['chrT']*3,[0,50000,50100],ends=[50000,50100,100000],values=[1.0,21.0,1.0]); bw.close()
def run(bed,extra=()):
    open(f'{O}/t.bed','w').write(bed)
    r=subprocess.run([sys.executable,S,f'{O}/planted.bw',f'{O}/t.bed',*extra],capture_output=True,text=True)
    return r.returncode,r.stdout.replace('\n',' '),r.stderr.strip()[-200:]
print('truth: center mean 21, flank 1 -> 21.0')
print('A BED6 TSS 1bp plus (50050):', run('chrT\t50050\t50051\tg1\t0\t+\n'))
print('B BED6 gene interval minus strand [start=30000,end=50051): true TSS=end-1=50050 ->', run('chrT\t30000\t50051\tg1\t0\t-\n'))
print('C plus-strand gene interval [50050,70000) ->', run('chrT\t50050\t70000\tg1\t0\t+\n'))
print('D BED6+ extra column after strand (gene name col7), true plus:', run('chrT\t50050\t50051\tg1\t0\t+\tGENE\n'))
print('E chromosome absent from bigWig (naming mismatch chr vs no chr):', run('T\t50050\t50051\tg1\t0\t+\n'))
print('F empty BED:', run(''))
print('G 3-column BED (no strand) plus:', run('chrT\t50050\t50051\n'))
