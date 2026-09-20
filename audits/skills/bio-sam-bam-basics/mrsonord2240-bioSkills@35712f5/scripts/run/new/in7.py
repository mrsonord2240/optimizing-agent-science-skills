"""Input 7 (NEW): a tiny HAND-WRITTEN SAM with planted truth, then the Skill's own claims and the rewritten
examples/view_bam.py against it.
Prompt: 'I wrote this 32-record SAM by hand (every CIGAR op, every FLAG bit, unplaced/placed unmapped reads, secondary/
supplementary, "*" SEQ, three kinds of pair). Decode every record for me, count reads by FLAG, tell me bases consumed per
CIGAR op, and show it with the view_bam.py helper as SAM, BAM, unindexed BAM, unmapped-only BAM, empty BAM, CRAM (with
and without the reference), then convert it around the formats with convert_formats.sh.'

The expected values in TRUTH are written by hand from the SAM spec (v1, sec 1.4) BEFORE running anything; they are not
computed by the code under test. Records are generated from (contig, pos, cigar) only to keep SEQ consistent.
"""
import collections, os, re, sys
os.environ['AUDIT_INPUT'] = '7'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regress'))
from chk import check, note, sh
import pysam

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = RUN + '/data/in7'
sh(f'rm -rf {W}; mkdir -p {W}')
VB = RUN + '/skill/examples/view_bam.py'
CV = RUN + '/skill/examples/convert_formats.sh'
ENV = {'REF_PATH': '', 'REF_CACHE': ''}

REF = {'ctgA': 'ACGTTGCAAC' * 20, 'ctgB': 'GGATCCTTAA' * 10}
with open(W + '/ref.fa', 'w') as fh:
    for k, v in REF.items():
        fh.write(f'>{k}\n{v}\n')
sh(f'samtools faidx {W}/ref.fa')

# name, flag, contig, pos, mapq, cigar, rnext, pnext, tlen ;; hand-written expectations: qlen (len of SEQ, H excluded), reflen
ROWS = [
    ('r_M',   0,   'ctgA', 5,   60, '10M',                    '*', 0, 0),
    ('r_I',   0,   'ctgA', 5,   60, '4M2I4M',                 '*', 0, 0),
    ('r_D',   0,   'ctgA', 5,   60, '4M3D4M',                 '*', 0, 0),
    ('r_N',   0,   'ctgA', 5,   60, '4M20N4M',                '*', 0, 0),
    ('r_S',   0,   'ctgA', 5,   60, '3S6M2S',                 '*', 0, 0),
    ('r_H',   0,   'ctgA', 5,   60, '2H6M2H',                 '*', 0, 0),
    ('r_EQX', 0,   'ctgA', 5,   60, '4=1X4=',                 '*', 0, 0),
    ('r_P',   0,   'ctgA', 5,   60, '3M2P3M',                 '*', 0, 0),
    ('r_all', 0,   'ctgA', 30,  60, '1H2S3M1I2M2D1M1N2M1S1H', '*', 0, 0),
    ('u_placed',   4, 'ctgA', 50, 0, '*',                     '*', 0, 0),
    ('u_unplaced', 4, '*',    0,  0, '*',                     '*', 0, 0),
    ('sec',   256, 'ctgA', 60,  0,  '10M',                    '*', 0, 0),
    ('supp',  2048, 'ctgA', 70, 30, '5M10H',                  '*', 0, 0),
    ('p1',    99,  'ctgA', 10,  60, '20M',                    '=', 61, 71),
    ('p1',    147, 'ctgA', 61,  60, '20M',                    '=', 10, -71),
    ('m1',    73,  'ctgA', 100, 60, '20M',                    '=', 100, 0),
    ('m1',    133, 'ctgA', 100, 0,  '*',                      '=', 100, 0),
    ('x1',    65,  'ctgA', 120, 60, '20M',                    'ctgB', 30, 0),
    ('x1',    129, 'ctgB', 30,  60, '20M',                    'ctgA', 120, 0),
]
for b in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048):
    ROWS.append((f'fb_{b}', b, 'ctgA', 150, 10, '*' if b == 4 else '5M', '*', 0, 0))
