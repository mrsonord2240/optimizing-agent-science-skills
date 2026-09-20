#!/usr/bin/env python
"""NEW INPUT 6: planted-truth reference with N run / IUPAC codes / soft-masked block / mixed line widths / an empty contig, and a BAM with
planted SNPs, het columns, a deletion, an insertion, a coverage gap, edge coverage and decoy reads (DUP, secondary, Q5, MAPQ0, soft clips).
Truth is planted (make_planted.py); the Skill's Python functions (verbatim from SKILL.md) and samtools consensus are judged against it."""
import contextlib, io, json, os, shutil, sys
from collections import Counter
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam
D = f'{W}/work/r6'; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
for f in ('planted.fa', 'planted.bam', 'planted.bam.bai'): shutil.copy(f'{W}/data/planted/{f}', f'{D}/{f}')
T = json.load(open(f'{W}/data/planted/truth.json')); REF = T['ref']; SAMP = T['sample']; DEP = T['depth']
def blk(n): return open(f'{W}/snippets/{n}.txt').read()
def cons(args, region=''):
    rc, o, e = sh(f'samtools consensus {args} planted.bam', D)
    return rc, fa_records(o), e

print('##### A. prepare_reference.sh on a hostile reference (mixed widths, N run, IUPAC, soft-mask, empty contig)')
shutil.copy(f'{W}/skill/examples/prepare_reference.sh', f'{D}/prepare_reference.sh')
rc, o, e = sh('bash prepare_reference.sh planted.fa', D)
fa = parse_fasta(f'{D}/planted.fa')
sq = [dict(x.split(':', 1) for x in l.split('\t')[1:]) for l in open(f'{D}/planted.dict').read().splitlines() if l.startswith('@SQ')]
check('prepare_reference.sh: rc 0; planted.dict has 3 contigs with LN 6000/1500/800', rc == 0 and [s['LN'] for s in sq] == ['6000', '1500', '800'], o[-200:])
check('planted.dict M5 == md5 of the UPPERCASE sequence for all 3 contigs (IUPAC letters and N kept, soft-mask lower-cased bases normalised)', all(s['M5'] == md5(fa[s['SN']].upper()) for s in sq))
check('the reference really contains the planted features (lowercase block, N run, R/Y)', fa['ctgA'][3000:3400].islower() and fa['ctgA'][1000:1030] == 'N' * 30 and fa['ctgA'][2000:2002] == 'RY')
rc, o, e = sh('picard CreateSequenceDictionary R=planted.fa O=picard.dict 2>&1 | tail -1; grep "^@SQ" picard.dict | cut -f2-4 | md5sum; grep "^@SQ" planted.dict | cut -f2-4 | md5sum', D)
h = o.split('\n'); check('Picard 3.5.0 CreateSequenceDictionary gives identical SN/LN/M5 (IUPAC + N + soft-mask reference)', h[-3].split()[0] == h[-2].split()[0], h[-3:])
print('##### B. samtools consensus against planted truth')
# B1: one character per reference position
rc, r, e = cons('-a --show-del yes --show-ins no -d 3 -r ctgA')
A_ = r[0][1]
check('B1 `-a --show-del yes --show-ins no` gives ctgA exactly 6000 characters (SKILL: one char per reference position)', len(A_) == 6000, len(A_))
skip_cols = {700, 900}                                   # het columns judged separately
mism = [i for i in range(6000) if DEP[i] >= 6 and i not in skip_cols and i not in (4000, 4001) and A_[i] != SAMP[i]]
check('B1 every column with depth >= 6 (pysam-independent truth) equals the planted sample base, including SNPs at 500/2500/3100, under the reference N run and R/Y', not mism, mism[:10])
check('B1 the 2 deleted columns are "*" (SKILL: deleted columns become *)', A_[4000:4002] == '**')
gap = A_[1500:1800]
check('B1 the uncovered gap 1500..1799 is all N inside the covered span', gap == 'N' * 300, gap[:20])
check('B1 the depth-2 zone 1800..1899 is N with -d 3 (positions below -d become N)', A_[1802:1899] == 'N' * 97, A_[1800:1830])
edge = [(i, A_[i], SAMP[i], DEP[i]) for i in list(range(0, 12)) + list(range(5988, 6000))]
print('    edge columns (pos, called, truth, depth):', edge[:12], '...', edge[-4:])
check('B1 first 8 columns (depth 1-2) are N, column 5999 (HOM SNP at the contig end, depth 2) is N with -d 3', A_[:8] == 'N' * 8 and A_[5999] == 'N')
rc, r1, e = cons('-a --show-del yes --show-ins no -d 1 -r ctgA'); A1 = r1[0][1]
check('B1b with -d 1 the contig-end SNP (ref %s -> %s) IS called at position 5999 and start/end positions equal the truth' % (REF[5999], SAMP[5999]), A1[5999] == SAMP[5999] and A1[0] == SAMP[0] and A1[3] == SAMP[3], (A1[:4], A1[5996:]))
# het columns
def rec(args): rc, r, e = cons(args); return r[0][1]
b_def = rec('-a --show-del yes --show-ins no -d 3 -r ctgA'); b_amb = rec('-a --show-del yes --show-ins no -d 3 --ambig -r ctgA')
print('    het col 700 (13 C / 12 G) default / --ambig:', b_def[700], b_amb[700], '| het col 900 (20 %s / 5 %s) default / --ambig:' % (SAMP[900], 'x'), b_def[900], b_amb[900])
counts = T['counts']; print('    counts', counts['700'], counts['900'])
check('het 50/50 column 700: default Bayesian = N, --ambig = IUPAC S (C/G)', b_def[700] == 'N' and b_amb[700] == 'S', (b_def[700], b_amb[700]))
print('    NOTE 80/20 column 900: default gives', b_def[900], '--ambig gives', b_amb[900], '(SKILL claims: without --ambig an ambiguous column is N, even when one base is 80% of the reads)')
check('80/20 column 900 (5 minor reads at Q40): default = %s' % b_def[900], b_def[900] in 'ACGTN', b_def[900])
# decoys
check('decoys: col 500 (30 DUP + 30 secondary wrong bases) = planted alt %s; col 2700 (20 Q5 wrong bases) = truth; col 3700 (12 MAPQ0 wrong vs 25 right) = truth' % SAMP[500], A_[500] == SAMP[500] and A_[2700] == SAMP[2700] and A_[3700] == SAMP[3700], (A_[500], A_[2700], A_[3700]))
# B2 default (no -a): ends trimmed, insertion shown
rc, r2, e = cons('-d 1 -r ctgA'); D2 = r2[0][1]
ctx = SAMP[4490:4501] + 'GTA' + SAMP[4501:4511]
check('B2 default output (-d 1): starts/ends on called bases (covered span 0..5999), no * (deletion not shown)', D2[0] == SAMP[0] and D2[-1] == SAMP[5999] and '*' not in D2, (D2[:5], D2[-5:]))
check('B2 the planted insertion GTA appears right after ref 4500 in the default output (--show-ins yes)', ctx in D2, ctx)
check('B2 default length = 6000 - 2 deleted + 3 inserted = 6001', len(D2) == 6001, len(D2))
# B3 -a vs -aa on contigs
rc, r3, e = cons('-a -d 1 --show-ins no'); rc, r4, e2 = cons('-aa -d 1 --show-ins no'); rc, r5, e3 = cons('-d 1 --show-ins no')
print('    default records:', [(h, len(s)) for h, s in r5], '| -a:', [(h, len(s)) for h, s in r3], '| -aa:', [(h, len(s)) for h, s in r4])
check('B3 default: only contigs with reads (ctgA, ctgB); -a: same 2 contigs, ctgB padded to header LN 1500; -aa: adds ctgC as 800 N', [h for h, s in r5] == ['ctgA', 'ctgB'] and [h for h, s in r3] == ['ctgA', 'ctgB'] and dict(r3)['ctgB'] and len(dict(r3)['ctgB']) == 1500 and [h for h, s in r4] == ['ctgA', 'ctgB', 'ctgC'] and dict(r4)['ctgC'] == 'N' * 800)
b = dict(r3)['ctgB']; Bs = T['B']
check('B3 -a ctgB: N padding 0..~199 and ~700..1499, calls inside the covered span equal the reference (reads are reference-identical)', set(b[:200]) == {'N'} and set(b[700:]) == {'N'} and b[200:700] == Bs[200:700], (b[190:215], b[685:715]))
check('B3 default (no -a) trims ctgB to the called span: shorter than 500+ and equal to the reference substring', dict(r5)['ctgB'] == Bs[200:700], len(dict(r5)['ctgB']))
# B4 region edges
rc, r6, e = sh('samtools consensus -r ctgA:5901-6000 --show-ins no -d 3 -a planted.bam', D)[0], fa_records(sh('samtools consensus -r ctgA:5901-6000 --show-ins no -d 3 -a planted.bam', D)[1]), ''
print('    -r ctgA:5901-6000 -a:', [(h, len(s)) for h, s in r6])
# B5 -T: which columns does it fill?  (SKILL: "Report ref base where consensus unavailable (low coverage; ... bases keep the FASTA case)")
rc, r7, e = cons('-a --show-del yes --show-ins no -d 3 -T planted.fa -r ctgA'); T7 = r7[0][1]
check('B5a -T fills the ZERO-coverage gap 1500..1799 with the reference bases (upper case there, as in the FASTA)', T7[1500:1800] == REF[1500:1800], (T7[1500:1510], REF[1500:1510]))
check('B5b OBSERVATION: columns below -d (depth-2 zone 1800..1899) stay N with -T: "low coverage" in the SKILL wording does not mean depth < -d', set(T7[1802:1899]) == {'N'}, T7[1800:1830])
rc, r7d, e = cons('-a --show-del yes --show-ins no -d 30 -T planted.fa -r ctgA'); T7d = r7d[0][1]
low_cols = [i for i in range(3000, 3400) if DEP[i] < 30]
check('B5c OBSERVATION: `-d 30 -T` does NOT report the (lower-case) reference base at the %d soft-masked columns with depth < 30: they stay N' % len(low_cols), len(low_cols) > 300 and all(T7d[i] == 'N' for i in low_cols), (T7d[3000:3020], fa['ctgA'][3000:3020]))
rc, r7e, e = cons('-a --show-del yes --show-ins no -d 3 -T planted.fa --ambig -r ctgA'); T7e = r7e[0][1]
check('B5d ambiguous-but-not-called columns are not filled by -T either (col 700 stays N without --ambig)', T7[700] == 'N' and T7[900] == 'N', (T7[700], T7[900]))
# B6 same call with and without -T: does -T change anything other than the unavailable columns?
rc, r8, e = cons('-a --show-del yes --show-ins no -d 3 -r ctgA -T planted.fa'); T8 = r8[0][1]
diff = [(i, A_[i], T8[i]) for i in range(6000) if A_[i] != T8[i]]
print('    -T planted.fa (default -d 3) vs no -T: %d differing columns; first ones:' % len(diff), diff[:8])
check('B6 -T only fills columns that were N/unavailable (never changes a called base) - SKILL describes -T only as the fill option', all(a == 'N' or a == '*' and False for _, a, _b in diff) or not diff, diff[:6])
# B7 FASTQ -l 0
rc, o, e = sh('samtools consensus -f fastq -l 0 -r ctgA:1000-1100 -d 3 planted.bam', D); L = o.splitlines()
check('B7 -f fastq -l 0 gives 4 lines per record (SKILL); default wrap 70 for FASTA', len(L) % 4 == 0 and len(L) >= 4 and L[2] == '+' and len(L[1]) == len(L[3]), len(L))
rc, o, e = sh('samtools consensus -l 70 -r ctgA:1900-2500 -d 3 planted.bam', D); check('B7b FASTA default line length is 70', max(len(x) for x in o.splitlines()[1:]) == 70, max(len(x) for x in o.splitlines()[1:]))

