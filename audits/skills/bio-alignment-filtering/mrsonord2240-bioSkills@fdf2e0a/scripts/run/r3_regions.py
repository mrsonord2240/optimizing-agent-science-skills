#!/usr/bin/env python3
"""Input 3 (regression, Edge): regions, -L BED, the pysam region and BED recipes, the shipped examples/filter_bam.py.
Recipes are EXTRACTED from the fixed SKILL.md and executed. Ground truth: own overlap arithmetic (1-based inclusive
regions, 0-based half-open BED) AND, second method, `samtools view -L`/`samtools view <region>` record-for-record.
Fuzz part: 80 random BEDs and 120 random region strings on three real BAMs (paired, spliced RNA, 1000G)."""
import os, random, shutil, subprocess, sys
import pysam
from lib import check, sh, block, finish

AFD = os.environ['AFDATA']; W = sys.argv[1]; SK = sys.argv[2]
MD = f'{SK}/SKILL.md'; FB = f'{SK}/examples/filter_bam.py'
os.makedirs(W, exist_ok=True)
rnd = random.Random(20260920)

BAMS = {'human_PE': f'{AFD}/human/test.paired_end.sorted.bam',
        'rna_spliced': f'{AFD}/human/test.rna.paired_end.sorted.bam',
        '1000g': f'{AFD}/1000g/HG00349.chr20_1400000-1500000.bam'}
def recs(bam):
    return [r.to_string() for r in pysam.AlignmentFile(bam)]

# ---------------- A. samtools region / BED semantics quoted in the text ----------------
src = BAMS['human_PE']
inp = f'{W}/input.bam'; shutil.copy(src, inp); shutil.copy(src + '.bai', inp + '.bai')
allr = [(r.query_name, r.flag, r.reference_start, r.reference_end if r.reference_end else r.reference_start + 1)
        for r in pysam.AlignmentFile(inp)]
def qn(bam): return sorted((r.query_name, r.flag) for r in pysam.AlignmentFile(bam))
for a, b in [(1952, 2100), (2500, 2500), (4617, 4700), (3000, 3200), (1, 1951), (1, 1952)]:
    out = f'{W}/reg.bam'
    sh(f'samtools view -b -o {out} {inp} chr22:{a}-{b}')
    exp = sorted((t[0], t[1]) for t in allr if (t[2] + 1) <= b and t[3] >= a)
    check(f'samtools chr22:{a}-{b} == 1-based inclusive overlap', qn(out) == exp, f'{len(exp)} reads')
rc, so, se = sh(f'samtools view -c {inp} chr1:1000000-2000000')
check('text: absent contig -> warning, zero reads, rc 0', rc == 0 and so.strip() == '0' and se.strip() != '', f'rc={rc} n={so.strip()} err={se.strip()[:60]!r}')
noidx = f'{W}/noindex.bam'; shutil.copy(src, noidx)
rc, so, se = sh(f'samtools view -c {noidx} chr22:1952-2100')
check('text: region needs an index (error on unindexed BAM)', rc != 0, se.strip()[:100])
# -L: each read once, BED header lines skipped
bed = f'{W}/t.bed'
open(bed, 'w').write('track name=x\n# c\nbrowser position\n\nchr22\t1951\t2100\nchr22\t2000\t2300\nchr22\t3000\t3200\n')
rc, so, se = sh(f'samtools view -c -L {bed} {inp}')
ivs = [(1951, 2100), (2000, 2300), (3000, 3200)]
exp = sum(1 for t in allr if any(t[2] < e and t[3] > s for s, e in ivs))
check('text: -L skips track/#/browser/blank lines; each overlapping read written once', rc == 0 and int(so) == exp, f'{so.strip()} vs {exp}; err={se.strip()[:60]!r}')
# -P claim: mates outside the region are retrieved (needs index)
rc, plain, _ = sh(f'samtools view {inp} chr22:1952-1960')
rc, withP, se = sh(f'samtools view -P {inp} chr22:1952-1960')
names_plain = {l.split('\t')[0] for l in plain.splitlines()}
mates_in = {l.split('\t')[0] for l in withP.splitlines()}
check('-P adds mates that lie outside the region (templates whole)', len(withP.splitlines()) > len(plain.splitlines()) and names_plain <= mates_in, f'{len(plain.splitlines())} -> {len(withP.splitlines())}')
rc, so, se = sh(f'samtools view -P {noidx} chr22:1952-1960')
check('-P without an index is an error (text says "needs ... an index")', rc != 0, se.strip()[:80])
# -q with -L
rc, so, _ = sh(f'samtools view -c -q 30 -L {bed} {inp}')
exp = sum(1 for r in pysam.AlignmentFile(inp) if r.mapping_quality >= 30 and any(r.reference_start < e and (r.reference_end or r.reference_start + 1) > s for s, e in ivs))
check('text: "-q 30 -L targets.bed" == both conditions', int(so) == exp, f'{so.strip()} vs {exp}')
# CRAM output line
ref = f'{AFD}/human/genome.fasta'
rc, so, se = sh(f'samtools view -C -T {ref} -F 4 -o {W}/out.cram {inp}')
rc2, so2, _ = sh(f'samtools view -c -T {ref} {W}/out.cram')
check('Output Options: CRAM with -T reference round-trips 5642 mapped', rc == 0 and so2.strip() == '5642', so2.strip())

