"""Input 6 (NEW, not in the pre-fix audit): the multi-region recipes the fixer ADDED to SKILL.md, tested against a
full-scan truth that uses none of samtools' or pysam's region iterators.

Prompt: 'Get reads from chr22:2000-3000 and chr22:2500-3500 (and other region sets, some adjacent, nested, with a small
gap, on several contigs) without duplicates, with samtools and with pysam. Count them.'

Truth: `samtools view file` (no region) parsed in Python; a record overlaps 1-based closed region [s,e] iff
POS <= e and end >= s, end = POS + reference_length - 1 (reference_length from CIGAR M/D/N/=/X; 1 for a placed
unmapped read, which is how htslib treats it). Records are compared as full SAM text lines (multisets).
Every Skill method is compared to that truth; the fetch_regions() helper is extracted verbatim from SKILL.md.
"""
import collections, os, random, re, sys
os.environ['AUDIT_INPUT'] = '6'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regress'))
from chk import check, note, sh
import pysam

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.environ['AFDATA'] + '/human'
BAM = D + '/test.paired_end.sorted.bam'
W = RUN + '/data/in6'
sh(f'rm -rf {W}; mkdir -p {W}')

# ---- fetch_regions() extracted verbatim from the Skill copy
md = open(RUN + '/skill/SKILL.md', encoding='utf-8').read()
code = [b for b in md.split('```python')[1:] if 'def fetch_regions' in b][0].split('```')[0]
ns = {}
exec(code, ns)
fetch_regions = ns['fetch_regions']
check('SKILL.md fetch_regions code block extracted and compiled', callable(fetch_regions), code.splitlines()[0])


def reflen(cigar):
    if cigar == '*':
        return 1
    return sum(int(n) for n, op in re.findall(r'(\d+)([MIDNSHP=X])', cigar) if op in 'MDN=X') or 1


def load(bam):
    """all records (text lines) with (contig, pos, end) from a plain full scan"""
    rc, o, e = sh(f'samtools view {bam}')
    recs = []
    for line in o.splitlines():
        f = line.split('\t')
        pos = int(f[3])
        recs.append((line, f[2], pos, pos + reflen(f[5]) - 1))
    return recs


def truth(recs, regions):
    """multiset of lines overlapping ANY region (each record once)"""
    out = []
    for line, c, s, e in recs:
        if c == '*':
            continue
        if any(c == rc_ and s <= re_ and e >= rs for rc_, rs, re_ in regions):
            out.append(line)
    return collections.Counter(out)


def per_region_sum(recs, regions):
    """what N independent region queries print in total (each record once PER region it overlaps)"""
    n = 0
    for rc_, rs, re_ in regions:
        n += sum(1 for line, c, s, e in recs if c == rc_ and s <= re_ and e >= rs)
    return n


def bed_text(regions, zero_based=True):
    return ''.join(f'{c}\t{s - 1 if zero_based else s}\t{e}\n' for c, s, e in regions)


def run_sets(name, path, recs, sets, verbose=True):
    """returns dict of method -> number of sets where output == truth; and tallies"""
    tally = collections.Counter()
    dup_sets = 0
    for k, regions in enumerate(sets):
        T = truth(recs, regions)
        Tn = sum(T.values())
        regstr = ' '.join(f'{c}:{s}-{e}' for c, s, e in regions)
        # default (one query per region)
        rc, o, e = sh(f'samtools view {path} {regstr}; echo rc=$? >&2')
        dflt = collections.Counter(o.splitlines())
        dflt_n = sum(dflt.values())
        overl = per_region_sum(recs, regions)
        tally['default_eq_per_region_sum'] += (dflt_n == overl)
        tally['default_rc0'] += ('rc=0' in e)
        if dflt_n > Tn:
            dup_sets += 1
        # -M
        rc, o, e = sh(f'samtools view -M {path} {regstr}')
        tally['M'] += (collections.Counter(o.splitlines()) == T)
        # BED variants, 0-based half-open
        open(f'{W}/r.bed', 'w').write(bed_text(regions))
        rc, o, e = sh(f'samtools view -M -L {W}/r.bed {path}')
        tally['M_L'] += (collections.Counter(o.splitlines()) == T)
        rc, o, e = sh(f'samtools view --region-file {W}/r.bed {path}')
        tally['region_file'] += (collections.Counter(o.splitlines()) == T)
        rc, o, e = sh(f'samtools view -L {W}/r.bed {path}')
        tally['L_only'] += (collections.Counter(o.splitlines()) == T)
        # pysam
        with pysam.AlignmentFile(path) as bam:
            got = [r.to_string() for r in fetch_regions(bam, [(c, s - 1, e_) for c, s, e_ in regions])]
            names = collections.Counter(got)
            tally['fetch_regions_eq_truth'] += (names == T)
            tally['fetch_regions_no_dups'] += (max(names.values(), default=1) == 1 or all(v == 1 for v in names.values()))
            naive = sum(1 for c, s, e_ in regions for _ in bam.fetch(c, s - 1, e_))
            tally['naive_pysam_eq_default'] += (naive == dflt_n)
    return tally, dup_sets