ROWS.append(('qcdup', 1536, 'ctgA', 160, 60, '10M', '*', 0, 0))

# hand-written truth: key "name/flag" -> (SEQ length, reference span or None)
TRUTH = {'r_M/0': (10, 10), 'r_I/0': (10, 8), 'r_D/0': (8, 11), 'r_N/0': (8, 28), 'r_S/0': (11, 6), 'r_H/0': (6, 6),
         'r_EQX/0': (9, 9), 'r_P/0': (6, 6), 'r_all/0': (12, 11), 'sec/256': (0, 10), 'supp/2048': (5, 5),
         'p1/99': (20, 20), 'p1/147': (20, 20), 'm1/73': (20, 20), 'x1/65': (20, 20), 'x1/129': (20, 20), 'qcdup/1536': (10, 10)}
# hand-written FLAG names (SAM spec table 1.4.2)
NAMES = {1: 'PAIRED', 2: 'PROPER_PAIR', 4: 'UNMAP', 8: 'MUNMAP', 16: 'REVERSE', 32: 'MREVERSE', 64: 'READ1', 128: 'READ2',
         256: 'SECONDARY', 512: 'QCFAIL', 1024: 'DUP', 2048: 'SUPPLEMENTARY'}
COMP = {'A': 'C', 'C': 'G', 'G': 'T', 'T': 'A'}


def seq_for(row):
    name, flag, c, pos, mq, cig, *_ = row
    if name == 'sec':
        return '*'
    if cig == '*':
        return 'ACGTACGTAC'
    r = REF[c]
    p = pos - 1
    q = []
    for n, op in re.findall(r'(\d+)([MIDNSHP=X])', cig):
        n = int(n)
        if op in 'M=':
            q.append(r[p:p + n]); p += n
        elif op == 'X':
            q.append(''.join(COMP[r[p + i]] for i in range(n))); p += n
        elif op in 'DN':
            p += n
        elif op in 'IS':
            q.append('A' * n)
    return ''.join(q)


lines = ['@HD\tVN:1.6\tSO:unsorted', '@SQ\tSN:ctgA\tLN:200', '@SQ\tSN:ctgB\tLN:100', '@RG\tID:g1\tSM:hand']
for row in ROWS:
    s = seq_for(row)
    q = '*' if s == '*' else 'I' * len(s)
    extra = ['SA:Z:ctgB,10,+,10S5M,60,0;'] if row[0] == 'supp' else []
    lines.append('\t'.join(map(str, [*row[:9], s, q, *extra])))
open(W + '/hand.sam', 'w', newline='\n').write('\n'.join(lines) + '\n')
check('hand-written SAM has 32 records (hand count) by `samtools view -c`', sh(f'samtools view -c {W}/hand.sam')[1].strip() == '32' and len(ROWS) == 32, len(ROWS))

# ---------------- A. FLAG decoding, counts, TLEN, CIGAR consumption ----------------
skill = open(RUN + '/skill/SKILL.md', encoding='utf-8').read()
tbl = re.findall(r'^\| 0x([0-9a-f]+) \| (\d+) \| ([^|]+) \|$', skill.split('## Common Flags')[1].split('###')[0], re.M)
check('Skill FLAG table: 12 rows, hex == decimal on every row, decimals are 1..2048 doubling', len(tbl) == 12 and all(int(h, 16) == int(d) for h, d, _ in tbl) and [int(d) for _, d, _ in tbl] == [1 << i for i in range(12)], [(h, d) for h, d, _ in tbl][:3])
key = {1: 'paired', 2: 'proper', 4: 'unmapped', 8: 'mate unmapped', 16: 'reverse strand', 32: 'mate reverse', 64: 'first', 128: 'second',
       256: 'secondary', 512: 'failed qc', 1024: 'duplicate', 2048: 'supplementary'}
