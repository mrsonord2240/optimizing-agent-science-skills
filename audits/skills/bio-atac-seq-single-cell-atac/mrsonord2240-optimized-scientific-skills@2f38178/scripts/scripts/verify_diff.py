import hashlib
p=r'F:\OpenScience\wt\atac-single-cell-atac\skills\bio-atac-seq-single-cell-atac\SKILL.md'
b=open(p,'rb').read().decode('utf-8')
ins="; few ARC peaks overlap the blacklist, so this ratio stays near 0 (max 0.004 on PBMC 3k, versus up to 0.18 from the ATAC `singlecell.csv` column) and the 0.05 cut removes no cells"
print('insert count',b.count(ins),'len bytes',len(ins.encode()))
old=b.replace(ins,'')
print('reverted sha256',hashlib.sha256(old.encode()).hexdigest())
print('expected prior 920e9abbc7a9f5f279d2ae36bbcba7cb3a47fdf288888db7e3ff68ed10e5fadf')
