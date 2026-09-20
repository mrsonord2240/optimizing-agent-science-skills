#!/usr/bin/env python3
"""Input 2: every -f/-F/-G/-q recipe in SKILL.md checked against bit arithmetic on ALL 4096 flag values
(synthetic BAM), plus every 'N = a + b + c' flag-breakdown claim in SKILL.md/usage-guide.md against
`samtools flags` (second, independent method)."""
import re, subprocess, sys, shlex
import pysam

BAM = sys.argv[1]
SK = sys.argv[2]   # skill dir copy
fails = []
def check(name, cond, detail=''):
    print(('PASS' if cond else 'FAIL'), name, detail)
    if not cond:
        fails.append(name)

def sam(args):
    out = subprocess.run(['samtools', 'view'] + args + [BAM], capture_output=True, text=True)
    if out.returncode != 0:
        return None, out.stderr
    return [l.split('\t') for l in out.stdout.splitlines()], ''

allrecs = [(int(l[1]), int(l[4])) for l in sam([])[0]]
assert len(allrecs) == 4096

def truth(pred):
    return sorted(f for f, q in allrecs if pred(f, q))

def run(name, args, pred):
    recs, err = sam(shlex.split(args))
    if recs is None:
        check(name, False, 'samtools error ' + err[:100]); return
    got = sorted(int(l[1]) for l in recs)
    exp = truth(pred)
    check(f'{name} [{args}]', got == exp, f'samtools={len(got)} bit-arithmetic={len(exp)}')

# ---- recipes as written (SKILL.md) ----
run('mapped',               '-F 4',              lambda f,q: not f&4)
run('unmapped',             '-f 4',              lambda f,q: f&4)
run('proper pair',          '-f 2',              lambda f,q: f&2)
run('remove dup',           '-F 1024',           lambda f,q: not f&1024)
run('primary -F 2304',      '-F 2304',           lambda f,q: not f&2304)
run('read1',                '-f 64',             lambda f,q: f&64)
run('read2',                '-f 128',            lambda f,q: f&128)
run('forward',              '-F 16',             lambda f,q: not f&16)
run('reverse',              '-f 16',             lambda f,q: f&16)
run('MAPQ30',               '-q 30',             lambda f,q: q>=30)
run('mapped+MAPQ30',        '-F 4 -q 30',        lambda f,q: not f&4 and q>=30)
run('standard 3332',        '-F 3332 -q 30',     lambda f,q: not f&3332 and q>=30)
run('germline',             '-f 2 -F 3328 -q 20',lambda f,q: (f&2) and not f&3328 and q>=20)
run('somatic',              '-F 3328 -q 1',      lambda f,q: not f&3328 and q>=1)
run('longread SNV',         '-F 3328 -q 5',      lambda f,q: not f&3328 and q>=5)
run('SV -F 1024',           '-F 1024',           lambda f,q: not f&1024)
run('ChIP 1804',            '-F 1804 -q 30',     lambda f,q: not f&1804 and q>=30)
run('ATAC 1804 -f 2',       '-F 1804 -q 30 -f 2',lambda f,q: not f&1804 and q>=30 and f&2)
run('HISAT2 RNA',           '-F 256 -q 60',      lambda f,q: not f&256 and q>=60)
run('STAR -q 255',          '-q 255',            lambda f,q: q>=255)
run('coverage 1284',        '-F 1284 -q 1',      lambda f,q: not f&1284 and q>=1)
run('usage 2308',           '-F 2308',           lambda f,q: not f&2308)
run('usage 2308 q30',       '-F 2308 -q 30',     lambda f,q: not f&2308 and q>=30)
run('usage -f 2 -F 3332 -q 20', '-f 2 -F 3332 -q 20', lambda f,q: (f&2) and not f&3332 and q>=20)
run('-f 3',                 '-f 3',              lambda f,q: (f&3)==3)
run('-f 1',                 '-f 1',              lambda f,q: f&1)
run('-G 3 (table: exclude reads with ALL bits set)', '-G 3', lambda f,q: (f&3)!=3)
run('tumor-normal -F 2308 count',   '-F 2308',   lambda f,q: not f&2308)