# ---------------- B. pysam region rule and recipe ----------------
def pysam_region(bam, contig, a, b, out):
    with pysam.AlignmentFile(bam) as fin, pysam.AlignmentFile(out, 'wb', header=fin.header) as fo:
        for r in fin.fetch(contig, a - 1, b):
            fo.write(r)
mism = 0
for _ in range(60):
    a = rnd.randint(1, 4700); b = rnd.randint(a, 4800)
    pysam_region(inp, 'chr22', a, b, f'{W}/pr.bam')
    sh(f'samtools view -b -o {W}/sr.bam {inp} chr22:{a}-{b}')
    if recs(f'{W}/pr.bam') != recs(f'{W}/sr.bam'): mism += 1
check("pysam rule fetch(c, start-1, end) == samtools c:start-end, 60 random regions", mism == 0, f'mismatches {mism}')
code = block(MD, 'Filter by Region', 'python', 'fetch').replace("'input.bam'", f"'{inp}'").replace("'chr1', 999999, 2000000", "'chr22', 1951, 2100").replace("'region.bam'", f"'{W}/snip_region.bam'")
exec(compile(code, 'region_snippet', 'exec'), {})
sh(f'samtools view -b -o {W}/sr.bam {inp} chr22:1952-2100')
check('SKILL.md pysam region snippet (adapted 1-based 1952-2100) == samtools', recs(f'{W}/snip_region.bam') == recs(f'{W}/sr.bam'), f'{len(recs(f"{W}/sr.bam"))} records')

# ---------------- C. pysam BED recipe (extracted) vs samtools -L ----------------
recipe = block(MD, 'Filter from BED File', 'python', 'merged')
def run_recipe(bam, bedtext, tag):
    d = f'{W}/bedrun_{tag}'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    shutil.copy(bam, f'{d}/input.bam')
    if os.path.exists(bam + '.bai'): shutil.copy(bam + '.bai', f'{d}/input.bam.bai')
    else: pysam.index(f'{d}/input.bam')
    open(f'{d}/targets.bed', 'w', newline='').write(bedtext)
    cwd = os.getcwd(); os.chdir(d)
    try:
        exec(compile(recipe, 'bed_recipe', 'exec'), {})
    finally:
        os.chdir(cwd)
    rc, so, se = sh(f'samtools view -b -L targets.bed -o st.bam input.bam', cwd=d)
    return recs(f'{d}/targets.bam'), recs(f'{d}/st.bam'), rc, pysam.AlignmentFile(f'{d}/targets.bam').header.to_dict()['HD']

