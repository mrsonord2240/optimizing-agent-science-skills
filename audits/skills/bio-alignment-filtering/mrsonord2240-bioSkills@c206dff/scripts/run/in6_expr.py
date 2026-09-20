#!/usr/bin/env python3
"""Input 6: 'Expression Filtering' (-e) and 'Filter by Read Group' (-r/-R) snippets, run verbatim on real BAMs,
checked against pysam/CIGAR arithmetic. Small SYNTHETIC BAM for reads lacking an RG tag."""
import os, subprocess, sys, shlex, re
import pysam

AFD = os.environ['AFDATA']
W = sys.argv[1]; os.makedirs(W, exist_ok=True)
fails = []
def check(name, cond, detail=''):
    print(('PASS' if cond else 'FAIL'), name, detail)
    if not cond: fails.append(name)
def st(args, bam):
    r = subprocess.run(f'samtools view {args} {bam}', shell=True, capture_output=True, text=True)
    return r.returncode, [l.split('\t') for l in r.stdout.splitlines()], r.stderr.strip()
def names(rows): return sorted((x[0], int(x[1])) for x in rows)

human = f'{AFD}/human/test.paired_end.sorted.bam'
g1k = f'{AFD}/1000g/HG00349.chr20_1400000-1500000.bam'
rna = f'{AFD}/human/test.rna.paired_end.sorted.bam'
H = list(pysam.AlignmentFile(human))
def tag(r, t):
    return r.get_tag(t) if r.has_tag(t) else None
def key(r): return (r.query_name, r.flag)

# 1. [NM] >= 2
rc, rows, err = st("-e '[NM] >= 2'", human)
exp = sorted(key(r) for r in H if tag(r, 'NM') is not None and tag(r, 'NM') >= 2)
check("-e '[NM] >= 2' == tag truth", rc == 0 and names(rows) == exp, f'{len(rows)} vs {len(exp)} {err[:80]}')

# 2. cigar variable (SKILL.md verbatim uses `cigar=~"^[0-9]+S"`)
rc, rows, err = st("-e 'cigar=~\"^[0-9]+S\" && rname==\"chr1\"'", human)
print('verbatim SKILL.md cigar expr (rname chr1) -> rc', rc, 'rows', len(rows), 'stderr:', err[:200])
check('SKILL.md `cigar=~"^[0-9]+S"` expression is accepted by samtools 1.24', rc == 0, err[:160])
rc, rows, err = st("-e 'cigar=~\"^[0-9]+S\" && rname==\"chr22\"'", human)
exp = sorted(key(r) for r in H if r.cigartuples and r.cigartuples[0][0] == 4)
print('adapted to chr22: rc', rc, 'n', len(rows), 'truth (leading soft clip)', len(exp), 'err', err[:120])
if rc == 0:
    check('cigar=~ leading soft-clip == CIGAR truth', names(rows) == exp)
# documented alternative variables: sclen / ncigar
rc, rows, err = st("-e 'sclen > 0'", human)
exp_sc = sorted(key(r) for r in H if r.cigartuples and any(op == 4 for op, _ in r.cigartuples))
check("-e 'sclen > 0' == reads with any soft clip", rc == 0 and names(rows) == exp_sc, f'{len(rows)} vs {len(exp_sc)}')

# 3. combined flags + expression
rc, rows, err = st("-F 2308 -q 30 -e '[NM] <= 5 && [AS] >= 100'", human)
exp = sorted(key(r) for r in H if not r.flag & 2308 and r.mapping_quality >= 30
             and tag(r, 'NM') is not None and tag(r, 'NM') <= 5 and tag(r, 'AS') is not None and tag(r, 'AS') >= 100)
check("-F 2308 -q 30 -e '[NM] <= 5 && [AS] >= 100' == truth", rc == 0 and names(rows) == exp, f'{len(rows)} vs {len(exp)}')

# 4. sclen / qlen < 0.2  ("Drop reads with low mapped fraction")
def qlen_sc(r):
    if not r.cigartuples: return None
    q = sum(n for op, n in r.cigartuples if op in (0, 1, 4, 7, 8))
    s = sum(n for op, n in r.cigartuples if op == 4)
    return q, s
rc, rows, err = st("-e 'sclen / qlen < 0.2'", human)
exp_keep, unm_kept = [], 0
for r in H:
    v = qlen_sc(r)
    if v is None:      # unmapped: qlen=0 -> sclen/qlen is 0/0 (null?)
        continue
    if v[1] / v[0] < 0.2: exp_keep.append(key(r))
got = names(rows)
extra = [k for k in got if k not in set(exp_keep)]
print("'sclen / qlen < 0.2': samtools", len(got), "truth (mapped reads, <20% soft-clipped)", len(exp_keep),
      "; unmapped kept:", sum(1 for k in got if k[1] & 4))
check("-e 'sclen / qlen < 0.2' == truth on mapped reads", sorted(exp_keep) == [k for k in got if not k[1] & 4])
frac_dropped = sum(1 for r in H if qlen_sc(r) and qlen_sc(r)[1] / qlen_sc(r)[0] >= 0.2)
print('reads with >=20% soft clip dropped by it:', frac_dropped)