# ---- repeated -F (SKILL.md "Keep Only Primary Alignments": -F 256 -F 2048) ----
recs,_ = sam(['-F','256','-F','2048'])
got = sorted(int(l[1]) for l in recs)
combined = truth(lambda f,q: not f&2304)
only_last = truth(lambda f,q: not f&2048)
only_first = truth(lambda f,q: not f&256)
print('repeated -F: n=',len(got),' OR-semantics n=',len(combined),' last-wins n=',len(only_last),' first-wins n=',len(only_first))
check('repeated "-F 256 -F 2048" behaves as -F 2304 (SKILL.md line 84 claim)', got == combined)

# ---- -F 16 "forward strand only" also keeps unmapped reads? ----
recs,_ = sam(['-F','16'])
n_unm = sum(1 for l in recs if int(l[1]) & 4)
print('-F 16 ("Forward Strand Only") includes', n_unm, 'unmapped reads (flag&4) among', len(recs))
check('-F 16 output contains no unmapped reads (would need -F 20)', n_unm == 0, f'unmapped in output={n_unm}')

# ---- Read1 only -f 64 includes secondary/supp/dup/unmapped? ----
recs,_ = sam(['-f','64'])
print('-f 64 ("Keep Read1 Only") includes', sum(1 for l in recs if int(l[1])&2304), 'secondary/supplementary and',
      sum(1 for l in recs if int(l[1])&1024), 'duplicate records among', len(recs))

# ---- flag breakdown arithmetic claims (text -> numbers) ----
names = {1:'PAIRED',2:'PROPER_PAIR',4:'UNMAP',8:'MUNMAP',16:'REVERSE',32:'MREVERSE',64:'READ1',128:'READ2',
         256:'SECONDARY',512:'QCFAIL',1024:'DUP',2048:'SUPPLEMENTARY'}
claims = {
    2304: [256,2048], 3328: [256,1024,2048], 3332: [4,256,1024,2048], 1284: [4,256,1024],
    1804: [4,8,256,512,1024], 2308: [4,256,2048],
}
for tot, parts in claims.items():
    check(f'{tot} = {"+".join(map(str,parts))}', sum(parts) == tot)
    out = subprocess.run(['samtools','flags',str(tot)],capture_output=True,text=True).stdout.strip()
    tokens = set(out.split('\t')[-1].split(','))
    expect = {names[p] for p in parts}
    check(f'samtools flags {tot} names == claimed', tokens == expect, out)
# every 'N = a + b ...' claim in the two docs
for fn in ('SKILL.md', 'usage-guide.md'):
    txt = open(f'{SK}/{fn}', encoding='utf-8').read()
    for m in re.finditer(r'(\d+)\s*=\s*((?:\d+\s*\(?[a-z ]*\)?\s*\+\s*)+\d+)', txt):
        tot = int(m.group(1)); parts = [int(x) for x in re.findall(r'\d+', m.group(2))]
        check(f'doc arithmetic {fn}: {m.group(0)[:60]}', sum(parts) == tot)

# ---- Common FLAG Values table ----
table = {1:'PAIRED',2:'PROPER_PAIR',4:'UNMAP',8:'MUNMAP',16:'REVERSE',32:'MREVERSE',64:'READ1',128:'READ2',
         256:'SECONDARY',512:'QCFAIL',1024:'DUP',2048:'SUPPLEMENTARY'}
for v, nm in table.items():
    out = subprocess.run(['samtools','flags',str(v)],capture_output=True,text=True).stdout.strip()
    check(f'table flag {v} hex/name', out.split('\t')[-1] == nm and int(out.split('\t')[0],16) == v, out)
# usage-guide "Decoding FLAGS" examples
for v, want in ((99,'PAIRED,PROPER_PAIR,MREVERSE,READ1'), (147,'PAIRED,PROPER_PAIR,REVERSE,READ2')):
    out = subprocess.run(['samtools','flags',str(v)],capture_output=True,text=True).stdout.strip()
    check(f'usage-guide samtools flags {v}', out.split('\t')[-1] == want, out)

print('\nFAILS:', fails)
