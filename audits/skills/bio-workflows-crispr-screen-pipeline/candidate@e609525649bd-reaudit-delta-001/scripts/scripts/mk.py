import pandas as pd,sys
R=sys.argv[1];D=sys.argv[2]
t=pd.read_csv(D+'/rra-qcpass/hap1.count.txt',sep='\t')
c=list(t.columns);print(c)
def mk(name,cols):
    u=t.copy();u.columns=c[:2]+cols;u.to_csv(f'{R}/{name}.txt',sep='\t',index=False)
mk('old_r',['P','S_r1','S_r2','S_r3'])
mk('old_rep',['P','S_rep1','S_rep2','S_rep3'])
mk('old_A',['P','S_A','S_B','S_C'])
mk('old_2',['P','S_1','S_2','S_3'])
mk('old_lower',['P','T18A','T18B','T18C'])
# FAIL + ungrouped: plasmid Gini gate failure with ungroupable names (use hap1 real qc table gate fail? use rr table with plasmid=S_x as endpoint)
mk('ungr_gatefail',['Pl','Alpha','Beta','Gamma'])
