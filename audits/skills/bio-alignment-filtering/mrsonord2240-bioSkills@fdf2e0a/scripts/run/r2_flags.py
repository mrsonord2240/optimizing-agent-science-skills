#!/usr/bin/env python3
"""Input 2 (regression, Variant A): every flag/MAPQ recipe in the FIXED SKILL.md, harvested by regex from its
fenced bash blocks and run, checked against bit arithmetic over ALL 4096 flag values (SYNTHETIC BAM, one read per
FLAG 0..4095, MAPQ (flag*7)%61). Also: flag table vs `samtools flags`, every 'N = a + b' arithmetic claim,
and the relabelled rows (forward/reverse/read1/read2/somatic)."""
import re, subprocess, sys, shlex
from lib import check, blocks, finish, sh

BAM, SK = sys.argv[1], sys.argv[2]
def sam(args):
    r = subprocess.run(['samtools', 'view'] + args + [BAM], capture_output=True, text=True)
    return r.returncode, [l.split('\t') for l in r.stdout.splitlines()], r.stderr
allrecs = [(int(l[1]), int(l[4])) for l in sam([])[1]]
assert len(allrecs) == 4096
def truth(pred): return sorted(f for f, q in allrecs if pred(f, q))

def predicate(args):
    """bit-arithmetic predicate for a samtools view arg list (-f -F -G -q only)"""
    f_req = F_ex = G_ex = 0; q = 0; i = 0; seen_G = False
    while i < len(args):
        a = args[i]
        if a == '-f': f_req |= int(args[i+1]); i += 2
        elif a == '-F': F_ex |= int(args[i+1]); i += 2
        elif a == '-G': G_ex |= int(args[i+1]); seen_G = True; i += 2
        elif a == '-q': q = int(args[i+1]); i += 2
        else: return None
    def p(f, mq):
        if (f & f_req) != f_req: return False
        if f & F_ex: return False
        if seen_G and (f & G_ex) == G_ex: return False
        return mq >= q
    return p

# 1. harvest every `samtools view ...` line from the SKILL.md bash blocks that has only -f/-F/-G/-q (+ -b/-o/file)
seen = {}
for head, lang, code in blocks(f'{SK}/SKILL.md'):
    if lang != 'bash':
        continue
    for line in code.splitlines():
        line = line.split('#')[0].strip()
        if not line.startswith('samtools view'):
            continue
        try:
            toks = shlex.split(line)[2:]
        except ValueError:
            continue
        cleaned = []; i = 0; ok = True
        while i < len(toks):
            t = toks[i]
            if t == '-o':
                i += 2
            elif t in ('-f', '-F', '-G', '-q'):
                cleaned += toks[i:i+2]; i += 2
            elif t == '-b' or t.endswith('.bam'):
                i += 1
            else:
                ok = False; break
        if ok and cleaned:
            seen.setdefault(tuple(cleaned), head)
print(len(seen), 'distinct flag/MAPQ recipes harvested from SKILL.md bash blocks')
for args, head in seen.items():
    p = predicate(list(args))
    rc, recs, err = sam(list(args))
    got = sorted(int(l[1]) for l in recs)
    check(f'[{head}] samtools view {" ".join(args)}', rc == 0 and got == truth(p), f'n={len(got)}')
# table-style recipes (in the assay table, not in bash blocks): all run too
tbl = {'-F 3328 -q 5': 'Long-read short-variant', '-f 2 -F 3328 -q 20': 'Germline', '-F 1280 -q 1': 'Somatic',
       '-F 1804 -q 30': 'ChIP', '-F 1804 -q 30 -f 2': 'ATAC', '-F 1284 -q 1': 'Coverage', '-F 256 -q 60': 'HISAT2 RNA',
       '-q 255': 'STAR', '-F 1024': 'SV'}
for a, nm in tbl.items():
    args = a.split(); p = predicate(args)
    rc, recs, _ = sam(args)
    check(f'[assay table: {nm}] {a}', sorted(int(l[1]) for l in recs) == truth(p), f'n={len(recs)}')