check('Skill FLAG table meaning column matches the SAM spec for all 12 bits (hand keyword per bit)', all(key[int(d)] in m.lower() for _, d, m in tbl), [(d, m) for _, d, m in tbl])
ok = True
for b, n in NAMES.items():
    o = sh(f'samtools flags {b}')[1].split('\t')[2].strip()
    ok &= (o == n)
check('`samtools flags <bit>` == spec name for all 12 single bits (hand names)', ok, 'ok')
o = sh('samtools flags 1536; samtools flags 73; samtools flags 133; samtools flags 65; samtools flags 129')[1]
check('samtools flags 1536/73/133/65/129 decode as the hand truth', [l.split('\t')[2] for l in o.strip().splitlines()] == ['QCFAIL,DUP', 'PAIRED,MUNMAP,READ1', 'PAIRED,UNMAP,READ2', 'PAIRED,READ1', 'PAIRED,READ2'], o.strip().replace('\n', ' | '))
o = sh('samtools flags PAIRED,PROPER_PAIR,REVERSE,READ2; samtools flags 0x93; samtools flags 99')[1]
check('Skill: mnemonics -> number (147), hex input works, and the Skill\'s 99/147 strings verbatim', o.strip().splitlines()[0].split('\t')[1] == '147' and 'PAIRED,PROPER_PAIR,MREVERSE,READ1' in o and '0x63' in skill and 'PAIRED,PROPER_PAIR,REVERSE,READ2' in skill, o.strip().replace('\n', ' | '))

# counts (hand-counted): total 32; unmapped-by-flag 4; secondary 2; supplementary 2; dup 2; qcfail 2; read1 4; read2 4; paired 7; mapq>=30 16
exp = {'': 32, '-f 4': 4, '-F 4': 28, '-F 256': 30, '-F 2048': 30, '-F 2304': 28, '-f 1024': 2, '-f 512': 2, '-f 64': 4, '-f 128': 4, '-f 1': 7, '-q 30': 16}
got = {k: int(sh(f'samtools view -c {k} {W}/hand.sam')[1]) for k in exp}
check('view -c with -f/-F/-q equals hand-counted truth for 12 filters (incl. Skill\'s `-F 2304` and plain `-c`)', got == exp, {k: (got[k], exp[k]) for k in exp if got[k] != exp[k]} or got)
check('Skill: `samtools view -c input.bam` counts secondary/supplementary too (32), `-F 2304` primary only (28) - on the SAM file', got[''] == 32 and got['-F 2304'] == 28, (got[''], got['-F 2304']))

with pysam.AlignmentFile(W + '/hand.sam') as sam:
    recs = list(sam)
by = {f'{r.query_name}/{r.flag}': r for r in recs}
check('pysam reads all 32 records, keys unique', len(recs) == 32 and len(by) == 32, len(by))
bad = []
for k, (ql, rl) in TRUTH.items():
    r = by[k]
    qlen = 0 if r.query_sequence is None else len(r.query_sequence)
    if qlen != ql or (r.reference_length != rl):
        bad.append((k, qlen, r.reference_length, ql, rl))
check('SEQ length and reference span of every CIGAR record equal the hand truth (pysam reference_length; SEQ excludes H) - Skill formulas', not bad, bad[:3] or f'{len(TRUTH)} records')
# Skill formulas evaluated independently on the CIGAR text of the SAM
ops = {'query': set('MIS=X'), 'ref': set('MDN=X')}
okf = True
for row in ROWS:
    if row[5] in ('*',) or row[0] == 'sec':
        continue
    cig = row[5]
    ql = sum(int(n) for n, o in re.findall(r'(\d+)([MIDNSHP=X])', cig) if o in 'MIS=X')
    rl = sum(int(n) for n, o in re.findall(r'(\d+)([MIDNSHP=X])', cig) if o in 'MDN=X')
    k = f'{row[0]}/{row[1]}'
    okf &= (k not in TRUTH) or TRUTH[k] == (ql, rl)
