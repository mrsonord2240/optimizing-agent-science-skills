"""Input 4 follow-up (run after in4.py, reuses data/cram): (a) does a mismatched reference ever corrupt silently?
(b) shipped view_bam.py statistics on CRAM vs the truth."""
import hashlib, os, sys
os.environ['AUDIT_INPUT'] = '4'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chk import check, note, sh
import pysam

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = RUN + '/data/cram'
D = os.environ['AFDATA'] + '/human'
BAM = D + '/test.paired_end.sorted.bam'
U = 'env -u REF_PATH -u REF_CACHE '


def canon(cmd):
    rc, o, e = sh(cmd)
    lines = [l.split('\t') for l in o.rstrip('\n').split('\n')] if o.strip() else []
    txt = ''.join('\t'.join(f[:11] + sorted(f[11:])) + '\n' for f in lines)
    return hashlib.md5(txt.encode()).hexdigest(), len(lines), rc, e


base, n0, _, _ = canon(f'samtools view {BAM}')
# (a) wrong reference + M5 check disabled, with the UR target unreachable so nothing can rescue the decode
os.rename(W + '/ref.fa', W + '/ref.away')
h, n, rc, e = canon(f'{U} samtools view -T {W}/alt.fa --input-fmt-option ignore_md5=1 {W}/b.cram')
n_diff = 0
rc2, o, e2 = sh(f'{U} samtools view -T {W}/alt.fa --input-fmt-option ignore_md5=1 {W}/b.cram')
_, o0, _ = sh(f'samtools view {BAM}')
for a, b in zip(o0.splitlines(), o.splitlines()):
    if a.split('\t')[9] != b.split('\t')[9]:
        n_diff += 1
note('ignore_md5=1 + -T alt.fa (1 base differs), UR unreachable', f'rc={rc} n={n} reads with different SEQ={n_diff}')
check('silent base corruption exists ONLY if the M5 check is disabled by the user (ignore_md5=1): bases differ in reads spanning the changed base',
      rc == 0 and n_diff > 0, f'{n_diff} reads decoded with a wrong base, rc={rc}')
os.rename(W + '/ref.away', W + '/ref.fa')

# (b) view_bam.py header statistics on a CRAM vs truth
with pysam.AlignmentFile(W + '/b.cram', 'rc', reference_filename=W + '/ref.fa') as cr:
    try:
        m, u = cr.mapped, cr.unmapped
    except Exception as ex:
        m = u = f'{type(ex).__name__}: {ex}'
rc, o, e = sh(f'{U} samtools idxstats {W}/b.cram')
note('pysam .mapped/.unmapped on CRAM vs samtools idxstats on CRAM', f'pysam=({m},{u}) idxstats={o.strip().replace(chr(10), " | ")} {e.strip()[:80]}')
rc, o2, e2 = sh(f'{U} python {RUN}/skill/examples/view_bam.py {W}/b.cram 1 | head -3')
check('view_bam.py on an indexed CRAM now prints the true 5642 mapped / 2 unmapped (scan, not the 0/0 index stats)', 'Mapped: 5642' in o2 and 'Unmapped: 2' in o2, o2.replace('
', ' | '))