# ---- part A: named region sets on the real BAM
recs = load(BAM)
check('full-scan model parsed all 5644 records (5642 placed + 2 unplaced)', len(recs) == 5644 and sum(1 for r in recs if r[1] == '*') == 2, len(recs))
named = {
    'overlap (Skill example)': [('chr22', 2000, 3000), ('chr22', 2500, 3500)],
    'adjacent, touching': [('chr22', 2000, 3000), ('chr22', 3001, 4000)],
    'nested': [('chr22', 2000, 4000), ('chr22', 2500, 3000)],
    'gap of 9 bp': [('chr22', 2000, 2100), ('chr22', 2110, 2200)],
    'gap of 100 bp': [('chr22', 2000, 2100), ('chr22', 2201, 2300)],
    'identical twice': [('chr22', 2000, 3000), ('chr22', 2000, 3000)],
    'three chained': [('chr22', 2000, 2300), ('chr22', 2250, 2600), ('chr22', 2580, 2900)],
    'reverse order given': [('chr22', 3000, 3500), ('chr22', 2000, 2600)],
    'single base each': [('chr22', 1952, 1952), ('chr22', 2000, 2000)],
    'disjoint far apart': [('chr22', 1952, 2000), ('chr22', 4000, 4100)],
}
truth_counts = {}
for label, regions in named.items():
    T = truth(recs, regions)
    truth_counts[label] = sum(T.values())
    tally, dup = run_sets(label, BAM, recs, [regions])
    note(f'set "{label}": truth {sum(T.values())}; default rows {per_region_sum(recs, regions)}', dict(tally))
    ok = all(tally[m] == 1 for m in ('M', 'M_L', 'region_file', 'fetch_regions_eq_truth', 'fetch_regions_no_dups', 'naive_pysam_eq_default', 'default_rc0', 'default_eq_per_region_sum'))
    check(f'region set "{label}": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth ({sum(T.values())}); default query = sum over regions ({per_region_sum(recs, regions)})',
          ok, dict(tally))

# the Skill's headline numbers (7356 / 5426)
reg = named['overlap (Skill example)']
open(f'{W}/r_ex.bed', 'w').write(bed_text(reg))
rc, o, e = sh(f'samtools view -c {BAM} chr22:2000-3000 chr22:2500-3500; samtools view -c -M {BAM} chr22:2000-3000 chr22:2500-3500; samtools view -c -M -L {W}/r_ex.bed {BAM}; samtools view -c --region-file {W}/r_ex.bed {BAM}')
check('Skill numbers reproduced: default 7356, -M 5426, -M -L 5426, --region-file 5426 (truth 5426)', o.split() == ['7356', '5426', '5426', '5426'] and truth_counts['overlap (Skill example)'] == 5426, o.split())

# ---- part B: BED coordinate convention (the Skill says the -L BED is 0-based half-open; is --region-file too?)
starts = sorted({r[2] for r in recs if r[1] == 'chr22'})[:3] + [2500]
ok_L = ok_R = True
det = []
for p in starts:
    Tzero = truth(recs, [('chr22', p, p)])            # 1-based single base p
    open(f'{W}/b0.bed', 'w').write(f'chr22\t{p - 1}\t{p}\n')      # 0-based half-open single base p
    open(f'{W}/b1.bed', 'w').write(f'chr22\t{p}\t{p + 1}\n')      # would be base p+1 if 0-based
    for opt, key in (('-M -L', 'L'), ('--region-file', 'R')):
        a = collections.Counter(sh(f'samtools view {opt} {W}/b0.bed {BAM}')[1].splitlines())
        b = collections.Counter(sh(f'samtools view {opt} {W}/b1.bed {BAM}')[1].splitlines())
        good = (a == Tzero)
        det.append((opt, p, sum(a.values()), sum(Tzero.values()), sum(b.values())))
        if key == 'L': ok_L &= good
        else: ok_R &= good
check('BED given as 0-based half-open (start-1, end) selects exactly the 1-based base p for -M -L (Skill comment)', ok_L, det[:4])
check('--region-file BED uses the same 0-based half-open convention (Skill lists it beside -M -L; convention not stated for it)', ok_R, det[4:])