check('Skill formulas ("span = sum M/D/N/=/X"; "SEQ length = sum M/I/S/=/X, H excluded") reproduce every hand-written expectation', okf, 'ok')
# consumption table row by row via pysam/htslib's own cigar-type table (an implementation independent of the Skill text)
rows = re.findall(r'^\| ([MIDNSHPX=, ]+) \| (yes|no) +\| (yes|no) +\|$', skill.split('Consumes reference')[1].split('Aligned reference span')[0], re.M)
claims = {}
for ops_, q, r in rows:
    for o in [x.strip() for x in ops_.split(',')]:
        claims[o] = (q == 'yes', r == 'yes')
check('Skill consumption table parsed: all 9 ops present', set(claims) == set('MIDNSHP=X'), claims)
bad = []
for o, (cq, cr) in claims.items():
    a = pysam.AlignedSegment()
    a.reference_start = 0
    a.cigartuples = [(0, 3), ('MIDNSHP=X'.index(o), 5), (0, 3)]
    a.query_sequence = 'A' * (6 + (5 if cq else 0))
    got_q = a.query_length
    got_r = a.reference_length
    if (got_q - 6 == 5) != cq or (got_r - 6 == 5) != cr:
        bad.append((o, got_q, got_r))
check('each op consumption claim (query yes/no, reference yes/no) equals htslib/pysam behaviour for all 9 ops', not bad, bad or 'all 9 match')
rN = by["r_N/0"]
pos_n = rN.get_reference_positions()
check('N (skipped region) not covered: r_N `4M20N4M` at POS 5 covers 8 reference positions (5-8 and 29-32), reference_end spans 28; get_reference_positions has 8', len(pos_n) == 8 and rN.reference_end - rN.reference_start == 28 and pos_n[3] == 7 and pos_n[4] == 28, (len(pos_n), pos_n))
# soft vs hard
rS = by['r_S/0']; rH = by['r_H/0']
check('soft clip stays in SEQ (r_S query_length 11, aligned 6), hard clip does not (r_H query_length 6, inferred 10)', rS.query_length == 11 and rS.query_alignment_length == 6 and rH.query_length == 6 and rH.infer_read_length() == 10, (rS.query_length, rH.query_length, rH.infer_read_length()))
# TLEN
a, b = by['p1/99'], by['p1/147']
check('TLEN: + on leftmost mate (99, POS 10), - on rightmost (147, POS 61), |TLEN| = 80-10+1 = 71; 0 when mate unmapped (m1) and when mates are on different contigs (x1)',
      a.template_length == 71 and b.template_length == -71 and by['m1/73'].template_length == 0 and by['m1/133'].template_length == 0 and by['x1/65'].template_length == 0 and by['x1/129'].template_length == 0,
      (a.template_length, b.template_length))
check('unmapped mate placed at its mate\'s position: m1/133 has reference ctgA, start 99, no CIGAR; samtools view shows POS 100', by['m1/133'].reference_name == 'ctgA' and by['m1/133'].reference_start == 99 and by['m1/133'].cigarstring is None, (by['m1/133'].reference_name, by['m1/133'].reference_start))
check('"*" SEQ (secondary record): query_sequence None, samtools prints "* *"', by['sec/256'].query_sequence is None and sh(f'samtools view {W}/hand.sam | awk \'$1=="sec"{{print $10,$11}}\'')[1].strip() == '* *', by['sec/256'].query_sequence)
check('SA:Z tag on the supplementary record has the Skill\'s documented shape rname,pos,strand,CIGAR,mapQ,NM;', re.fullmatch(r'\w+,\d+,[+-],[0-9MIDNSHP=X]+,\d+,\d+;', by['supp/2048'].get_tag('SA')) is not None, by['supp/2048'].get_tag('SA'))
for b_ in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048):
    r = by[f'fb_{b_}/{b_}']
    ok = getattr(r, {1: 'is_paired', 2: 'is_proper_pair', 4: 'is_unmapped', 8: 'mate_is_unmapped', 16: 'is_reverse', 32: 'mate_is_reverse', 64: 'is_read1', 128: 'is_read2', 256: 'is_secondary', 512: 'is_qcfail', 1024: 'is_duplicate', 2048: 'is_supplementary'}[b_])
    if not ok:
        check(f'pysam property for bit {b_}', False, r.flag)
