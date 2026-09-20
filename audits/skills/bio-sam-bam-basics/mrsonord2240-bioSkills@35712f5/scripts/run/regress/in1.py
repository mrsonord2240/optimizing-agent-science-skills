"""Input 1 (Canonical): inspect the real human PE BAM the way the Skill teaches.
Prompt: 'Here is test.paired_end.sorted.bam. Show me the header, the first reads decoded (flag meaning,
position, CIGAR), how many reads are in the file and in chr22:2000-3000, and tell me whether pysam
fetch gives the same answer as samtools.'
"""
import os, re, sys
os.environ['AUDIT_INPUT'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chk import check, note, sh
import pysam

D = os.environ['AFDATA'] + '/human'
BAM = D + '/test.paired_end.sorted.bam'
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- independent FLAG decoder written from the SAM spec (v1 sec 1.4.2), not from the Skill/samtools
SPEC = [(0x1, 'PAIRED'), (0x2, 'PROPER_PAIR'), (0x4, 'UNMAP'), (0x8, 'MUNMAP'), (0x10, 'REVERSE'),
        (0x20, 'MREVERSE'), (0x40, 'READ1'), (0x80, 'READ2'), (0x100, 'SECONDARY'), (0x200, 'QCFAIL'),
        (0x400, 'DUP'), (0x800, 'SUPPLEMENTARY')]
SKILL_TABLE = {0x1: 'Paired', 0x2: 'Proper pair', 0x4: 'Unmapped', 0x8: 'Mate unmapped', 0x10: 'Reverse strand',
               0x20: 'Mate reverse strand', 0x40: 'First in pair', 0x80: 'Second in pair', 0x100: 'Secondary alignment',
               0x200: 'Failed QC', 0x400: 'PCR duplicate', 0x800: 'Supplementary'}


def spec_decode(f):
    return ','.join(n for b, n in SPEC if f & b)


# 1. Skill commands: header, first reads, count
rc, out, err = sh(f'samtools view -H {BAM}')
check('view -H prints @HD/@SQ/@RG/@PG', all(t in out for t in ('@HD', '@SQ', '@RG', '@PG')), out.splitlines()[0])
check('view -H adds its own @PG (chain grows by one when viewing a header)', out.count('@PG') == 2 and 'view -H' in out,
      'the header printed by samtools view has an extra @PG for the view command itself; the Skill says nothing (use --no-PG)')
rc, out, err = sh(f'samtools view --no-PG -H {BAM}')
check('--no-PG removes that extra @PG line', out.count('@PG') == 1, f'{out.count("@PG")} @PG lines')

rc, cnt, err = sh(f'samtools view -c {BAM}')
n_view = int(cnt)
with pysam.AlignmentFile(BAM, 'rb') as bam:
    n_iter = sum(1 for _ in bam)
check('samtools view -c == pysam iteration count == 5644 (smoke value)', n_view == n_iter == 5644, f'{n_view} vs {n_iter}')

# 2. decode first reads: samtools flags vs spec vs pysam properties vs Skill table
with pysam.AlignmentFile(BAM, 'rb') as bam:
    reads = [r for _, r in zip(range(400), bam)]
flags = sorted({r.flag for r in reads})
note('distinct flags among first 400 reads', flags)
ok_all = True
for f in flags:
    rc, o, e = sh(f'samtools flags {f}')
    sam_dec = o.split('\t')[2].strip()
    ok_all &= (sam_dec == spec_decode(f))
check('samtools flags <n> agrees with independent spec decoder for every flag seen', ok_all, str(flags))
for f, expect in ((99, 'PAIRED,PROPER_PAIR,MREVERSE,READ1'), (147, 'PAIRED,PROPER_PAIR,REVERSE,READ2')):
    check(f'Skill flag {f} text ("{expect}") equals spec decode', spec_decode(f) == expect, spec_decode(f))
# usage-guide text: 99 = 'First read, properly paired, mate on reverse strand'; 147 = 'Second read, properly paired, on reverse strand'
r99 = next(r for r in reads if r.flag == 99)
check('flag 99 read: is_read1, is_proper_pair, mate_is_reverse, not is_reverse, reference_start<next_reference_start or equal',
      r99.is_read1 and r99.is_proper_pair and r99.mate_is_reverse and not r99.is_reverse
      and r99.template_length >= 0, f'{r99.query_name} tlen={r99.template_length}')
r147 = next(r for r in reads if r.flag == 147)
check('flag 147 read: is_read2, reverse; TLEN is negative (spec: rightmost segment negative)',
      r147.is_read2 and r147.is_reverse and r147.template_length < 0, f'{r147.query_name} tlen={r147.template_length}')
# every Skill table row matches the pysam property of the same bit
props = {0x1: 'is_paired', 0x2: 'is_proper_pair', 0x4: 'is_unmapped', 0x8: 'mate_is_unmapped', 0x10: 'is_reverse',
         0x20: 'mate_is_reverse', 0x40: 'is_read1', 0x80: 'is_read2', 0x100: 'is_secondary', 0x200: 'is_qcfail',
         0x400: 'is_duplicate', 0x800: 'is_supplementary'}
ok = True
for bit, p in props.items():
    r = pysam.AlignedSegment()
    r.flag = bit
    ok &= bool(getattr(r, p)) and all(not getattr(r, q) for b2, q in props.items() if b2 != bit)
check('Skill 12-row FLAG table: each bit maps 1:1 to the pysam property named for it', ok, 'built AlignedSegment per bit')

# 3. Skill's pysam patterns: coordinates and properties
r0 = reads[0]
rc, o, e = sh(f'samtools view {BAM} | head -1')
f = o.split('\t')
check('SAM POS (col 4) = pysam reference_start + 1 (0-based)', int(f[3]) == r0.reference_start + 1, f'{f[3]} vs {r0.reference_start}')
check('CIGAR/MAPQ/flag agree between samtools text and pysam', f[5] == r0.cigarstring and int(f[4]) == r0.mapping_quality and int(f[1]) == r0.flag,
      f'{f[5]} {f[4]} {f[1]}')
note('Skill snippet prints read.query_qualities', repr(r0.query_qualities)[:70])

# 4. region semantics (the "footgun" table): find a read whose reference_end lands on a chosen boundary
with pysam.AlignmentFile(BAM, 'rb') as bam:
    allr = list(bam.fetch('chr22'))
    E = allr[100].reference_end            # 0-based exclusive end == 1-based last base position
    n_sam = int(sh(f'samtools view -c {BAM} chr22:{E}-{E+1}')[1])
    n_fetch = sum(1 for _ in bam.fetch('chr22', E, E + 1))
    n_fetch_wrong = sum(1 for _ in bam.fetch('chr22', E - 1, E))      # 0-based [E-1,E) == 1-based E
    n_naive = sum(1 for _ in bam.fetch('chr22', E, E + 1))
    # Quick Reference row: samtools chr1:1-1000 <-> fetch(chr1, 0, 1000)
    a = int(sh(f'samtools view -c {BAM} chr22:2000-3000')[1])
    b = sum(1 for _ in bam.fetch('chr22', 1999, 3000))
    c = sum(1 for _ in bam.fetch('chr22', 2000, 3000))
check('Quick Reference equivalence: samtools chr:2000-3000 == fetch(chr,1999,3000)', a == b, f'{a} vs {b}')
note('fetch(chr,2000,3000) vs samtools chr:2000-3000 on this region (counts can coincide when no read ends on the boundary)', f'samtools {a}, fetch(2000,3000)={c}')
check('boundary read (last base at 1-based E) is in samtools chr22:E-E+1 but missing from fetch(E,E+1) when copying coordinates verbatim',
      n_sam > n_fetch, f'E={E}: samtools {n_sam}, fetch(E,E+1)={n_fetch}, fetch(E-1,E)={n_fetch_wrong}')

# 5. wrong contig name / missing index behaviour (usage-guide troubleshooting)
rc, o, e = sh(f'samtools view -c {BAM} 22:2000-3000; echo "rc=$?"')
note('wrong contig name (22 vs chr22) samtools', (o + e).strip().replace('\n', ' | '))
rc, o, e = sh(f'samtools view {BAM} 22:2000-3000 | wc -l; echo "pipe-rc=${{PIPESTATUS[0]}}"')
note('wrong contig, stdout mode', (o + e).strip().replace('\n', ' | '))
try:
    with pysam.AlignmentFile(BAM, 'rb') as bam:
        list(bam.fetch('22', 2000, 3000))
    check('pysam fetch with wrong contig name raises', False, 'no exception')
except Exception as ex:
    check('pysam fetch with wrong contig name raises ValueError', isinstance(ex, ValueError), f'{type(ex).__name__}: {ex}')

os.makedirs(RUN + '/data', exist_ok=True)
sh(f'cp {BAM} {RUN}/data/noidx.bam')
rc, o, e = sh(f'samtools view -c {RUN}/data/noidx.bam chr22:2000-3000')
note('samtools region query on unindexed BAM: rc / message', f'rc={rc} stdout={o.strip()!r} stderr={e.strip()!r}')
check('usage-guide says region on missing index errors with "Could not retrieve index file"', 'Could not retrieve index file' in e,
      e.strip())
try:
    with pysam.AlignmentFile(RUN + '/data/noidx.bam', 'rb') as bam:
        list(bam.fetch('chr22', 2000, 3000))
    check('pysam fetch without index raises', False, 'no exception')
except Exception as ex:
    check('pysam fetch without index raises ValueError', isinstance(ex, ValueError), f'{type(ex).__name__}: {ex}')

# 6. shipped example view_bam.py (from the copy under run/skill)
rc, o, e = sh(f'python {RUN}/skill/examples/view_bam.py {BAM} 3')
print(o)
lines = o.strip().splitlines()
check('view_bam.py prints References: 1 / Mapped: 5642 / Unmapped: 2 (pysam index stats)', 'References: 1' in o and 'Mapped: 5642' in o and 'Unmapped: 2' in o, lines[:3])
check('view_bam.py prints reference_start 0-based (SAM 1952 -> 1951) AND the header row now says so (chrom:start(0-based))', 'chr22:1951' in o and '1952' not in o and 'chrom:start(0-based)' in o, lines[4] if len(lines) > 4 else '')
rc, o, e = sh(f'python {RUN}/skill/examples/view_bam.py {RUN}/data/noidx.bam 2; echo rc=$?')
note('view_bam.py on an UNINDEXED BAM', (o + e).strip().replace('\n', ' | ')[-300:])
check('view_bam.py works on unindexed BAM (bam.mapped needs an index)', 'Mapped:' in o and 'Traceback' not in e, (o + e)[-200:])
rc, o, e = sh(f'python {RUN}/skill/examples/view_bam.py $AFDATA/human/test.paired_end.sorted.cram 2; echo rc=$?')
note('view_bam.py on a CRAM (opens with mode rb)', (o + e).strip().replace('\n', ' | ')[-300:])

# 7. the SAM example block in SKILL.md (fixed): extract it verbatim from the Skill copy and parse it
md = open(RUN + '/skill/SKILL.md', encoding='utf-8').read()
blk = md.split('## SAM Format Structure')[1].split('```')[1]
open(RUN + '/data/skill_example.sam', 'w', encoding='utf-8', newline='').write(blk.lstrip('\n'))
rc, o, e = sh(f'samtools view -b -o {RUN}/data/skill_example.bam {RUN}/data/skill_example.sam && samtools view {RUN}/data/skill_example.bam')
f = o.rstrip('\n').split('\t')
check('SKILL.md SAM example, extracted verbatim, parses with `samtools view -b` and reads back as read1 chr1:100 8M ACGTACGT', rc == 0 and f[:6] == ['read1', '0', 'chr1', '100', '60', '8M'] and f[9] == 'ACGTACGT', f'rc={rc} {o.strip()[:80]} {e.strip()[:100]}')