bt = 'track name="t"\n# comment\n\nchr22\t1951\t2100\nchr22\t2000\t2300\nchr22\t3000\t3200\nchr22\t2500\t2500\nchr1\t5\t50\nbrowser position chr22:1-100\nchr22\t3100\t3150\n'
a, b, rc, hd = run_recipe(inp, bt, 'fixerbed')
check('BED recipe (track/#/browser/blank/zero-width/unknown contig/nested rows) == samtools -L, record-for-record in order', a == b and len(a) > 0, f'{len(a)} vs {len(b)}')
check('output header keeps SO:coordinate', hd.get('SO') == 'coordinate', str(hd))
# naive loop count for comparison (the defect the fix removed)
# adversarial-format BEDs
cases = {
    'crlf': 'chr22\t1951\t2100\r\nchr22\t3000\t3200\r\n',
    '6col_names': 'chr22\t1951\t2100\tnameA\t0\t+\nchr22\t3000\t3200\tnameB\t0\t-\n',
    'no_trailing_newline': 'chr22\t1951\t2100\nchr22\t3000\t3200',
    'unsorted_reverse': 'chr22\t3000\t3200\nchr22\t1951\t2100\n',
    'touching': 'chr22\t1951\t2100\nchr22\t2100\t2300\n',
    'contained': 'chr22\t1951\t4000\nchr22\t2000\t2100\n',
    'space_delimited': 'chr22 1951 2100\nchr22 3000 3200\n',
    'whole_contig_huge_end': 'chr22\t0\t999999999\n',
}
for nm, txt in cases.items():
    try:
        a, b, rc, hd = run_recipe(inp, txt, nm)
        check(f'BED recipe on {nm} BED == samtools -L', a == b, f'{len(a)} vs {len(b)}')
    except Exception as e:
        check(f'BED recipe on {nm} BED == samtools -L', False, f'{type(e).__name__}: {str(e)[:80]}')
# fuzz on three real BAMs
def rand_bed(bam_key, zero_ok=True):
    rows = []
    if bam_key == '1000g':
        lo, hi, chrom = 1_400_000, 1_500_000, 'chr20'
    else:
        lo, hi, chrom = 0, 4800, 'chr22'
    for _ in range(rnd.randint(1, 8)):
        s = rnd.randint(lo, hi - 1); w = rnd.choice(([0] if zero_ok else []) + [1, 30, 150, 500, 3000, 20000])
        rows.append((chrom, s, min(s + w, hi + 50)))
    if rnd.random() < .3: rows.append(('chrUnknown', 1, 100))
    if rnd.random() < .3: rows.append(('chr1', 100, 900))
    lines = []
    if rnd.random() < .3: lines.append('track name=fuzz\n')
    lines += [f'{c}\t{s}\t{e}\n' for c, s, e in rows]
    return ''.join(lines)
def fuzz(zero_ok, label):
    bad = 0; nonempty = 0; nzw = 0
    for key, path in BAMS.items():
        for i in range(27):
            txt = rand_bed(key, zero_ok)
            a, b, rc, hd = run_recipe(path, txt, f'fz{label}{key}{i}')
            nonempty += len(b) > 0
            has_zero = any(l.split('	')[1:3] and l.split('	')[1] == l.split('	')[2].strip() for l in txt.splitlines() if l.startswith('chr'))
            if a != b:
                bad += 1
                nzw += has_zero
                if bad <= 3:
                    print(f'   MISMATCH {label} {key} #{i}: pysam {len(a)} vs samtools {len(b)}; only-pysam {len(set(a)-set(b))}, only-samtools {len(set(b)-set(a))}; BED has zero-width row: {has_zero}')
                    print('      BED:', txt.replace(chr(10), ' | ').replace(chr(9), ' '))
    return bad, nonempty, nzw
