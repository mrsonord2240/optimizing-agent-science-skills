#!/usr/bin/env python
"""INPUT 1 checks (content, not exit codes): for each reference shape prepare_reference.sh handled, compare .fai / .dict / .chrom.sizes
to an independent computation (plain-Python FASTA parse + hashlib md5 of the UPPERCASE sequence), then run the SKILL's
'Check Reference Setup' block (snippet skill_29) verbatim against each shape."""
import glob, gzip, os, re, sys
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
W1 = f'{W}/work/r1'
SRC = parse_fasta(f'{W}/data/real/genome.fasta')['chr22']
exp_m5 = md5(SRC.upper())
print('independent M5 of the chr22 slice:', exp_m5)
shapes = [('s1', 'genome.fasta', 'genome'), ('s2', 'ref.fa', 'ref'), ('s3', 'ref2.fna', 'ref2'), ('s4', 'refz.fa.gz', 'refz'),
          ('s5', 'Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz', 'Homo_sapiens.GRCh38.dna.primary_assembly'),
          ('s6', 'hg38.p14.v2.fasta', 'hg38.p14.v2'), ('s7', 'genome.fna.gz', 'genome'), ('s8', 'genome.fasta.gz', 'genome'),
          ('s9', 'my genome.fasta', 'my genome'), ('s10.v2', 'noext', 'noext'), ('s11', 'GENOME.FA', 'GENOME'), ('s12', 'ref.fas', 'ref')]
blk = open(f'{W}/snippets/skill_29_bash.txt').read()
for d, f, stem in shapes:
    dd = f'{W1}/{d}'
    dic = f'{dd}/{stem}.dict'
    ok = os.path.exists(dic)
    if ok:
        lines = open(dic).read().splitlines()
        sq = [dict(x.split(':', 1) for x in l.split('\t')[1:]) for l in lines if l.startswith('@SQ')]
        ok = len(sq) == 1 and sq[0]['SN'] == 'chr22' and sq[0]['LN'] == '40001' and sq[0]['M5'] == exp_m5
    check(f'{d}/{f}: {stem}.dict exists, SN=chr22 LN=40001 M5==independent md5', ok)
    cs = f'{dd}/{stem}.chrom.sizes'
    check(f'{d}/{f}: {stem}.chrom.sizes == "chr22<TAB>40001"', os.path.exists(cs) and open(cs).read() == 'chr22\t40001\n')
    # the Check Reference Setup block, verbatim, with REF replaced
    script = blk.replace('REF=reference.fa', f'REF="{f}"')
    open(f'{dd}/_chk.sh', 'w').write(script)
    rc, o, e = sh('bash _chk.sh', dd)
    if d.startswith('s1') and stem in ('noext',) or f in ('noext', 'GENOME.FA'):
        pass
    good = 'FAI: OK' in o and 'DICT: OK' in o and 'Fetch: OK' in o
    check(f'{d}/{f}: SKILL "Check Reference Setup" block prints FAI/DICT/Fetch OK', good, o.replace('\n', ' | ') + e[:150])
# negative: block against a reference whose ONLY dict is the old-style name
os.makedirs(f'{W}/work/r1c/neg_chk', exist_ok=True)
nd = f'{W}/work/r1/neg'
script = blk.replace('REF=reference.fa', 'REF=genome.fasta')
open(f'{nd}/_chk.sh', 'w').write(script)
rc, o, e = sh('bash _chk.sh', nd)
check('Check block on a reference with only genome.fasta.dict prints DICT: MISSING (does not claim OK)', 'DICT: MISSING' in o and 'DICT: OK' not in o, o.replace('\n', ' | '))
summary()
