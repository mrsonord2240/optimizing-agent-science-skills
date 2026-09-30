import re,subprocess,os
doc=open(os.environ['SKILL']+'/references/method-reference.md',encoding='utf-8').read()
m=re.search(r"```bash\n(awk -F'.*?danpos_diff/condition2-condition1.positions.integrative.xls > shifted.tsv)\n```",doc,re.S)
cmd=m.group(1).replace('danpos_diff/condition2-condition1.positions.integrative.xls',os.environ['NP']+'/work/a4/diff/trt-ctl.positions.integrative.xls')
out=os.environ['NP']+'/../../audits/bio-atac-seq-nucleosome-positioning/reaudit-run/out'
subprocess.run(['bash','-c',cmd],cwd=out,check=True)
f=os.environ['NP']+'/work/a4/diff/trt-ctl.positions.integrative.xls'
hdr=open(f).readline().rstrip('\n').split('\t');print(hdr[:14])
rows=[l.rstrip('\n').split('\t') for l in open(out+'/shifted.tsv')][1:]
allr=[l.rstrip('\n').split('\t') for l in open(f)][1:]
pl=[r for r in allr if 10_000_000<=int(r[3])<12_000_000]
tp=[r for r in rows if 10_000_000<=int(r[3])<12_000_000]; fp=[r for r in rows if int(r[3])>=12_000_000]
print('planted-half positions',len(pl),'passing',len(tp),'recall',len(tp)/len(pl),'false (unshifted half)',len(fp))
