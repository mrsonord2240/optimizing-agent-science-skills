#!/usr/bin/env python3
"""Input 3 (edge/boundary): region + BED filtering, the shipped examples/filter_bam.py, CRAM output.
Ground truth = own overlap arithmetic over every record (1-based inclusive regions, 0-based half-open BED)."""
import os, subprocess, sys, shutil, collections
import pysam

AFD = os.environ['AFDATA']
W = sys.argv[1]; SK = sys.argv[2]
os.makedirs(W, exist_ok=True)
fails = []
def check(name, cond, detail=''):
    print(('PASS' if cond else 'FAIL'), name, detail)
    if not cond: fails.append(name)
def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

src = f'{AFD}/human/test.paired_end.sorted.bam'
inp = f'{W}/input.bam'; shutil.copy(src, inp); shutil.copy(src + '.bai', inp + '.bai')
allr = [(r.query_name, r.flag, r.reference_start, r.reference_end if r.reference_end else r.reference_start + 1)
        for r in pysam.AlignmentFile(inp)]   # start 0-based, end exclusive (placed unmapped = 1 bp)
print('records', len(allr))
def key(t): return (t[0], t[1])
def qn(bam):
    return sorted((r.query_name, r.flag) for r in pysam.AlignmentFile(bam))

# ---- A. samtools region, 1-based inclusive ----
for (a, b) in [(1952, 2100), (2500, 2500), (4617, 4700), (3000, 3200)]:
    out = f'{W}/region_{a}_{b}.bam'
    rc, _, se = sh(f'samtools view -b -o {out} {inp} chr22:{a}-{b}')
    exp = sorted(key(t) for t in allr if (t[2] + 1) <= b and t[3] >= a)
    check(f'samtools region chr22:{a}-{b} == 1-based-inclusive overlap', qn(out) == exp, f'{len(exp)} reads')
# multi-region (SKILL.md)
out = f'{W}/multi.bam'
sh(f'samtools view -b -o {out} {inp} chr22:1952-2100 chr22:3000-3200')
exp = sorted(key(t) for t in allr if ((t[2]+1) <= 2100 and t[3] >= 1952) or ((t[2]+1) <= 3200 and t[3] >= 3000))
check('samtools multi-region == union of overlaps (no duplicated records)', qn(out) == exp, f'{len(exp)}')
# region command w/ output flag AFTER regions (usage-guide order: view input region -o out)
out = f'{W}/ug_order.bam'
rc, _, se = sh(f'samtools view {inp} chr22:1952-2100 -o {out}')
check('usage-guide arg order "view in.bam region -o out" works', rc == 0 and len(qn(out)) == len([t for t in allr if (t[2]+1) <= 2100 and t[3] >= 1952]), se[:80])
# the literal example region from SKILL.md on this contig naming: chr1 does not exist
rc, so, se = sh(f'samtools view -o {W}/x.bam {inp} chr1:1000000-2000000')
print('literal SKILL.md region chr1:1000000-2000000 ->', rc, se.strip()[:120], '| records in output', len(qn(f'{W}/x.bam')) if os.path.exists(f'{W}/x.bam') else 'no file')
# unindexed input + region
noidx = f'{W}/noindex.bam'; shutil.copy(src, noidx)
rc, so, se = sh(f'samtools view -o {W}/y.bam {noidx} chr22:1952-2100')
check('region on unindexed BAM gives an error', rc != 0, se.strip()[:120])

# ---- C. BED ----
bed = f'{W}/targets.bed'
open(bed, 'w').write('chr22\t1951\t2100\nchr22\t2000\t2300\nchr22\t3000\t3200\n')   # first two overlap
rc, _, se = sh(f'samtools view -b -L {bed} -o {W}/L.bam {inp}')
ivs = [(1951, 2100), (2000, 2300), (3000, 3200)]
exp = sorted(key(t) for t in allr if any(t[2] < e and t[3] > s for s, e in ivs))
check('samtools -L BED == 0-based half-open overlap, each read once', qn(f'{W}/L.bam') == exp, f'{len(exp)}')
# pysam recipe (verbatim from SKILL.md)
def read_bed(bed_path):
    regions = []
    with open(bed_path) as f:
        for line in f:
            if line.startswith('#'): continue
            parts = line.strip().split('\t')
            regions.append((parts[0], int(parts[1]), int(parts[2])))
    return regions