# ---- part C: 60 random region sets on the real BAM
rng = random.Random(6006)
sets = []
for _ in range(60):
    k = rng.randint(2, 5)
    sets.append([('chr22', (s := rng.randint(1900, 4700)), s + rng.randint(0, 400)) for _ in range(k)])
tally, dup_sets = run_sets('random-real', BAM, recs, sets)
note('60 random sets on the real BAM: tally', dict(tally))
check('60 random multi-region sets (real BAM): -M, -M -L, --region-file, fetch_regions == truth in all 60; fetch_regions never repeats a record; default over-counts in some sets (meaningful test)',
      all(tally[m] == 60 for m in ('M', 'M_L', 'region_file', 'fetch_regions_eq_truth', 'fetch_regions_no_dups', 'default_eq_per_region_sum', 'default_rc0', 'naive_pysam_eq_default')) and dup_sets >= 10,
      f'{dict(tally)}; sets where default duplicates: {dup_sets}')
check('-L bed WITHOUT -M is also correct (full scan filter): informational agreement with truth', tally['L_only'] == 60, tally['L_only'])

# ---- part D: synthetic multi-contig BAM (placed unmapped read, secondary/supplementary, 66,000-op CIGAR)
sh(f'python {RUN}/regress/make_synth.py; cd {RUN}/data/synth; samtools sort -o synth.bam synth.sam; samtools index synth.bam')
SB = RUN + '/data/synth/synth.bam'
srecs = load(SB)
check('synthetic BAM: 15 records loaded, 1 unplaced', len(srecs) == 15 and sum(1 for r in srecs if r[1] == '*') == 1, len(srecs))
rng = random.Random(77)
ssets = []
for _ in range(80):
    k = rng.randint(2, 4)
    reg = []
    for _ in range(k):
        c = rng.choice(['ctg1', 'ctg1', 'ctg2', 'ctg3'])
        L = {'ctg1': 300, 'ctg2': 2000, 'ctg3': 40000}[c]
        s = rng.randint(1, L)
        reg.append((c, s, min(L, s + rng.randint(0, 200))))
    ssets.append(reg)
tally, dup_sets = run_sets('random-synth', SB, srecs, ssets)
note('80 random multi-contig sets on synthetic BAM: tally', dict(tally))
check('80 random multi-contig sets (synthetic BAM incl. placed-unmapped, secondary, supplementary, 66k-op CIGAR): -M, --region-file, -M -L, fetch_regions == truth; default = per-region sum',
      all(tally[m] == 80 for m in ('M', 'M_L', 'region_file', 'fetch_regions_eq_truth', 'fetch_regions_no_dups', 'default_eq_per_region_sum')),
      f'{dict(tally)}; sets with duplication in default: {dup_sets}')

# ---- part E: unindexed BAM and error paths for the recipes (Skill says -M needs an index only implicitly)
sh(f'cp {BAM} {W}/noidx.bam')
rc, o, e = sh(f'samtools view -M {W}/noidx.bam chr22:2000-3000 chr22:2500-3500; echo rc=$?')
note('-M on an UNINDEXED BAM', (o[-40:] + e).strip().replace('\n', ' | ')[:200])
check('-M on an unindexed BAM fails loudly (non-zero rc, message names the index) and prints no records', 'rc=0' not in o and 'index' in e.lower(), (o[-30:] + e).strip()[:200])
rc, o, e = sh(f'samtools view {BAM} chr22:2000-3000 22:1-50; echo rc=$?')
check('unknown contig mixed in a multi-region call: warning on stderr, still exit 0, records of the good region present', 'rc=0' in o and 'invalid region or unknown reference' in e and len(o.splitlines()) > 100, e.strip()[:160])
rc, o, e = sh(f'samtools view -M {BAM} chr22:2000-3000 22:1-50; echo rc=$?')
note('-M with an unknown contig mixed in', (o[-20:] + e).strip().replace('\n', ' | ')[:200])
# fetch_regions with unknown contig: pysam raises ValueError
try:
    with pysam.AlignmentFile(BAM) as bam:
        list(fetch_regions(bam, [('22', 0, 50)]))
    check('fetch_regions with a wrong contig name raises (no silent empty result)', False, 'no exception')
except ValueError as ex:
    check('fetch_regions with a wrong contig name raises ValueError (no silent empty result)', True, str(ex)[:100])
# empty region list
with pysam.AlignmentFile(BAM) as bam:
    check('fetch_regions on an empty region list yields nothing', list(fetch_regions(bam, [])) == [], 'ok')