bad, nonempty, nzw = fuzz(False, 'nz')
check('BED recipe fuzz, no zero-width rows: 81 random BEDs on 3 real BAMs (paired, spliced RNA, 1000G) identical to samtools -L in content and order', bad == 0, f'mismatching BEDs {bad}; non-empty outputs {nonempty}/81')
bad, nonempty, nzw = fuzz(True, 'zw')
print(f'   fuzz WITH zero-width rows: {bad}/81 BEDs differ from samtools -L; {nzw} of those {bad} contain a start==end row')
check('BED recipe fuzz, zero-width (start==end) rows allowed: identical to samtools -L (text claims "same records as samtools view -L")', bad == 0, f'{bad}/81 differ')
# characterise the zero-width difference on the 1000G BAM at a position with reads
g = BAMS['1000g']; s0 = 1433164
d = f'{W}/zw'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
open(f'{d}/z.bed', 'w').write('chr20\t%d\t%d\n' % (s0, s0))
sh(f'samtools view -b -L {d}/z.bed -o {d}/z.bam {g}')
zs = sorted(r.query_name + str(r.flag) for r in pysam.AlignmentFile(f'{d}/z.bam'))
with pysam.AlignmentFile(g) as fin:
    f_zero = sorted(r.query_name + str(r.flag) for r in fin.fetch('chr20', s0, s0))
    f_one = sorted(r.query_name + str(r.flag) for r in fin.fetch('chr20', s0, s0 + 1))
    cover = sorted(r.query_name + str(r.flag) for r in pysam.AlignmentFile(g) if r.reference_name == 'chr20' and r.reference_end and r.reference_start <= s0 < r.reference_end)
print(f'   zero-width BED chr20 {s0} {s0}: samtools -L {len(zs)} reads; pysam fetch(s,s) {len(f_zero)}; fetch(s,s+1) {len(f_one)}; reads covering 0-based pos s {len(cover)}')
check('samtools -L treats a zero-width row as the single base at 0-based s (== fetch(s, s+1))', zs == f_one == cover and len(zs) > 0)
check('pysam fetch(c, s, s) on a zero-width row returns nothing (so the recipe drops what samtools keeps)', f_zero == [])

# ---------------- D. shipped examples/filter_bam.py ----------------
def fb(bam, out, args):
    return sh(f'python {FB} {bam} {out} {args}')
truth_map = {}
def st_count(bam, region): return int(sh(f"samtools view -c -F 4 {bam} '{region}'")[1])
for reg, kind in [('chr22', 'bare contig'), ('chr22:1952', 'contig:start'), ('chr22:1952-', 'open end'), ('chr22:1,952-2,100', 'commas'),
                  ('chr22:1952-2100', '1-based start'), ('chr22:2043-2043', 'single base'), ('chr22:4617-4700', 'end of coverage'),
                  ('chr22:1-99999999', 'huge end'), ('chr22:0-100', 'zero start')]:
    rc, so, se = fb(inp, f'{W}/fb.bam', f"-r '{reg}'")
    rc2, so2, se2 = sh(f"samtools view -c -F 4 {inp} '{reg}'")
    if rc2 != 0 or not so2.strip().isdigit():
        print(f'   (samtools rejects {reg!r}: {se2.strip()[:60]}) script rc={rc}: {(se or so).strip().splitlines()[-1][:80]}')
        check(f'filter_bam -r {reg} ({kind}): both tools refuse it', rc != 0, '')
        continue
    n = int(so2)
    check(f'filter_bam -r {reg} ({kind}) Kept == samtools -F 4 count', rc == 0 and f'Kept: {n:,}' in so, f'kept {so.split(chr(10))[0]} samtools {n}')
# fuzz: 120 random regions, output records identical (mapped only) to samtools
bad = 0
for i in range(120):
    a = rnd.randint(1, 4700); b = rnd.randint(a, 4900)
    fmt = rnd.choice(['plain', 'comma', 'open'])
    reg = {'plain': f'chr22:{a}-{b}', 'comma': f'chr22:{a:,}-{b:,}', 'open': f'chr22:{a}'}[fmt]
    rc, so, se = fb(inp, f'{W}/fb.bam', f"-r '{reg}'")
    sh(f"samtools view -b -F 4 -o {W}/st.bam {inp} '{reg}'")
    if rc != 0 or recs(f'{W}/fb.bam') != recs(f'{W}/st.bam'): bad += 1