regions = read_bed(bed)
with pysam.AlignmentFile(inp, 'rb') as infile:
    with pysam.AlignmentFile(f'{W}/targets_pysam.bam', 'wb', header=infile.header) as outfile:
        for chrom, start, end in regions:
            for read in infile.fetch(chrom, start, end):
                outfile.write(read)
got = qn(f'{W}/targets_pysam.bam')
cnt = collections.Counter(got)
dups = sum(v - 1 for v in cnt.values() if v > 1)
print(f'pysam BED recipe wrote {len(got)} records; samtools -L wrote {len(exp)}; duplicated records {dups}')
check('pysam BED recipe == samtools -L (reads overlapping two BED rows are written once)', got == exp)
# is the pysam output even sorted?
pos = [r.reference_start for r in pysam.AlignmentFile(f'{W}/targets_pysam.bam')]
print('pysam BED recipe output coordinate-sorted:', pos == sorted(pos))
# BED with header line / blank line
bed2 = f'{W}/targets_hdr.bed'
open(bed2, 'w').write('track name="t"\nchr22\t1951\t2100\n\nchr22\t3000\t3200\n')
try:
    read_bed(bed2); print('pysam read_bed on track/blank-line BED: ok')
except Exception as e:
    print('pysam read_bed on BED with track line ->', type(e).__name__, e)
rc, so, se = sh(f'samtools view -c -L {bed2} {inp}')
print('samtools -L on same BED: rc', rc, 'count', so.strip(), se.strip()[:100])
# BED chrom absent from header
bed3 = f'{W}/absent.bed'; open(bed3, 'w').write('chr1\t100\t200\n')
rc, so, se = sh(f'samtools view -c -L {bed3} {inp}')
print('samtools -L with chr absent from header: rc', rc, 'count', so.strip())

# ---- D. shipped examples/filter_bam.py (run from the copy) ----
FB = f'{SK}/examples/filter_bam.py'
def fb(args, out):
    return sh(f'python {FB} {inp} {out} {args}')
# D1 no filters: kept everything mapped
rc, so, se = fb('', f'{W}/fb_none.bam')
print('fb none:', so.replace('\n', ' | '), se[-200:])
n_mapped = sum(1 for t in allr if not t[1] & 4)
check('fb no-filter keeps all mapped (5642)', f'Kept: {n_mapped:,}' in so, so.strip().replace('\n',' '))
# D2 combined flags vs samtools
rc, so, se = fb('-q 30 -d -p -P', f'{W}/fb_all.bam')
rc2, so2, _ = sh(f'samtools view -c -F 4 -F 256 -F 2048 -F 1024 -f 2 -q 30 {inp}')
print('fb -q30 -d -p -P ->', so.replace('\n',' | '), '| samtools equiv count', so2.strip())
check('fb -q 30 -d -p -P Kept == samtools -f2 -F3332 -q30', f'Kept: {int(so2):,}' in so)
check('fb output indexed (.bai exists and opens)', os.path.exists(f'{W}/fb_all.bam.bai'))
# D3 region: off-by-one vs samtools
diffs = []
for a in [1952, 2000, 2500, 3000]:
    b = a + 60
    rc, so, se = fb(f'-r chr22:{a}-{b}', f'{W}/fb_r.bam')
    rc, _, _ = sh(f'samtools view -b -F 4 -o {W}/st_r.bam {inp} chr22:{a}-{b}')
    s_set = set(qn(f'{W}/st_r.bam')); f_set = set(qn(f'{W}/fb_r.bam'))
    diffs.append((a, b, len(s_set), len(f_set), len(s_set - f_set), len(f_set - s_set)))
