#!/usr/bin/env python3
"""Input 1 (regression, canonical): 'Filter my BAM to keep only high-quality reads' and 'remove duplicates'.
Snippets are EXTRACTED from the fixed SKILL.md and executed (not retyped). Ground truth = hand count from raw
FLAG/MAPQ integers. Real BAMs: 1000G HG00349 (9601 rec, 101 dup-flagged), nf-core human PE (5644), planted-dup BAM."""
import os, shutil, sys, collections
import pysam
from lib import check, sh, block, finish

AFD = os.environ['AFDATA']; W = sys.argv[1]; SK = sys.argv[2]
os.makedirs(W, exist_ok=True)
MD = f'{SK}/SKILL.md'

for label, src in [('1000g', f'{AFD}/1000g/HG00349.chr20_1400000-1500000.bam'),
                   ('human', f'{AFD}/human/test.paired_end.sorted.bam')]:
    print(f'\n===== {label}')
    d = f'{W}/{label}'; os.makedirs(d, exist_ok=True)
    inp = f'{d}/input.bam'; shutil.copy(src, inp)
    recs = [(r.flag, r.mapping_quality, r.query_name) for r in pysam.AlignmentFile(inp)]
    exp = sorted(t for t in recs if not (t[0] & 3332) and t[1] >= 30)
    print('records', len(recs), 'expected standard filter', len(exp),
          '| dup-flagged', sum(1 for t in recs if t[0] & 1024))
    # CLI: the Standard Quality Filter block
    cli = block(MD, 'Standard Quality Filter', 'bash')
    rc, so, se = sh(cli, cwd=d)
    got = sorted((r.flag, r.mapping_quality, r.query_name) for r in pysam.AlignmentFile(f'{d}/filtered.bam'))
    check(f'{label} SKILL.md standard-filter block == hand-count', got == exp, f'{len(got)} vs {len(exp)} rc={rc} err={se[:80]}')
    check(f'{label} -o filtered.bam (no -b) is BGZF', open(f'{d}/filtered.bam', 'rb').read(2) == b'\x1f\x8b')
    rc, so, _ = sh(f'samtools quickcheck {d}/filtered.bam && echo OK')
    check(f'{label} quickcheck', 'OK' in so)
    # pysam passes_filter block, extracted and run with file names substituted
    code = block(MD, 'Filter with Function', 'python').replace("'input.bam'", f"'{inp}'").replace("'filtered.bam'", f"'{d}/pf.bam'")
    exec(compile(code, 'passes_filter', 'exec'), {})
    gotpf = sorted((r.flag, r.mapping_quality, r.query_name) for r in pysam.AlignmentFile(f'{d}/pf.bam'))
    check(f'{label} pysam passes_filter block == hand-count == CLI', gotpf == exp == got, f'{len(gotpf)}')
    # md5 of full record strings CLI vs pysam
    a = [r.to_string() for r in pysam.AlignmentFile(f'{d}/filtered.bam')]
    b = [r.to_string() for r in pysam.AlignmentFile(f'{d}/pf.bam')]
    check(f'{label} CLI and pysam outputs record-for-record identical', a == b)
    # -c count-before-write line from Output Options
    rc, so, _ = sh(f'samtools view -c -F 3332 -q 30 {inp}')
    check(f'{label} count-only == filtered size', int(so) == len(exp), so.strip())

# --- fixed: Remove Duplicates pre-check snippet ---
print('\n===== Remove Duplicates pre-check (extracted from SKILL.md)')
snip = block(MD, 'Remove Duplicates', 'bash')
for label, src, ndup, nexp in [('planted (unmarked, 100 dup reads)', f'{AFD}/derived/planted_dups.bam', 100, 400),
                               ('1000g (already marked, 101)', f'{AFD}/1000g/HG00349.chr20_1400000-1500000.bam', 101, 9601 - 101)]:
    d = f'{W}/dedup_{label.split()[0]}'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    shutil.copy(src, f'{d}/input.bam')
    rc, so, se = sh(snip, cwd=d)
    n = int(sh(f'samtools view -c {d}/nodup.bam')[1])
    still = int(sh(f'samtools view -c -f 1024 {d}/nodup.bam')[1])
    check(f'{label}: snippet rc=0 and nodup.bam has {nexp} records, 0 dup-flagged', rc == 0 and n == nexp and still == 0, f'rc={rc} n={n} dupflag={still} stderr={se.strip()[:100]!r}')
    if label.startswith('planted'):
        check('unmarked BAM: the snippet announced that it is marking first', 'marking first' in se, se.strip()[:80])
        m = pysam.AlignmentFile(f'{d}/marked.bam')
        grp = collections.defaultdict(list)
        for r in m:
            if r.is_read1 and not r.is_secondary:
                grp[(r.reference_start, r.next_reference_start, r.is_reverse, r.cigarstring)].append(r)
        ok = all(sum(1 for x in v if x.is_duplicate) == (1 if len(v) == 2 else 0) for v in grp.values())
        two = sum(1 for v in grp.values() if len(v) == 2)
        check('planted truth: 50 coordinate groups have 2 templates, exactly one flagged in each, singletons never flagged', ok and two == 50, f'groups with 2 templates={two}')
        check('marked.bam is coordinate sorted, has 500 records', pysam.AlignmentFile(f'{d}/marked.bam').header.to_dict()['HD'].get('SO') == 'coordinate' and int(sh(f'samtools view -c {d}/marked.bam')[1]) == 500)
# human BAM: natural dup flags?
rc, so, _ = sh(f"samtools view -c -f 1024 {AFD}/human/test.paired_end.sorted.bam")
print('human PE BAM dup-flagged records (natural):', so.strip())
# what a naive -F 1024 does on the unmarked BAM (fixed text says it removes nothing)
rc, so, _ = sh(f"samtools view -c -F 1024 {AFD}/derived/planted_dups.bam")
check('claim in text: "-F 1024 on unmarked BAM keeps 500 of 500"', so.strip() == '500', so.strip())
# usage-guide no longer defines a competing "standard" filter
ug = open(f'{SK}/usage-guide.md', encoding='utf-8').read()
check('usage-guide.md no longer contains a competing -F 2308 "standard" filter', '2308' not in ug and '-F 3332' not in ug)
finish()
