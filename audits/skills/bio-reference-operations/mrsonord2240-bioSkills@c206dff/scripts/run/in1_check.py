#!/usr/bin/env python
"""INPUT 1 checks: verify the outputs of prepare_reference.sh / samtools faidx / samtools dict against an
INDEPENDENT computation (plain-Python FASTA parse, hashlib MD5, Picard's dict) and run the pysam dict snippet verbatim."""
import hashlib, os, re, subprocess, sys

W = '/mnt/openscience/audits/bio-reference-operations/run'
sys.path.insert(0, W)
FAILS = []


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (' -- ' + detail if detail else ''))
    if not ok:
        FAILS.append(name)


def parse_fasta(path):
    """independent parse: returns list of (name, seq, linebases, linewidth, offset)"""
    out = []
    with open(path, 'rb') as f:
        data = f.read()
    pos = 0
    lines = data.split(b'\n')
    off = 0
    cur = None
    for ln in lines[:-1] if data.endswith(b'\n') else lines:
        L = len(ln) + 1
        if ln.startswith(b'>'):
            if cur:
                out.append(cur)
            cur = {'name': ln[1:].split()[0].decode(), 'seq': [], 'lb': None, 'lw': None, 'off': off + L}
        else:
            if cur['lb'] is None:
                cur['lb'] = len(ln)
                cur['lw'] = L
            cur['seq'].append(ln.decode())
        off += L
    out.append(cur)
    for c in out:
        c['seq'] = ''.join(c['seq'])
    return out


def read_fai(p):
    return [l.split('\t') for l in open(p).read().splitlines()]


def read_dict(p):
    sq = []
    for l in open(p).read().splitlines():
        if l.startswith('@SQ'):
            d = dict(x.split(':', 1) for x in l.split('\t')[1:])
            sq.append(d)
    return sq


for label, d, fa in (('A synth .fa', f'{W}/work/in1/A', 'ref.fa'), ('B real .fasta', f'{W}/work/in1/B', 'genome.fasta')):
    ref = parse_fasta(f'{d}/{fa}')
    # ---- fai
    fai = read_fai(f'{d}/{fa}.fai')
    exp = [[c['name'], str(len(c['seq'])), str(c['off']), str(c['lb']), str(c['lw'])] for c in ref]
    check(f'{label}: .fai equals independent (name,len,offset,linebases,linewidth)', fai == exp, f'{fai} vs {exp}' if fai != exp else str(fai[0]))
    # ---- chrom.sizes
    stem = fa[:-3] if fa.endswith('.fa') else fa
    cs = open(f'{d}/{stem}.chrom.sizes').read().splitlines()
    check(f'{label}: chrom.sizes equals name<TAB>len', cs == [f"{c['name']}\t{len(c['seq'])}" for c in ref])
    # ---- dict (whichever file the script produced)
    dpath = f'{d}/{stem}.dict'
    sq = read_dict(dpath)
    ok = len(sq) == len(ref)
    for s, c in zip(sq, ref):
        m5 = hashlib.md5(c['seq'].upper().encode()).hexdigest()
        ok &= (s['SN'] == c['name'] and int(s['LN']) == len(c['seq']) and s['M5'] == m5)
    check(f'{label}: dict SN/LN/M5 equal independent (M5 = md5 of UPPERCASE sequence, no newlines)', ok)
    # dict name the GATK/Picard convention wants: replace extension -> <stem>.dict
    conv = os.path.splitext(f'{d}/{fa}')[0] + '.dict'
    check(f'{label}: dict exists under the name GATK/Picard look for ({os.path.basename(conv)})', os.path.exists(conv),
          'present' if os.path.exists(conv) else 'only ' + ', '.join(sorted(x for x in os.listdir(d) if x.endswith('.dict'))))

# soft-masked lowercase block must not change M5 (uppercase-normalised)
raw = open(f'{W}/data/synthetic/synth.fa').read()
check('synthetic FASTA really contains lowercase (soft-mask) so the M5 check above is meaningful', re.search(r'[acgt]{50}', raw) is not None)

# --- header claims in SKILL.md "Dictionary Format" vs real output
first = open(f'{W}/work/in1/A/ref.dict').read().splitlines()
check('SKILL dict example says "@HD VN:1.0 SO:unsorted" (real 1.24 output)', first[0] == '@HD\tVN:1.0\tSO:unsorted', first[0])
check('SKILL dict example says UR:file:reference.fa (relative); real UR is absolute file:///…', first[1].split('\t')[4].startswith('UR:file:///'), first[1].split('\t')[4][:40])
picard = open(f'{W}/work/in1/A/picard.dict').read().splitlines()
check('Picard 3.5.0 dict has the same SN/LN/M5 as samtools dict', [l.split('\t')[:4] for l in picard[1:]] == [l.split('\t')[:4] for l in first[1:]])

# --- pysam create_dict_header, verbatim from SKILL.md
import pysam
src = open(f'{W}/snippets/skill_24_python.txt').read().replace("'reference.fa'", f"'{W}/work/in1/A/ref.fa'")
ns = {}
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(src, ns)
print(buf.getvalue().strip())
h = ns['header']
check('create_dict_header prints the 3 contigs with lengths', buf.getvalue().count(' bp') == 3)
check('create_dict_header dict is loadable by pysam.AlignmentHeader.from_dict', len(pysam.AlignmentHeader.from_dict(h).references) == 3)
check('create_dict_header result has NO M5 (differs from samtools dict / .dict file)', 'M5' not in h['SQ'][0])
check('create_dict_header writes no file (function returns dict only; nothing usable by GATK)', not os.path.exists(f'{W}/work/in1/A/header.dict'))

print('\nFAILS:', FAILS)
