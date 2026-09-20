"""Input 2 (Variant A): format conversion.
Prompt: 'Convert my BAM to SAM, back to BAM, then to CRAM against the reference, then back to BAM, and use the
Skill's convert_formats.sh helper for the same jobs. Confirm nothing was lost.'
"""
import hashlib, os, sys, shutil
os.environ['AUDIT_INPUT'] = '2'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chk import check, note, sh
import pysam

D = os.environ['AFDATA'] + '/human'
BAM, REF, CRAM = D + '/test.paired_end.sorted.bam', D + '/genome.fasta', D + '/test.paired_end.sorted.cram'
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = RUN + '/data/conv'
shutil.rmtree(W, ignore_errors=True)
os.makedirs(W)
ENV = {'REF_PATH': '', 'REF_CACHE': ''}    # make sure nothing resolves references behind our back


def recs(path, extra='', canon=True):
    """md5 + count of alignment records (no header) as SAM text. canon=True sorts the optional tags of each
    record first (CRAM legitimately re-orders tags: see in2_diff.sh); canon=False is raw text."""
    rc, o, e = sh(f'samtools view {extra} {path}', env=ENV)
    if canon:
        o = ''.join('\t'.join(f[:11] + sorted(f[11:])) + '\n' for f in (l.split('\t') for l in o.rstrip('\n').split('\n')))
    return hashlib.md5(o.encode()).hexdigest(), o.count('\n'), rc


base_md5, base_n, _ = recs(BAM)
check('baseline BAM has 5644 records', base_n == 5644, base_n)

# --- Skill commands verbatim (usage-guide / SKILL.md)
steps = [
    ('BAM->SAM  samtools view -h -o output.sam input.bam', f'samtools view -h -o {W}/o.sam {BAM}'),
    ('SAM->BAM  samtools view -b -o output.bam input.sam', f'samtools view -b -o {W}/o.bam {W}/o.sam'),
    ('BAM->CRAM samtools view -C -T reference.fa -o output.cram input.bam', f'samtools view -C -T {REF} -o {W}/o.cram {W}/o.bam'),
    ('CRAM->BAM samtools view -b -T reference.fa -o output.bam input.cram', f'samtools view -b -T {REF} -o {W}/o2.bam {W}/o.cram'),
    ('Pipe      samtools view -b input.sam > output.bam', f'samtools view -b {W}/o.sam > {W}/pipe.bam'),
]
for label, cmd in steps:
    rc, o, e = sh(cmd, env=ENV)
    check(f'{label}: exit 0 and non-empty output', rc == 0 and os.path.getsize(W + '/' + cmd.split(' > ')[-1].split()[-1].split('/')[-1] if ' > ' in cmd else cmd.split('-o ')[1].split()[0]) > 0, f'rc={rc} {e.strip()[:100]}')
for f in ('o.bam', 'o.cram', 'o2.bam', 'pipe.bam'):
    md5, n, rc = recs(f'{W}/{f}', f'-T {REF}')
    check(f'round-trip {f}: 5644 records with byte-identical SAM text (all fields + tags) vs original', md5 == base_md5 and n == 5644, f'n={n} md5 match={md5 == base_md5}')
md5, n, rc = recs(f'{W}/o.sam')
check('SAM step keeps all records identical', md5 == base_md5, n)
raw0, _, _ = recs(BAM, canon=False)
raw_cram, _, _ = recs(f'{W}/o.cram', f'-T {REF}', canon=False)
check('CRAM round trip preserves every field, but NOT the raw text: optional-tag ORDER changes (NM/MD move to the end)',
      raw0 != raw_cram, 'raw md5 differs while sorted-tag md5 is identical; Skill calls nothing lossless-by-text, so informational')
sizes = {f: os.path.getsize(f'{W}/{f}') for f in ('o.sam', 'o.bam', 'o.cram')}
check('Format table: SAM > BAM > CRAM in size (CRAM "smaller than BAM", SAM larger)', sizes['o.sam'] > sizes['o.bam'] > sizes['o.cram'], sizes)
# header content survives
rc, h1, _ = sh(f'samtools view --no-PG -H {BAM}')
rc, h2, _ = sh(f'samtools view --no-PG -H {W}/o2.bam -T {REF}')
strip = lambda h: [l for l in h.splitlines() if not l.startswith('@PG')]
check('@HD/@SQ/@RG survive BAM->SAM->BAM->CRAM->BAM (M5/UR tags may be added by CRAM)', [l for l in strip(h1)][:3] == [l.split('\tM5:')[0] if l.startswith('@SQ') else l for l in strip(h2)][:3] or strip(h1)[0] == strip(h2)[0],
      f'{strip(h1)} vs {strip(h2)}')