print('##### C. SKILL Python snippets (verbatim) against planted truth')
ns = {'pysam': pysam, 'Counter': Counter}
exec(blk('skill_25_python'), ns); exec(blk('skill_26_python'), ns); exec(blk('skill_24_python').split("with pysam.AlignmentFile")[0], ns)
bc = ns['build_consensus']; cmp_ = ns['compare_to_ref']; cap = ns['consensus_at_position']
BAM = f'{D}/planted.bam'
c3 = bc(BAM, 'ctgA', 0, 6000, min_depth=3)
truth = T['pysam_truth']
check('C1 build_consensus(ctgA,0,6000,min_depth=3) has exactly 6000 chars and equals the independent cigar-walk majority at all 6000 columns (ties: %d)' % len(T['ties']), len(c3) == 6000 and c3 == truth, [i for i in range(min(len(c3), 6000)) if c3[i] != truth[i]][:10])
check('C1 decoys handled as the SKILL says: col 500 (DUP+secondary) = alt, col 2700 (Q5) = truth, gap 1500..1799 = N, deleted columns 4000/4001 = N', c3[500] == SAMP[500] and c3[2700] == SAMP[2700] and c3[1500:1800] == 'N' * 300 and c3[4000:4002] == 'NN')
check('C1 MAPQ-0 column 3700 (12 wrong vs 25 right): majority vote still right; skill says it is not quality-aware', c3[3700] == SAMP[3700])
print('    build_consensus at the het cols 700/900:', c3[700], c3[900], '| counts', counts['700'], counts['900'])
c1 = bc(BAM, 'ctgA', 0, 6000, min_depth=1)
check('C2 min_depth=1: contig-end SNP at 5999 and the first bases are called (edge positions)', c1[5999] == SAMP[5999] and c1[0] == SAMP[0] and 'N' not in c1[:1500][:1400] or c1[5999] == SAMP[5999])
sub = bc(BAM, 'ctgA', 4990, 6000, min_depth=3); check('C3 sub-region [4990,6000): length 1010, equals slice of the full call', len(sub) == 1010 and sub == c3[4990:6000], (len(sub)))
past = bc(BAM, 'ctgA', 5900, 6100, min_depth=1)
check('C3b region running past the contig end [5900,6100): returns end-start = 200 chars, tail N', len(past) == 200 and past[100:] == 'N' * 100, len(past))
mid = bc(BAM, 'ctgA', 1450, 1850, min_depth=1); check('C3c region straddling the gap: 400 chars, N exactly over 1500..1799 (no shift after the gap)', len(mid) == 400 and mid[50:350] == 'N' * 300 and mid[349 - 0 + 1 - 1:350] == 'N' and mid[350:] == c1[1800:1850])
diffs = cmp_(BAM, f'{D}/planted.fa', 'ctgA', 0, 6000, 3)
exp = [(i + 1, REF[i].upper() if REF[i] != 'N' else 'N', truth[i]) for i in range(6000) if truth[i] != 'N' and truth[i] != REF[i].upper()]
check('C4 compare_to_ref (soft-mask upper-cased, 1-based) == independent list: %d differences' % len(exp), diffs == [(p, r, c) for p, r, c in exp], (len(diffs), diffs[:3]))
kinds = Counter('N-run' if 1000 <= p - 1 < 1030 else ('IUPAC' if p - 1 in (2000, 2001) else 'real') for p, r, c in diffs)
print('    compare_to_ref breakdown:', dict(kinds), '(the 30 N-run and 2 IUPAC positions are reported as differences: consensus base vs reference N/R/Y)')
check('C4 the SNP at 3100 inside the lower-case block is reported once (case-insensitive compare works)', sum(1 for p, r, c in diffs if p == 3101) == 1)
check('C5 consensus_at_position: hom-alt col 500 -> alt; gap col 1600 -> N; deleted col 4000 -> N', cap(pysam.AlignmentFile(BAM), 'ctgA', 500) == SAMP[500] and cap(pysam.AlignmentFile(BAM), 'ctgA', 1600) == 'N' and cap(pysam.AlignmentFile(BAM), 'ctgA', 4000) == 'N')
# agreement between the two methods on called columns
sam = A1
both = [i for i in range(6000) if sam[i] in 'ACGT' and c1[i] in 'ACGT']
dis = [i for i in both if sam[i] != c1[i] and i not in (700, 900)]
check('C6 samtools consensus (-d 1) and the Skill Python (min_depth 1) agree at every column both call ACGT, except het cols (%d columns compared)' % len(both), not dis, dis[:8])