check('pysam is_* property for each of the 12 single-bit records is True (only that bit set)', True, 'no failures logged above')

# ---------------- B. view_bam.py matrix ----------------
sh(f'cd {W}; samtools view -b -o unsorted.bam hand.sam; samtools view -b -f 4 -o unmapped_only_unsorted.bam hand.sam; samtools sort -o unmapped_only.bam unmapped_only_unsorted.bam; cp unmapped_only.bam unmapped_only_noidx.bam; samtools index unmapped_only.bam; samtools sort -o hand.bam hand.sam; cp hand.bam hand_noidx.bam; samtools index hand.bam')
open(W + '/empty.sam', 'w').write('@HD\tVN:1.6\tSO:coordinate\n@SQ\tSN:ctgA\tLN:200\n')
sh(f'cd {W}; samtools view -b -o empty_noidx.bam empty.sam; cp empty_noidx.bam empty.bam; samtools index empty.bam')
sh(f'cd {W}; samtools view -C -T ref.fa -o hand.cram hand.bam; samtools index hand.cram; samtools view -C -T ref.fa -o unmapped_only.cram unmapped_only.bam')
rc, o, e = sh(f'samtools view -c {W}/hand.cram -T {W}/ref.fa; samtools view -c {W}/unmapped_only.cram')
check('CRAMs built: hand.cram has 32 records, unmapped_only.cram 4 (truth -f 4)', o.split() == ['32', '4'], o.split())


def vb(path, limit='', ref='', env=None):
    """run view_bam.py; return rc, stdout, stderr"""
    rc, o, e = sh(f'python {VB} {path} {limit} {ref}; echo "rc=$?" >&2', env=env)
    m = re.search(r'rc=(\d+)', e)
    return int(m.group(1)), o, re.sub(r'rc=\d+\s*$', '', e)


def stats(o):
    m = re.search(r'Mapped: (\d+)\s+Unmapped: (\d+)\s+\(from (\w+)\)', o)
    return (int(m.group(1)), int(m.group(2)), m.group(3)) if m else None


cases = [('hand.sam', (28, 4, 'scan')), ('hand.bam', (28, 4, 'index')), ('hand_noidx.bam', (28, 4, 'scan')), ('unsorted.bam', (28, 4, 'scan')),
         ('unmapped_only.bam', (0, 4, 'index')), ('unmapped_only_noidx.bam', (0, 4, 'scan')), ('empty.bam', (0, 0, 'index')),
         ('empty_noidx.bam', (0, 0, 'scan')), ('empty.sam', (0, 0, 'scan'))]
for f, expect in cases:
    rc, o, e = vb(f'{W}/{f}', 40)
    truth_m = int(sh(f'samtools view -c -F 4 {W}/{f}')[1])
    truth_u = int(sh(f'samtools view -c -f 4 {W}/{f}')[1])
    st = stats(o)
    check(f'view_bam.py {f}: rc 0, "Mapped/Unmapped" = {expect[:2]} = samtools -F4/-f4 truth ({truth_m}/{truth_u}), from {expect[2]}', rc == 0 and st == expect and st[:2] == (truth_m, truth_u) and 'Traceback' not in e, f'rc={rc} stats={st} err={e.strip()[:100]}')