check('filter_bam -r fuzz: 120 random regions (plain/comma/open) record-identical to samtools -F 4 region', bad == 0, f'mismatches {bad}')
# region boundary: read whose last base == region start
lasts = sorted({t[3] for t in allr if not t[1] & 4})
L = next(l for l in lasts if l > 1960)
rc, so, se = fb(inp, f'{W}/fb_b.bam', f'-r chr22:{L}-{L+40}')
sh(f'samtools view -b -F 4 -o {W}/st_b.bam {inp} chr22:{L}-{L+40}')
check(f'region start == last base of a read (chr22:{L}-): identical to samtools', recs(f'{W}/fb_b.bam') == recs(f'{W}/st_b.bam'), f'{len(recs(f"{W}/st_b.bam"))} reads')
# bad regions: clean error, no output
for reg in ['chrX:1-100', 'chr22:abc', 'chr22:100-50', 'chr22:-100', ':']:
    if os.path.exists(f'{W}/fb_bad.bam'): os.remove(f'{W}/fb_bad.bam')
    rc, so, se = fb(inp, f'{W}/fb_bad.bam', f"-r '{reg}'")
    last = (se.strip().splitlines() or [''])[-1]
    print(f'   bad region {reg!r}: rc={rc} out_exists={os.path.exists(f"{W}/fb_bad.bam")} msg={last[:90]!r}')
    check(f'bad region {reg!r}: non-zero exit, message, no Traceback', rc != 0 and 'Traceback' not in se, last[:70])
# unindexed input
rc, so, se = fb(noidx, f'{W}/fb_ni.bam', '-r chr22:1952-2100')
check('unindexed input + -r: clean message', rc != 0 and 'no index' in se and 'Traceback' not in se, se.strip()[-90:])
# name-sorted input
ns = f'{AFD}/human/test.paired_end.name.sorted.bam'
rc, so, se = fb(ns, f'{W}/fb_ns.bam', '-q 30')
check('name-sorted input: runs, output not indexed, says so', rc == 0 and not os.path.exists(f'{W}/fb_ns.bam.bai') and 'not SO:coordinate' in so, so.strip().replace('\n', ' | ')[:120])
# colon contig (real UMI BAM: contig chr22:16570000-16610000)
umi = f'{AFD}/human/test.paired_end.umi_unsorted.bam'
sh(f'samtools sort -o {W}/umi_sorted.bam {umi} && samtools index {W}/umi_sorted.bam')
contig = 'chr22:16570000-16610000'
print('   header @SQ:', sh(f'samtools view -H {W}/umi_sorted.bam | grep ^@SQ')[1].strip())
for sub in ['', ':16570100-16570300', ':1952-2100', ':1,952-2,100']:
    reg = contig + sub
    rc, so, se = fb(f'{W}/umi_sorted.bam', f'{W}/fb_c.bam', f"-r '{reg}'")
    rc2, so2, se2 = sh(f"samtools view -c -F 4 {W}/umi_sorted.bam '{{{contig}}}{sub.replace(',', '')}'")
    rc3, so3, se3 = sh(f"samtools view -c -F 4 {W}/umi_sorted.bam '{reg}'")
    print(f'   colon-contig region {reg!r}: script rc={rc} {so.splitlines()[0] if so else se.strip()[-60:]}; samtools braces {so2.strip()}; samtools plain {so3.strip()} {se3.strip()[:50]}')
    exp = so2.strip()
    check(f'filter_bam colon-contig {reg!r} Kept == samtools brace-syntax count', rc == 0 and f'Kept: {int(exp):,}' in so, f'{exp}')