print('region  (start,end, samtools_n, script_n, only_samtools, only_script):')
for d in diffs: print('  ', d)
# pick boundary where a read's last base == region start
lasts = sorted({t[3] for t in allr if not t[1] & 4})
L = next(l for l in lasts if l > 1960)
rc, so, se = fb(f'-r chr22:{L}-{L+40}', f'{W}/fb_b.bam')
sh(f'samtools view -b -F 4 -o {W}/st_b.bam {inp} chr22:{L}-{L+40}')
d = set(qn(f'{W}/st_b.bam')) - set(qn(f'{W}/fb_b.bam'))
check(f'fb region start==read last base (chr22:{L}-): script matches samtools (1-based) semantics', len(d) == 0, f'reads samtools returns but script drops: {len(d)}')
# D4 unusual region strings
for reg in ['chr22', 'chr22:1952', 'chr22:1,952-2,100', 'chr22:1952-2100', 'chr22:1-99999999']:
    rc, so, se = fb(f'-r {reg}', f'{W}/fb_u.bam')
    print(f'fb -r {reg!r}: rc={rc}', (so.strip().replace('\n',' | ') if rc == 0 else se.strip().splitlines()[-1]))
# D5 unindexed input + region; name-sorted input (index step)
noi = f'{W}/noindex.bam'
rc, so, se = sh(f'python {FB} {noi} {W}/fb_ni.bam -r chr22:1952-2100')
print('fb region on unindexed: rc', rc, se.strip().splitlines()[-1])
ns = f'{AFD}/human/test.paired_end.name.sorted.bam'
rc, so, se = sh(f'python {FB} {ns} {W}/fb_ns.bam -q 30')
print('fb on name-sorted input: rc', rc, (se.strip().splitlines()[-1] if rc else so.strip().replace("\n"," | ")), '| output exists', os.path.exists(f'{W}/fb_ns.bam'))
# D6 colon in contig name (real UMI BAM: contig chr22:16570000-16610000)
umi = f'{AFD}/human/test.paired_end.umi_unsorted.bam'
sh(f'samtools sort -o {W}/umi_sorted.bam {umi} && samtools index {W}/umi_sorted.bam')
hdr = sh(f'samtools view -H {W}/umi_sorted.bam | grep ^@SQ')[1].strip()
print('umi contig header:', hdr)
contig = 'chr22:16570000-16610000'
rc, so, se = sh(f"python {FB} {W}/umi_sorted.bam {W}/fb_c.bam -r '{contig}:16570100-16570300'")
print('fb region on colon-named contig: rc', rc, (se.strip().splitlines()[-1] if rc else so.strip()))
rc, so, se = sh(f"samtools view -c {W}/umi_sorted.bam '{{{contig}}}:100-300'")
print('samtools brace syntax {contig}:100-300 ->', rc, so.strip(), se.strip()[:80])
rc, so, se = sh(f"samtools view -c {W}/umi_sorted.bam '{contig}:100-300'")
print('samtools without braces ->', rc, so.strip(), se.strip()[:100])

# ---- E. CRAM output/input (usage-guide "Output Options") ----
ref = f'{AFD}/human/genome.fasta'
cr = f'{W}/out.cram'
rc, so, se = sh(f'samtools view -C -T {ref} -F 4 -o {cr} {inp}')
check('usage-guide CRAM output (-C -T ref -F 4)', rc == 0 and os.path.getsize(cr) > 0, se[:80])
rc, so, se = sh(f'samtools view -c -T {ref} {cr}')
check('CRAM round trip count == 5642 mapped', so.strip() == '5642', so.strip())
rc, so, se = sh(f'samtools view -c {cr}')
print('CRAM read without -T: rc', rc, so.strip(), se.strip()[:120])
rc, so, se = sh(f'python {FB} {cr} {W}/fb_cram.bam')
print('fb on CRAM without reference: rc', rc, (se.strip().splitlines()[-1] if rc else so.strip().replace("\n"," | ")))
print('\nFAILS:', fails)