# CRAM with/without reference
rc, o, e = vb(f'{W}/hand.cram', 40, '', ENV)
check('view_bam.py hand.cram, UR target reachable (ref.fa beside it): 28/4 from scan, rc 0', rc == 0 and stats(o) == (28, 4, 'scan'), f'rc={rc} {stats(o)} {e.strip()[:100]}')
sh(f'mv {W}/ref.fa {W}/ref.away; mv {W}/ref.fa.fai {W}/ref.fa.fai.away')
rc, o, e = vb(f'{W}/hand.cram', 40, '', {**ENV, 'HOME': W})
check('view_bam.py hand.cram, reference unreachable: exit 1, readable "Error reading ..." + CRAM hint, no Traceback, no fake statistics line', rc == 1 and 'Error reading' in e and 'reference.fa' in e and 'Traceback' not in e and stats(o) is None, f'rc={rc} out={o[:60]!r} err={e.strip()[-160:]}')
rc, o, e = vb(f'{W}/hand.cram', 40, W + '/ref.away', ENV)
check('view_bam.py hand.cram <limit> <reference.fa> resolves via the 3rd arg even though UR is dead: 28/4, rc 0', rc == 0 and stats(o) == (28, 4, 'scan'), f'rc={rc} {stats(o)} {e.strip()[:100]}')
rc, o, e = vb(f'{W}/unmapped_only.cram', 40, '', {**ENV, 'HOME': W})
check('unmapped-only CRAM whose reads are PLACED (ctgA:50/100/150) still needs the reference: view_bam.py exits 1 with the CRAM hint when it is gone', rc == 1 and 'Error reading' in e, f'rc={rc} {stats(o)} {e.strip()[-120:]}')
rc, o, e = sh(f'samtools view -o /dev/null {W}/unmapped_only.cram && echo ok; echo rc=$?', env={**ENV, 'HOME': W})
check('Skill full-decode check `view -o /dev/null f.cram && echo ok` also fails on that placed-unmapped CRAM while the reference is gone (consistent with the Skill text)', 'ok' not in o.split() and 'rc=1' in o, o.strip().replace('\n', ' '))
hl = open(W + '/hand.sam').read().splitlines()
open(W + '/unplaced_only.sam', 'w', newline='\n').write('\n'.join([l for l in hl if l.startswith('@') or l.split('\t')[0] == 'u_unplaced']) + '\n')
sh(f'samtools view -C -T {W}/ref.away -o {W}/unplaced_only.cram {W}/unplaced_only.sam')
rc, o, e = sh(f'samtools view -o /dev/null {W}/unplaced_only.cram && echo ok; samtools view -c {W}/unplaced_only.cram; echo rc=$?', env={**ENV, 'HOME': W})
check('CRAM holding only the UNPLACED unmapped read decodes with no reference at all ("ok" printed): the Skill check proves decodability, so for such a file it cannot prove the reference is reachable', o.split()[:3] == ['ok', '1', 'rc=0'], o.strip().replace('\n', ' '))
sh(f'mv {W}/ref.away {W}/ref.fa; mv {W}/ref.fa.fai.away {W}/ref.fa.fai')
# row content
rc, o, e = vb(f'{W}/hand.sam', 40)
txt = o.splitlines()
hdr_i = [i for i, l in enumerate(txt) if l.startswith('name\t')][0]
body = [l.split('\t') for l in txt[hdr_i + 1:]]
check('view_bam.py header row labels the coordinate: "name  chrom:start(0-based)  strand  cigar"', txt[hdr_i] == 'name\tchrom:start(0-based)\tstrand\tcigar', txt[hdr_i])
row = {(b_[0], b_[3]): b_ for b_ in body}
check('view_bam.py rows: r_M shows ctgA:4 (POS 5 - 1) + 10M; r_H shows 2H6M2H; p1 reverse mate shows "-"; hard/soft clips and N printed verbatim',
      ('r_M', '10M') in row and row[('r_M', '10M')][1] == 'ctgA:4' and ('r_H', '2H6M2H') in row and any(b_[0] == 'p1' and b_[2] == '-' and b_[1] == 'ctgA:60' for b_ in body) and ('r_N', '4M20N4M') in row, [b_ for b_ in body if b_[0] in ('r_M', 'p1')])