# -q/-d/-p/-P combos vs samtools
rc, so, se = fb(inp, f'{W}/fb_all.bam', '-q 30 -d -p -P')
rc2, so2, _ = sh(f'samtools view -c -f 2 -F 3332 -q 30 {inp}')
check('filter_bam -q 30 -d -p -P Kept == samtools -f 2 -F 3332 -q 30 (5638 expected per TOOLS.md order of magnitude)', f'Kept: {int(so2):,}' in so, f'{so.splitlines()[0]} vs {so2.strip()}')
check('filter_bam output indexed when coordinate-sorted', os.path.exists(f'{W}/fb_all.bam.bai'))
a = recs(f'{W}/fb_all.bam'); sh(f'samtools view -b -f 2 -F 3332 -q 30 -o {W}/st_all.bam {inp}')
check('filter_bam -q 30 -d -p -P records identical to samtools -f 2 -F 3332 -q 30', a == recs(f'{W}/st_all.bam'))
# -d warning on unmarked BAM
pd = f'{AFD}/derived/planted_dups.bam'
rc, so, se = fb(pd, f'{W}/fb_pd.bam', '-d')
check('-d on an unmarked BAM prints the WARNING and keeps 500', 'WARNING' in se and 'Kept: 500' in so, se.strip()[:100])
rc, so, se = fb(f'{AFD}/1000g/HG00349.chr20_1400000-1500000.bam', f'{W}/fb_g.bam', '-d')
check('-d on a marked BAM: no warning, removes 101 dup-flagged among mapped', 'WARNING' not in se and 'Removed:' in so, so.strip().replace('\n', ' | '))
# CRAM without reference: what does the script do?
rc, so, se = fb(f'{W}/out.cram', f'{W}/fb_cram.bam', '')
print('   filter_bam on CRAM without reference: rc', rc, (se or so).strip().splitlines()[-1][:120] if (se or so).strip() else '')
# filter_bam.py -r on two more real BAMs (1000G: many-contig header, chr20; spliced RNA-seq): 30 random regions each vs samtools
for label, path, contig, lo, hi in [('1000g', BAMS['1000g'], 'chr20', 1400001, 1500000), ('rna', BAMS['rna_spliced'], 'chr22', 1, 4800)]:
    d = f'{W}/fb_{label}'; os.makedirs(d, exist_ok=True); shutil.copy(path, f'{d}/in.bam'); pysam.index(f'{d}/in.bam')
    bad = 0; nz = 0
    for i in range(30):
        a = rnd.randint(lo, hi); b = rnd.randint(a, min(a + rnd.choice([100, 2000, 30000]), hi + 100))
        reg = f'{contig}:{a:,}-{b:,}' if i % 2 else f'{contig}:{a}-{b}'
        rc, so, se = fb(f'{d}/in.bam', f'{d}/fb.bam', f"-r '{reg}'")
        sh(f"samtools view -b -F 4 -o {d}/st.bam {d}/in.bam '{contig}:{a}-{b}'")
        nz += len(recs(f'{d}/st.bam')) > 0
        if rc != 0 or recs(f'{d}/fb.bam') != recs(f'{d}/st.bam'): bad += 1
    check(f'filter_bam -r on real {label} BAM: 30 random regions record-identical to samtools -F 4 region', bad == 0, f'mismatches {bad}; non-empty {nz}/30')
# -P together with -L (text: "needs a region or -L, and an index")
bedP = f'{W}/p.bed'; open(bedP, 'w').write('chr22\t1951\t1960\n')
rc, plain, _ = sh(f'samtools view -L {bedP} {inp}'); rc2, withP, se = sh(f'samtools view -P -L {bedP} {inp}')
check('-P with -L BED retrieves mates outside the BED region', rc2 == 0 and len(withP.splitlines()) > len(plain.splitlines()), f'{len(plain.splitlines())} -> {len(withP.splitlines())} err={se.strip()[:60]}')
rc3, so3, se3 = sh(f'samtools view -P {inp}')
print('   -P without region or -L: rc', rc3, se3.strip()[:100])
check('-P without a region/-L is an error or no-op (text says it needs one)', rc3 != 0 or len(so3.splitlines()) == 5644, f'rc={rc3}')
finish()
