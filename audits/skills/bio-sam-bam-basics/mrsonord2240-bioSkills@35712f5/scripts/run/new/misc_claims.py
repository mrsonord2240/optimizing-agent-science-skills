"""Input 1 add-on (canonical use): small claims in the fixed SKILL.md that no earlier script covers, on the real human PE BAM.
Each line is a statement the Skill makes; the check runs it and asserts on the output.
"""
import os, re, sys
os.environ['AUDIT_INPUT'] = '1'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regress'))
from chk import check, note, sh
import pysam

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.environ['AFDATA'] + '/human'
BAM, REF, CRAM = D + '/test.paired_end.sorted.bam', D + '/genome.fasta', D + '/test.paired_end.sorted.cram'
W = RUN + '/data/misc'
sh(f'rm -rf {W}; mkdir -p {W}')
ENV = {'REF_PATH': '', 'REF_CACHE': ''}

# "keep -h when piping to another samtools/BAM writer, or the header is lost"
rc, o, e = sh(f'samtools view {BAM} | head -200 | samtools view -b -o {W}/nohdr.bam - ; echo rc=$?')
rc2, o2, e2 = sh(f'samtools view -h {BAM} | head -200 | samtools view -b -o {W}/hdr.bam - ; echo rc=$?; samtools view -c {W}/hdr.bam')
check('piping without -h into a BAM writer fails (no header); with -h it works and keeps records', 'rc=0' not in o and 'rc=0' in o2 and o2.split()[-1].isdigit() and int(o2.split()[-1]) > 100, f'no -h: {(o + e).strip()[:100]!r}; with -h: {o2.split()}')
# count claims
n_all = int(sh(f'samtools view -c {BAM}')[1]); n_prim = int(sh(f'samtools view -c -F 2304 {BAM}')[1])
fs = sh(f'samtools flagstat {BAM}')[1]
prim = int(re.search(r'(\d+) \+ \d+ primary\n', fs).group(1))
check('`view -c` 5644 records incl. secondary; `view -c -F 2304` 5642 == flagstat "primary" (Skill: "primary alignments only")', (n_all, n_prim) == (5644, 5642) and prim == 5642, (n_all, n_prim, prim))
n_t = int(sh(f'samtools view -c -@ 2 {BAM}')[1])
check('-@ 2 accepted and count unchanged', n_t == 5644, n_t)
# whole chromosome == idxstats mapped
idx = sh(f'samtools idxstats {BAM}')[1].splitlines()[0].split('\t')
n_chr = int(sh(f'samtools view -c {BAM} chr22')[1])
check('`samtools view input.bam chr22` (whole contig) count == idxstats mapped+unmapped-placed of that contig', n_chr == int(idx[2]) + int(idx[3]), (n_chr, idx))
# NM filter claim
rc, o, e = sh(f"samtools view -c -e '[NM]<=2' {BAM}")
truth = sum(1 for r in pysam.AlignmentFile(BAM) if r.has_tag('NM') and r.get_tag('NM') <= 2)
check("Skill tag row: `samtools view -e '[NM]<=2'` filters by edit distance (count equals a pysam scan)", int(o) == truth and truth > 0, (o.strip(), truth))
# pysam modes x formats
sh(f'samtools view -h -o {W}/t.sam {BAM}; cp {BAM} {W}/t.bam; cp {BAM}.bai {W}/t.bam.bai')
sh(f'samtools view -C -T {REF} -o {W}/t.cram {BAM}; samtools index {W}/t.cram')
res = {}
for fmt in ('sam', 'bam', 'cram'):
    for mode in ('r', 'rb', 'rc'):
        try:
            with pysam.AlignmentFile(f'{W}/t.{fmt}', mode, reference_filename=REF if fmt == 'cram' else None) as a:
                n = sum(1 for _ in a)
                res[(fmt, mode)] = (n, a.is_bam, a.is_cram)
        except Exception as ex:
            res[(fmt, mode)] = f'{type(ex).__name__}: {str(ex)[:50]}'
note('pysam read modes x formats', {f'{k[0]}/{k[1]}': v for k, v in res.items()})
check("Skill: reading detects SAM/BAM/CRAM, so 'r', 'rb' and 'rc' each read any of them (9 combinations, 5644 records each; is_bam/is_cram tell which)",
      all(v[0] == 5644 for v in res.values() if isinstance(v, tuple)) and len([v for v in res.values() if isinstance(v, tuple)]) == 9 and res[('cram', 'r')][2] and res[('bam', 'rc')][1] and not res[('sam', 'rb')][1] and not res[('sam', 'rb')][2], res)
# bam.mapped / unmapped limits
lim = {}
for fmt in ('sam', 'bam', 'cram'):
    try:
        with pysam.AlignmentFile(f'{W}/t.{fmt}', reference_filename=REF if fmt == 'cram' else None) as a:
            lim[fmt] = (a.mapped, a.unmapped)
    except Exception as ex:
        lim[fmt] = f'{type(ex).__name__}: {str(ex)[:60]}'
sh(f'cp {BAM} {W}/noidx.bam')
try:
    with pysam.AlignmentFile(f'{W}/noidx.bam') as a:
        lim['bam_noidx'] = (a.mapped, a.unmapped)
except Exception as ex:
    lim['bam_noidx'] = f'{type(ex).__name__}: {str(ex)[:60]}'
note('bam.mapped/bam.unmapped by format', lim)
check("Skill: `bam.mapped`/`bam.unmapped` come from the index: correct (5642, 2) for indexed BAM; unavailable ('0 or an error') for SAM, unindexed BAM and CRAM",
      lim['bam'] == (5642, 2) and all(not (isinstance(lim[k], tuple) and lim[k] == (5642, 2)) for k in ('sam', 'bam_noidx', 'cram')), lim)
with pysam.AlignmentFile(f'{W}/noidx.bam') as a:
    n = a.count(until_eof=True)
check("Skill quick-reference: `bam.count(until_eof=True)` counts an unindexed BAM (5644)", n == 5644, n)
# 'wc' needs reference_filename
try:
    with pysam.AlignmentFile(BAM) as i:
        with pysam.AlignmentFile(f'{W}/w.cram', 'wc', header=i.header) as o_:
            for r in i:
                o_.write(r)
    sz = os.path.getsize(f'{W}/w.cram')
    note("pysam 'wc' WITHOUT reference_filename", f'no exception; wrote {sz} bytes')
except Exception as ex:
    note("pysam 'wc' WITHOUT reference_filename", f'{type(ex).__name__}: {str(ex)[:100]}')
# tag-order line
rc, o1, e = sh(f'samtools view {BAM} | head -1 | cut -f12-')
rc, o2, e = sh(f'samtools view -T {REF} {W}/t.cram | head -1 | cut -f12-', env=ENV)
check('Skill: CRAM moves NM/MD to the end: same tag set, different order on the real BAM->CRAM (record 1)', o1.split('\t') != o2.split('\t') and sorted(o1.split('\t')) == sorted(o2.split('\t')), (o1.strip(), o2.strip()))
# @PG example vs real chain (informational: Skill labels it "A clean germline pipeline")
rc, o, e = sh(f'samtools view -H {BAM} | grep "^@PG" | cut -f2-4 | head -3')
note('real @PG lines of the test BAM (IDs are what the tools wrote)', o.strip().replace('\n', ' | '))