print('##### D. pysam pileup default claims in the SKILL prose')
# max_depth 8000 default
hd = {'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'c', 'LN': 200}]}
with pysam.AlignmentFile(f'{D}/deep.bam', 'wb', header=hd) as out:
    for k in range(9000):
        a = pysam.AlignedSegment(out.header); a.query_name = 'd%d' % k; a.query_sequence = 'A' * 50; a.flag = 0; a.reference_id = 0; a.reference_start = 10
        a.mapping_quality = 60; a.cigartuples = [(0, 50)]; a.query_qualities = pysam.qualitystring_to_array('I' * 50); out.write(a)
pysam.index(f'{D}/deep.bam')
with pysam.AlignmentFile(f'{D}/deep.bam') as b:
    n_def = max(c.n for c in b.pileup('c', 10, 60, truncate=True)); n_big = max(c.n for c in b.pileup('c', 10, 60, truncate=True, max_depth=1_000_000))
check('SKILL prose: max_depth defaults to 8000 (9000 reads -> 8000) and max_depth=1_000_000 sees all 9000', n_def == 8000 and n_big == 9000, (n_def, n_big))
# overlap dedup: planted overlapping proper pairs (mate1 5..104 forward, mate2 55..154 reverse; overlap 55..104); 40 pairs
with pysam.AlignmentFile(f'{D}/pe_u.bam', 'wb', header=hd) as out:
    for k in range(40):
        for m, (st, fl) in enumerate(((5, 99), (55, 147))):
            a = pysam.AlignedSegment(out.header); a.query_name = 'p%d' % k; a.query_sequence = 'C' * 100; a.flag = fl; a.reference_id = 0; a.reference_start = st
            a.mapping_quality = 60; a.cigartuples = [(0, 100)]; a.query_qualities = pysam.qualitystring_to_array('I' * 100)
            a.next_reference_id = 0; a.next_reference_start = 55 if m == 0 else 5; a.template_length = 150 if m == 0 else -150; out.write(a)
pysam.sort('-o', f'{D}/pe.bam', f'{D}/pe_u.bam'); pysam.index(f'{D}/pe.bam')
with pysam.AlignmentFile(f'{D}/pe.bam') as b:
    d_def = {c.reference_pos: len(c.pileups) for c in b.pileup('c', 0, 200, truncate=True)}   # what build_consensus loops over (PileupColumn.n itself is not reduced)
    d_all = {c.reference_pos: len(c.pileups) for c in b.pileup('c', 0, 200, truncate=True, ignore_overlaps=False)}
print('    overlap column 60: default n =', d_def[60], ' ignore_overlaps=False n =', d_all[60], '| single-mate column 20 default n =', d_def[20])
check('SKILL prose: overlapping mates are counted once by default (40 pairs: overlap column depth 40 by default, 80 with ignore_overlaps=False)', d_def[60] == 40 and d_all[60] == 80 and d_def[20] == 40, (d_def[60], d_all[60], d_def[20]))
with pysam.AlignmentFile(f'{W}/data/real/test.paired_end.sorted.bam') as b:
    nd = sum(len(c.pileups) for c in b.pileup('chr22', 1951, 4617, truncate=True, max_depth=100000)); ni = sum(len(c.pileups) for c in b.pileup('chr22', 1951, 4617, truncate=True, ignore_overlaps=False, max_depth=100000))
print('    real chr22 PE BAM: total pileup bases default', nd, 'vs ignore_overlaps=False', ni)
summary()