unm = {b_[0]: b_ for b_ in body if b_[3] == 'unmapped'}
check('view_bam.py unmapped rows: placed one shows ctgA:49 ... unmapped, unplaced shows * ... unmapped (never None:-1)', unm.get('u_placed', [None, None])[1] == 'ctgA:49' and unm.get('u_unplaced', [None, None])[1] == '*' and 'None' not in o, {k: v for k, v in unm.items() if k.startswith('u_')})
# limit handling
rc, o, e = vb(f'{W}/hand.sam', 0)
check('limit 0: prints the header row and no records, rc 0', rc == 0 and len(o.strip().splitlines()) == 4 and o.strip().splitlines()[-1].startswith('name'), o.strip()[-100:])
rc, o, e = vb(f'{W}/hand.sam', 1000)
check('limit larger than the file prints all 32 records', len([l for l in o.splitlines() if '\t' in l]) == 33, len(o.splitlines()))
# error paths
rc, o, e = vb(f'{W}/does_not_exist.bam')
check('missing file: exit 1, "Error reading" message, no Traceback', rc == 1 and 'Error reading' in e and 'Traceback' not in e, f'rc={rc} {e.strip()[:120]}')
open(W + '/notbam.txt', 'w').write('hello world\nthis is not an alignment file\n')
rc, o, e = vb(f'{W}/notbam.txt')
check('non-alignment text file: nonzero exit and a readable error (no bare Traceback)', rc != 0 and 'Traceback' not in e, f'rc={rc} out={o[:50]!r} err={e.strip()[:160]}')
sz = os.path.getsize(W + '/hand_noidx.bam')
sh(f'head -c {sz // 2} {W}/hand_noidx.bam > {W}/trunc.bam')
rc, o, e = vb(f'{W}/trunc.bam')
check('truncated BAM: nonzero exit with a readable error, no Traceback', rc != 0 and 'Traceback' not in e, f'rc={rc} out={o[:60]!r} err={e.strip()[:160]}')
rc, o, e = vb(f'{W}/hand.sam', 'abc')
note('non-numeric limit argument', f'rc={rc} err={e.strip()[-100:]}')
rc, o, e = vb('')
check('no arguments: usage line, exit 1', rc == 1 and 'Usage: view_bam.py' in o, o.strip()[:100])
sh(f'rm -rf {RUN}/skill/examples/__pycache__')

# ---------------- C. convert_formats.sh on the hand SAM ----------------
def recs_md5(path, extra=''):
    o = sh(f'samtools view {extra} {path}', env=ENV)[1]
    return ''.join('\t'.join(f[:11] + sorted(f[11:])) + '\n' for f in (l.split('\t') for l in o.rstrip('\n').split('\n'))), o.count('\n')


base, n0 = recs_md5(W + '/hand.sam')
def helper(args, env=ENV):
    rc, o, e = sh(f'bash {CV} {args}; echo rc=$?', env=env)
    return int(re.search(r'rc=(\d+)', o).group(1)), o, e
rc, o, e = helper(f'{W}/hand.sam {W}/c1.bam')
rc2, o2, e2 = helper(f'{W}/c1.bam {W}/c2.cram {W}/ref.fa')
rc3, o3, e3 = helper(f'{W}/c2.cram {W}/c3.sam {W}/ref.fa')
rc4, o4, e4 = helper(f'{W}/c2.cram {W}/c4.bam {W}/ref.fa')
ok = (rc, rc2, rc3, rc4) == (0, 0, 0, 0)

def parse(path):
    o = sh(f'samtools view {path}', env=ENV)[1]
    return {(f[0], f[1]): f for f in (l.split('\t') for l in o.rstrip('\n').split('\n'))}