# 5. ![NM]
rc, rows, err = st("-e '![NM]'", human)
exp = sorted(key(r) for r in H if tag(r, 'NM') is None)
check("-e '![NM]' returns only reads missing NM (2 unmapped)", rc == 0 and names(rows) == exp, f'{len(rows)} vs {len(exp)}')
# silent-empty trap: expression on a tag absent from the BAM
rc, rows, err = st("-e '[XY] >= 2'", human)
print("-e on absent tag [XY]: rc", rc, "rows", len(rows), "(silently empty, no warning):", repr(err))

# 6. read groups
G = list(pysam.AlignmentFile(g1k))
rgs = sorted({r.get_tag('RG') for r in G})
print('1000g RG IDs:', rgs, ' LB values:', {h['LB'] for h in pysam.AlignmentFile(g1k).header.to_dict()['RG']})
for rg in rgs:
    rc, rows, err = st(f'-r {rg}', g1k)
    exp = sorted(key(r) for r in G if r.get_tag('RG') == rg)
    check(f'-r {rg} == RG tag truth', rc == 0 and names(rows) == exp, f'{len(rows)}')
lb = pysam.AlignmentFile(g1k).header.to_dict()['RG'][0]['LB']
rc, rows, err = st(f'-r {lb}', g1k)
print(f'SKILL.md example uses a LIBRARY-style name (-r library_A): `-r {lb}` (a real LB value) returns', len(rows), 'reads')
rc, rows, err = st(f'-l {lb}', g1k)
print(f'`-l {lb}` (the actual library option, not in the Skill) returns', len(rows), 'of', len(G))
open(f'{W}/rg_list.txt', 'w').write(rgs[0] + '\n')
rc, rows, err = st(f'-R {W}/rg_list.txt', g1k)
check('-R rg_list.txt (one ID per line) == truth', names(rows) == sorted(key(r) for r in G if r.get_tag('RG') == rgs[0]), f'{len(rows)}')
# synthetic: reads with no RG tag are also emitted by -r
syn = f'{W}/syn_rg.bam'
hdr = {'HD': {'VN': '1.6', 'SO': 'unsorted'}, 'SQ': [{'SN': 'c', 'LN': 1000}], 'RG': [{'ID': 'a'}, {'ID': 'b'}]}
with pysam.AlignmentFile(syn, 'wb', header=hdr) as fo:
    for i, rg in enumerate(['a', 'a', 'a', 'b', 'b', 'b', None, None, None]):
        a = pysam.AlignedSegment(fo.header); a.query_name = f's{i}'; a.flag = 0; a.reference_id = 0
        a.reference_start = 10 * i; a.mapping_quality = 60; a.cigartuples = [(0, 10)]
        a.query_sequence = 'A' * 10; a.query_qualities = pysam.qualitystring_to_array('I' * 10)
        if rg: a.set_tag('RG', rg)
        fo.write(a)
rc, rows, err = st('-r a', syn)
print('SYNTHETIC: 3 reads RG=a, 3 RG=b, 3 no RG; `-r a` returns', len(rows), '->', sorted(x[0] for x in rows))
check('-r a returns only RG a reads (SKILL.md: "single read group")', len(rows) == 3, f'{len(rows)} (samtools 1.24 man: reads with no RG are also output)')

# 7. multi-part composite request (scope-boundary style): proper pairs, insert 100-500, <=20% soft clip, NM<=3, MAPQ>=30
expr = "tlen >= 100 && tlen <= 500 && sclen / qlen < 0.2 && [NM] <= 3"
rc, rows, err = st(f"-f 2 -F 3332 -q 30 -e '{expr}'", human)
def ok(r, tl):
    v = qlen_sc(r)
    return (r.flag & 2) and not r.flag & 3332 and r.mapping_quality >= 30 and v and v[1] / v[0] < 0.2 \
        and tag(r, 'NM') is not None and tag(r, 'NM') <= 3 and tl
exp_pos = sorted(key(r) for r in H if ok(r, 100 <= r.template_length <= 500))
exp_abs = sorted(key(r) for r in H if ok(r, 100 <= abs(r.template_length) <= 500))
print('composite: naive tlen>=100&&tlen<=500 keeps', len(rows), '; truth positive-tlen only', len(exp_pos), '; abs(tlen) truth', len(exp_abs))
check('naive positive-tlen expression matches its own truth', names(rows) == exp_pos)
check('naive tlen expression keeps BOTH mates of each in-range pair (would need abs)', names(rows) == exp_abs, f'{len(rows)} vs {len(exp_abs)}')
expr2 = "((tlen >= 100 && tlen <= 500) || (tlen <= -100 && tlen >= -500)) && sclen / qlen < 0.2 && [NM] <= 3"
rc, rows2, err = st(f"-f 2 -F 3332 -q 30 -e '{expr2}'", human)
check('symmetric tlen expression == abs(tlen) truth', names(rows2) == exp_abs, f'{len(rows2)}')
# orphaned mates after any read-level filter
from collections import Counter
c = Counter(x[0] for x in rows2); print('after composite filter: templates with one mate only =', sum(1 for v in c.values() if v == 1), 'of', len(c))

# 8. STAR real BAM: [NH]==1 vs -q 255
rc, r1, _ = st("-e '[NH]==1'", rna); rc, r2, _ = st('-q 255', rna)
check("real STAR BAM: -e '[NH]==1' == -q 255 (SKILL.md STAR sentinel claim)", names(r1) == names(r2), f'{len(r1)} vs {len(r2)}')
print('\nFAILS:', fails)