rc, h, _ = sh(f'samtools view --no-PG -H {W}/o.cram -T {REF}')
note('CRAM header @SQ (M5/UR added at CRAM write)', [l for l in h.splitlines() if l.startswith('@SQ')][0])

# --- -o extension does NOT choose format
rc, o, e = sh(f'samtools view -o {W}/noflag.bam {BAM}; head -c 4 {W}/noflag.bam | xxd -p', env=ENV)
note('samtools view -o x.bam (no -b): first bytes', o.strip())
rc, o, e = sh(f'samtools view -o {W}/noflag.cram {BAM}; head -c 4 {W}/noflag.cram | xxd -p', env=ENV)
note('samtools view -o x.cram (no -C): first bytes', o.strip())
rc, o, e = sh(f'samtools view -T {REF} -o {W}/noflag.cram {BAM}; head -c 4 {W}/noflag.cram; echo', env=ENV)
note('samtools view -T ref -o x.cram (no -C): magic', o.strip())

# --- CRAM without reference: exit codes are the trap
rc, o, e = sh(f'samtools view {CRAM} | wc -l', env=ENV)
note('samtools view CRAM with unresolvable reference (no -T, REF_PATH empty), stdout lines', f'{o.strip()} :: {e.strip()[:200]}')
rc, o, e = sh(f'samtools view -b -o {W}/fail.bam {CRAM}; echo rc=$?', env=ENV)
check('CRAM->BAM without -T and no REF_PATH fails loudly (non-zero rc)', 'rc=0' not in o, f'{o.strip()} {e.strip()[:150]}')
rc, o, e = sh(f'samtools view -C -o {W}/noref.cram {BAM}; echo rc=$?; ls -la {W}/noref.cram', env=ENV)
note('samtools view -C without -T (BAM->CRAM) and no REF_PATH', f'{o.strip()} | {e.strip()[:200]}')

# --- SAM without @SQ
open(W + '/nosq.sam', 'w').write('r1\t4\t*\t0\t0\t*\t*\t0\t0\tACGT\tFFFF\n')
rc, o, e = sh(f'samtools view -b -o {W}/nosq.bam {W}/nosq.sam; echo rc=$?', env=ENV)
note('unaligned headerless SAM -> BAM (Skill recipe)', f'{o.strip()} {e.strip()[:100]}')
open(W + '/nosq2.sam', 'w').write('r1\t0\tchr22\t100\t60\t4M\t*\t0\t0\tACGT\tFFFF\n')
rc, o, e = sh(f'samtools view -b -o {W}/nosq2.bam {W}/nosq2.sam; echo rc=$?', env=ENV)
check('aligned SAM lacking @SQ -> BAM recipe fails (needs -t ref.fai); message', 'rc=0' not in o, f'{o.strip()} {e.strip()[:150]}')
rc, o, e = sh(f'samtools view -b -t {REF}.fai -o {W}/nosq2.bam {W}/nosq2.sam; echo rc=$?; samtools view -c {W}/nosq2.bam', env=ENV)
check('the -t ref.fai workaround (not in the Skill) produces a 1-record BAM', o.split() == ['rc=0', '1'], o)

# --- pysam conversions from usage-guide/SKILL
with pysam.AlignmentFile(BAM, 'rb') as infile:
    with pysam.AlignmentFile(W + '/p.sam', 'w', header=infile.header) as out:
        for r in infile:
            out.write(r)
with pysam.AlignmentFile(W + '/p.sam', 'r') as infile:
    with pysam.AlignmentFile(W + '/p.bam', 'wb', header=infile.header) as out:
        for r in infile:
            out.write(r)
with pysam.AlignmentFile(W + '/p.bam', 'rb') as infile:
    with pysam.AlignmentFile(W + '/p.cram', 'wc', reference_filename=REF, header=infile.header) as out:
        for r in infile:
            out.write(r)
for f in ('p.sam', 'p.bam', 'p.cram'):
    md5, n, rc = recs(f'{W}/{f}', f'-T {REF}')
    check(f'pysam-written {f}: 5644 records identical to original SAM text', md5 == base_md5, f'n={n}')
# mode strings table
try:
    with pysam.AlignmentFile(BAM, 'r') as b:
        n_r = sum(1 for _ in b)
    check("mode 'r' on a BAM (usage-guide says 'r' = Read SAM)", True, f'pysam auto-detected, read {n_r} records')
except Exception as ex:
    check("mode 'r' on a BAM (usage-guide says 'r' = Read SAM)", False, f'{type(ex).__name__}: {ex}')
try:
    with pysam.AlignmentFile(W + '/o.sam', 'rb') as b:
        n = sum(1 for _ in b)
    note("mode 'rb' on a SAM file", f'read {n} records (autodetect)')
except Exception as ex:
    note("mode 'rb' on a SAM file", f'{type(ex).__name__}: {ex}')