# 2. relabelled rows
_, recs, _ = sam(['-F', '20']); check('forward -F 20: no unmapped, no reverse', all(not int(l[1]) & 20 for l in recs) and len(recs) == len(truth(lambda f, q: not f & 20)), f'n={len(recs)}')
_, recs, _ = sam(['-f', '16', '-F', '4']); check('reverse -f 16 -F 4: all reverse, no unmapped', all(int(l[1]) & 16 and not int(l[1]) & 4 for l in recs) and len(recs) > 0, f'n={len(recs)}')
_, recs, _ = sam(['-f', '64', '-F', '2308']); check('read1 -f 64 -F 2308: only mapped primary read1', all(int(l[1]) & 64 and not int(l[1]) & 2308 for l in recs) and len(recs) == len(truth(lambda f, q: f & 64 and not f & 2308)), f'n={len(recs)}')
_, recs, _ = sam(['-f', '128', '-F', '2308']); check('read2 -f 128 -F 2308', all(int(l[1]) & 128 and not int(l[1]) & 2308 for l in recs) and len(recs) > 0, f'n={len(recs)}')
_, recs, _ = sam(['-F', '1280', '-q', '1']); n_supp = sum(1 for l in recs if int(l[1]) & 2048)
check('somatic -F 1280 -q 1 keeps supplementary (rationale in text)', n_supp == len(truth(lambda f, q: f & 2048 and not f & 1280 and q >= 1)) and n_supp > 0, f'supp kept {n_supp}')
_, recs, _ = sam(['-F', '1024']); check('SV recipe -F 1024 keeps supplementary reads', any(int(l[1]) & 2048 for l in recs))
for a in ('-F 2304', '-F 2308', '-F 3328', '-F 3332'):
    _, recs, _ = sam(a.split()); check(f'text: {a} removes every supplementary record', not any(int(l[1]) & 2048 for l in recs))
rc, recs, _ = sam(['-G', '3']); check('-G 3 == exclude reads having BOTH bits 1 and 2 (option table)', sorted(int(l[1]) for l in recs) == truth(lambda f, q: (f & 3) != 3))
rc, recs, _ = sam(['-f', '3']); check('-f 3 == ALL bits (option table)', sorted(int(l[1]) for l in recs) == truth(lambda f, q: (f & 3) == 3))
rc, recs, _ = sam(['-F', '3']); check('-F 3 == ANY bit excluded (option table)', sorted(int(l[1]) for l in recs) == truth(lambda f, q: not f & 3))

# 3. flag table + arithmetic claims vs samtools flags
names = {1: 'PAIRED', 2: 'PROPER_PAIR', 4: 'UNMAP', 8: 'MUNMAP', 16: 'REVERSE', 32: 'MREVERSE', 64: 'READ1', 128: 'READ2',
         256: 'SECONDARY', 512: 'QCFAIL', 1024: 'DUP', 2048: 'SUPPLEMENTARY'}
for v, nm in names.items():
    out = subprocess.run(['samtools', 'flags', str(v)], capture_output=True, text=True).stdout.strip().split('\t')
    check(f'flag table {v}: hex+name', int(out[0], 16) == v and out[-1] == nm, str(out))
out = subprocess.run(['samtools', 'flags', '99'], capture_output=True, text=True).stdout.strip()
check('`samtools flags 99` line quoted in SKILL.md is the real output', out == '0x63\t99\tPAIRED,PROPER_PAIR,MREVERSE,READ1', repr(out))
txt = open(f'{SK}/SKILL.md', encoding='utf-8').read()
arith = re.findall(r'^- (\d+) = ([\d +]+) \(([^)]*)\)', txt, re.M)
print(len(arith), 'flag-breakdown lines found')
check('7 breakdown lines present (1280,1284,1804,2304,2308,3328,3332)', len(arith) == 7)
for tot, parts, words in arith:
    ps = [int(x) for x in parts.split('+')]
    got = set(subprocess.run(['samtools', 'flags', tot], capture_output=True, text=True).stdout.strip().split('\t')[-1].split(','))
    check(f'{tot} = {parts.strip()}', sum(ps) == int(tot) and got == {names[p] for p in ps}, ','.join(sorted(got)))
    check(f'{tot}: prose "{words}" lists {len(ps)} terms', len(re.split(r'\+', words)) == len(ps))
finish()