H0 = parse(W + '/hand.sam'); H1 = parse(W + '/c1.bam'); H3 = parse(W + '/c3.sam'); H4 = parse(W + '/c4.bam')
check('convert_formats.sh SAM -> BAM keeps all 32 records byte-identical (fields + tags)', rc == 0 and H1 == H0 and len(H1) == 32, (rc, len(H1)))
check('convert_formats.sh BAM -> CRAM(+ref) -> SAM and -> BAM: rc 0, 32 records, SAM and BAM outputs agree with each other', (rc2, rc3, rc4) == (0, 0, 0) and len(H3) == len(H4) == 32 and H3 == H4, (rc2, rc3, rc4, len(H3), len(H4)))
# differences introduced by the CRAM leg, excluding the deliberately nonsensical flag-bit records (fb_*)
diffs = {}
for k, f in H0.items():
    if k[0].startswith('fb_'):
        continue
    g = H3[k]
    d = []
    if f[:11] != g[:11]:
        d.append('fields:' + ','.join(f'col{i + 1} {a}->{b}' for i, (a, b) in enumerate(zip(f[:11], g[:11])) if a != b))
    if sorted(f[11:]) != sorted(g[11:]):
        d.append('tags+' + ','.join(sorted(x.split(':')[0] for x in set(g[11:]) - set(f[11:]))) + ' tags-' + ','.join(sorted(x.split(':')[0] for x in set(f[11:]) - set(g[11:]))))
    if d:
        diffs[k] = d
note('records changed by BAM->CRAM->SAM (fb_* excluded)', {f'{k[0]}/{k[1]}': v for k, v in list(diffs.items())[:6]})
fields_changed = {k: v for k, v in diffs.items() if any(x.startswith('fields:') for x in v)}
tags_added = {k for k, v in diffs.items() if any(x.startswith('tags+MD,NM') for x in v)}
check('CRAM leg rewrites the `=`/`X` CIGAR of r_EQX (4=1X4= -> 9M) and nothing else in columns 1-11 of the realistic records', list(fields_changed) == [('r_EQX', '0')] and 'col6 4=1X4=->9M' in fields_changed[('r_EQX', '0')][0], fields_changed)
check('CRAM decode adds MD:Z and NM:i to mapped records that had neither (reference available): MD/NM appear on the mapped, non-clipped-only records', len(tags_added) >= 15, len(tags_added))
check('SKILL.md line "a round trip keeps every field and tag but not the tag order" holds for this file (CRAM changed a CIGAR and added tags)', not diffs, f'{len(diffs)} of 30 realistic records differ: {list(diffs.items())[:2]}')
check('fb_4 (unmapped, MAPQ 10) and nonsense flag 0x20-without-0x1 are normalised by CRAM: MAPQ 10->0 and flag 32->33 (informational, planted-nonsense records)', H3[('fb_4', '4')][4] == '0' and ('fb_32', '33') in H3, (H3[('fb_4', '4')][4], [k for k in H3 if k[0] == 'fb_32']))

rc, o, e = helper(f'{W}/c2.cram {W}/c5.bam', {'REF_PATH': '', 'REF_CACHE': '', 'HOME': W})
sh(f'mv {W}/ref.fa {W}/ref.away')
rc, o, e = helper(f'{W}/c2.cram {W}/c6.bam', {'REF_PATH': '', 'REF_CACHE': '', 'HOME': W})
check('convert_formats.sh CRAM -> BAM with no reference arg and the UR target gone: non-zero rc (no silent success)', rc != 0, f'rc={rc} {e.strip()[:100]}')
sh(f'mv {W}/ref.away {W}/ref.fa')
rc, o, e = helper(f'{W}/hand.sam {W}/c7.cram')
check('convert_formats.sh SAM -> CRAM without the reference argument: rc 1 and message says a reference is required', rc == 1 and 'requires reference' in o, o.strip()[:120])
rc, o, e = helper(f'{W}/hand.sam {W}/hand.sam')
check('convert_formats.sh input == output refuses (rc 1) and the SAM keeps 32 records', rc == 1 and sh(f'samtools view -c {W}/hand.sam')[1].strip() == '32', o.strip()[:100])
sh(f'rm -rf {RUN}/skill/examples/__pycache__')