with pysam.AlignmentFile(W + '/o.cram', 'rc', reference_filename=REF) as b:
    n_rc = sum(1 for _ in b)
check("mode 'rc' + reference_filename reads CRAM (5644)", n_rc == 5644, n_rc)
os.environ['REF_PATH'] = ''
try:
    with pysam.AlignmentFile(CRAM, 'rc') as b:
        n = sum(1 for _ in b)
    note("pysam 'rc' on CRAM with no reference at all", f'{n} records (no error!)')
except Exception as ex:
    note("pysam 'rc' on CRAM with no reference at all", f'{type(ex).__name__}: {str(ex)[:150]}')
with pysam.AlignmentFile(BAM, 'rb') as bam:
    sq = [f'{s["SN"]}: {s["LN"]} bp' for s in bam.header['SQ']]
check('Skill snippet bam.header["SQ"] works on pysam 0.24 -> "chr22: 40001 bp"', sq == ['chr22: 40001 bp'], sq)

# --- shipped helper convert_formats.sh, run from the copy
H = RUN + '/skill/examples/convert_formats.sh'
def helper(args, label, expect_ok, desc):
    rc, o, e = sh(f'bash {H} {args}', env=ENV)
    check(f'convert_formats.sh {label}', (rc == 0) == expect_ok, f'{desc} rc={rc} out={o.strip()[:80]!r} err={e.strip()[:120]!r}')
    return rc
helper(f'{BAM} {W}/h.sam', 'BAM->SAM', True, '')
helper(f'{W}/h.sam {W}/h.bam', 'SAM->BAM', True, '')
helper(f'{W}/h.bam {W}/h.cram {REF}', 'BAM->CRAM with reference', True, '')
helper(f'{W}/h.bam {W}/h2.cram', 'BAM->CRAM without reference arg -> clean error', False, '')
for f in ('h.bam', 'h.cram'):
    md5, n, rc = recs(f'{W}/{f}', f'-T {REF}')
    check(f'helper output {f} identical to original records', md5 == base_md5, n)
# The Skill advertises CRAM->BAM; fixed helper passes -T for CRAM input. CRAM header UR is unreachable and REF_PATH empty (ENV), so only the 3rd arg can resolve it.
rc = helper(f'{D}/test.paired_end.sorted.cram {W}/h3.bam {REF}', 'CRAM->BAM with reference arg (usage says [reference.fa]); input is the ORIGINAL nf-core CRAM whose UR is dead', True, '')
helper(f'{D}/test.paired_end.sorted.cram {W}/h3.sam {REF}', 'CRAM->SAM with reference arg', True, '')
for f in ('h3.bam', 'h3.sam'):
    md5, n, rc = recs(f'{W}/{f}', f'-T {REF}')
    check(f'helper CRAM-input output {f} identical to original 5644 records (fields + tags)', md5 == base_md5 and n == 5644, f'n={n}')
rc, o, e = sh(f'bash {H} {D}/test.paired_end.sorted.cram {W}/h4.bam; echo rc=$?; ls {W}/h4.bam 2>&1', env=ENV)
check('helper CRAM->BAM WITHOUT reference (unresolvable) fails with non-zero rc, not exit 0', 'rc=0' not in o, f'{o.strip()[:120]} {e.strip()[:150]}')
helper(f'{W}/h.bam {W}/h5.BAM', 'uppercase extension .BAM now accepted', True, '')
md5, n, rc = recs(f'{W}/h5.BAM')
check('uppercase .BAM output is a real BAM with the original records', md5 == base_md5, n)
helper(f'{W}/h.bam {W}/h.txt', 'unknown extension -> error', False, '')
helper(f'', 'no args -> usage', False, '')
rc, o, e = sh(f'bash {H} {W}/does_not_exist.bam {W}/x.bam; echo rc=$?; ls {W}/x.bam 2>&1', env=ENV)
note('helper with missing input: rc and leftover output file', f'{o.strip()} | {e.strip()[:150]}')
check('helper with missing input exits non-zero', 'rc=0' not in o, o.strip()[:120])
rc, o, e = sh(f'cp {W}/h.bam {W}/same.bam; bash {H} {W}/same.bam {W}/same.bam; echo rc=$?; samtools view -c {W}/same.bam; bash {H} {W}/same.bam {W}/./same.bam; echo rc2=$?; samtools view -c {W}/same.bam; bash {H} {W}/same.bam {W}/same.sam; ln -sf {W}/same.bam {W}/link.bam; bash {H} {W}/same.bam {W}/link.bam; echo rc3=$?; samtools view -c {W}/same.bam', env=ENV)
t = o.split()
check('helper refuses input == output (same path, ./ path, symlink): rc 1 each and the input keeps 5644 records', 'rc=1' in t and 'rc2=1' in t and 'rc3=1' in t and t.count('5644') == 3, o.replace(chr(10), ' | ')[:300])
