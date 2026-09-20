#!/usr/bin/env python3
"""Input 1 (canonical): 'Filter my BAM to keep only high-quality reads' -> SKILL.md standard filter
(samtools -F 3332 -q 30 and pysam passes_filter) on REAL BAMs, verified against hand-count from raw flag/MAPQ ints.
Also usage-guide recipes (-F 2308 -q 30, AlignmentFilter, count_with_filter)."""
import os, subprocess, sys, shutil
import pysam

AFD = os.environ['AFDATA']
W = sys.argv[1]; os.makedirs(W, exist_ok=True)
fails = []
def check(name, cond, detail=''):
    print(('PASS' if cond else 'FAIL'), name, detail)
    if not cond: fails.append(name)

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def magic(p):
    return open(p, 'rb').read(4)

for label, src in [('1000g', f'{AFD}/1000g/HG00349.chr20_1400000-1500000.bam'),
                   ('human', f'{AFD}/human/test.paired_end.sorted.bam')]:
    print(f'\n===== {label}')
    inp = f'{W}/{label}.input.bam'; shutil.copy(src, inp)
    recs = [(r.flag, r.mapping_quality, r.query_name) for r in pysam.AlignmentFile(inp)]
    n = len(recs)
    exp_std = sorted((f, q, n_) for f, q, n_ in recs if not (f & 3332) and q >= 30)
    exp_2308 = sorted((f, q, n_) for f, q, n_ in recs if not (f & 2308) and q >= 30)
    print('records', n, ' expected -F3332 -q30:', len(exp_std), ' expected -F2308 -q30:', len(exp_2308))
    print('flag mix: dup', sum(1 for f,_,_ in recs if f&1024), 'secondary', sum(1 for f,_,_ in recs if f&256),
          'supp', sum(1 for f,_,_ in recs if f&2048), 'unmapped', sum(1 for f,_,_ in recs if f&4),
          'mapq<30', sum(1 for _,q,_ in recs if q < 30))

    # CLI exactly as SKILL.md "Standard Quality Filter" (no -b: relies on -o extension)
    out = f'{W}/{label}.filtered.bam'
    rc, so, se = sh(f'samtools view -F 3332 -q 30 -o {out} {inp}')
    check(f'{label} CLI -F 3332 -q 30 exit+file', rc == 0 and os.path.exists(out), se[:100])
    check(f'{label} -o x.bam without -b writes BGZF/BAM (magic 1f8b)', magic(out)[:2] == b'\x1f\x8b', repr(magic(out)))
    got = sorted((r.flag, r.mapping_quality, r.query_name) for r in pysam.AlignmentFile(out))
    check(f'{label} CLI records == hand-count', got == exp_std, f'{len(got)} vs {len(exp_std)}')
    check(f'{label} header kept (SQ/RG count)', pysam.AlignmentFile(out).header.to_dict().get('RG') == pysam.AlignmentFile(inp).header.to_dict().get('RG'))
    rc, so, se = sh(f'samtools quickcheck {out} && echo OK')
    check(f'{label} quickcheck', 'OK' in so)

    # usage-guide: -F 2308 -q 30 ('Standard quality filter' there)
    out2 = f'{W}/{label}.f2308.bam'
    sh(f'samtools view -F 2308 -q 30 -o {out2} {inp}')
    got2 = sorted((r.flag, r.mapping_quality, r.query_name) for r in pysam.AlignmentFile(out2))
    check(f'{label} usage-guide -F 2308 -q 30 == hand-count', got2 == exp_2308, f'{len(got2)}')
    ndup_kept = sum(1 for f, _, _ in got2 if f & 1024)
    print(f'{label}: usage-guide "standard" -F 2308 keeps {ndup_kept} duplicate-flagged reads that SKILL.md -F 3332 drops '
          f'({len(got2)} vs {len(got)})')

    # pysam "Basic Filtering" from SKILL.md (verbatim logic): unmapped, mapq<30, duplicate
    pb = f'{W}/{label}.pysam_basic.bam'
    with pysam.AlignmentFile(inp, 'rb') as infile:
        with pysam.AlignmentFile(pb, 'wb', header=infile.header) as outfile:
            for read in infile:
                if read.is_unmapped: continue
                if read.mapping_quality < 30: continue
                if read.is_duplicate: continue
                outfile.write(read)
    nb = sum(1 for _ in pysam.AlignmentFile(pb))
    nsec = sum(1 for r in pysam.AlignmentFile(pb) if r.is_secondary or r.is_supplementary)
    print(f'{label}: pysam Basic Filtering writes {nb}; CLI standard writes {len(exp_std)}; secondary/supp left in: {nsec}')

    # pysam passes_filter (verbatim from SKILL.md)
    def passes_filter(read):
        if read.is_unmapped: return False
        if read.is_secondary or read.is_supplementary: return False
        if read.is_duplicate: return False
        if read.mapping_quality < 30: return False
        return True
    pf = f'{W}/{label}.pysam_pf.bam'
    with pysam.AlignmentFile(inp, 'rb') as infile:
        with pysam.AlignmentFile(pf, 'wb', header=infile.header) as outfile:
            for read in infile:
                if passes_filter(read): outfile.write(read)
    gotpf = sorted((r.flag, r.mapping_quality, r.query_name) for r in pysam.AlignmentFile(pf))
    check(f'{label} pysam passes_filter == CLI -F 3332 -q 30', gotpf == exp_std, f'{len(gotpf)}')

    # usage-guide AlignmentFilter + count_with_filter (verbatim)
    class AlignmentFilter:
        def __init__(self, min_mapq=0, remove_duplicates=True, primary_only=True):
            self.min_mapq = min_mapq; self.remove_duplicates = remove_duplicates; self.primary_only = primary_only
        def passes(self, read):
            if read.is_unmapped: return False
            if read.mapping_quality < self.min_mapq: return False
            if self.remove_duplicates and read.is_duplicate: return False
            if self.primary_only and (read.is_secondary or read.is_supplementary): return False
            return True
    filt = AlignmentFilter(min_mapq=30)
    with pysam.AlignmentFile(inp, 'rb') as infile:
        cnt = sum(1 for r in infile if filt.passes(r))
    check(f'{label} usage-guide AlignmentFilter count == hand-count', cnt == len(exp_std), f'{cnt}')

    def count_with_filter(bam_path, mapq_min=0, exclude_flags=0):
        count = 0
        with pysam.AlignmentFile(bam_path, 'rb') as bam:
            for read in bam:
                if read.flag & exclude_flags: continue
                if read.mapping_quality >= mapq_min: count += 1
        return count
    before = count_with_filter(inp); after = count_with_filter(inp, mapq_min=30, exclude_flags=2308)
    rc, so, _ = sh(f'samtools view -c {inp}'); rc, so2, _ = sh(f'samtools view -c -F 2308 -q 30 {inp}')
    check(f'{label} count_with_filter == samtools -c (before/after)', (before, after) == (int(so), int(so2)) and before == n, f'{before}/{after}')

    # Troubleshooting 'Check filter effect first' + verify output
    rc, so, _ = sh(f'samtools flagstat {out}')
    print(so.splitlines()[0:4])

# planted-dup BAM: counts derived from planted truth
print('\n===== planted_dups (no dup flags set)')
pd = f'{AFD}/derived/planted_dups.bam'
rc, so, _ = sh(f'samtools view -c -F 1024 {pd}')
print('planted_dups -F 1024 count =', so.strip(), '(500 records, 100 are planted duplicate reads but UNMARKED)')
check('SKILL.md "Remove Duplicates" (-F 1024) on an unmarked BAM removes nothing', int(so) == 500)
print('\nFAILS:', fails)
