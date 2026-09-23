"""Input 8 (NEW): CRAM reference states. Every state of the reference (given, reachable via UR, gone, cached via
REF_PATH / REF_CACHE, cache built by the Skill's own recipe, wrong, missing contig, embedded) against the Skill's
CRAM section, on a SECOND real dataset (nf-core SARS-CoV-2 PE BAM, contig MT192765.1) and on aligner output
(minimap2 --eqx) produced in Input 5.

Prompt: 'My CRAMs will be read on nodes with no internet. Show me, for each way the reference can be present or absent,
whether samtools decodes the file, and whether the check the Skill recommends actually tells me.'
Truth for "decoded correctly" = md5 of columns 1-11 of `samtools view` on the source BAM vs the decode of the CRAM.
"""
import hashlib, os, re, sys
os.environ['AUDIT_INPUT'] = '8'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regress'))
from chk import check, note, sh
import pysam

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S2 = os.environ['AFDATA'] + '/sarscov2'
W = RUN + '/data/in8'
sh(f'rm -rf {W}; mkdir -p {W}/home {W}/d1 {W}/d2')
skill = open(RUN + '/skill/references/cram-reference.md', encoding='utf-8').read()
U = f'env -u REF_PATH -u REF_CACHE -u XDG_CACHE_HOME HOME={W}/home '     # no reference environment; HOME empty so no ~/.cache/hts-ref


def cols(cmd, n=11):
    rc, o, e = sh(cmd)
    txt = ''.join('\t'.join(l.split('\t')[:n]) + '\n' for l in o.splitlines())
    return hashlib.md5(txt.encode()).hexdigest(), o.count('\n'), rc, e


sh(f'cp {S2}/test.paired_end.sorted.bam {W}/src.bam; cp {S2}/genome.fasta {W}/d1/ref.fa; cp {S2}/genome.fasta.fai {W}/d1/ref.fa.fai')
base, n0, _, _ = cols(f'samtools view {W}/src.bam')
check('source BAM: 200 records on MT192765.1', n0 == 200, n0)
sh(f'{U} samtools view -C -T {W}/d1/ref.fa -o {W}/s.cram {W}/src.bam; {U} samtools index {W}/s.cram')
hdr = sh(f'{U} samtools view --no-PG -H {W}/s.cram')[1]
sq = [l for l in hdr.splitlines() if l.startswith('@SQ')][0]
m5 = re.search(r'M5:([0-9a-f]{32})', sq).group(1)
check('CRAM header @SQ carries M5 and UR (points at d1/ref.fa)', 'UR:' in sq and 'd1/ref.fa' in sq, sq)


def state(label, env='', extra='', expect_ok=True, cram='s.cram', want_err=None):
    """full decode with the Skill's own check form, plus a content check of the decode"""
    rc, o, e = sh(f'{U} {env} samtools view -o /dev/null {extra} {W}/{cram} && echo ok; echo rc=$?')
    verdict = ('ok' in o.split()) and 'rc=0' in o
    h, n, rc2, e2 = cols(f'{U} {env} samtools view {extra} {W}/{cram}')
    good = (h == base and n == 200) if expect_ok else (rc2 != 0)
    check(f'{label}: Skill check `view -o /dev/null f.cram && echo ok` prints ok={verdict} (expected {expect_ok}); independent decode {"identical to source" if expect_ok else "fails"} (rc {rc2}, {n} rows)',
          verdict == expect_ok and good and (want_err is None or want_err in (e + e2)), f'{o.strip()[:40]!r} {e.strip()[:120]}')
    return verdict


# A. -T given, B. UR reachable
state('A: -T d1/ref.fa', extra=f'-T {W}/d1/ref.fa')
state('B: no -T, no env, UR path reachable (fallback 4)')
# C. reference gone
sh(f'mv {W}/d1 {W}/d1.gone')
state('C: reference gone (UR dead, no env)', expect_ok=False, want_err='Unable to fetch reference')
rc, o, e = sh(f'{U} samtools view -c {W}/s.cram; {U} samtools flagstat {W}/s.cram | head -1; {U} samtools idxstats {W}/s.cram | head -1; {U} samtools quickcheck -v {W}/s.cram; echo qc=$?')
check('C: with the reference gone, `view -c` (200), flagstat (200 + 0), idxstats (MT192765.1 29829 197 3: 197 mapped + 3 placed-unmapped) all succeed and quickcheck rc 0: none of them can prove reachability (Skill claim)', o.split()[0] == '200' and '200 + 0 in total' in o and 'MT192765.1\t29829\t197\t3' in o and o.strip().endswith('qc=0'), o.strip().replace('\n', ' | ')[:200])
rc, o, e = sh(f'{U} samtools stats {W}/s.cram > /dev/null; echo rc=$?')
check('C: `samtools stats` (decodes bases) fails non-zero with the reference gone (Skill: "or stats")', 'rc=0' not in o, o.strip() + e.strip()[:80])
rc, o, e = sh(f'{U} samtools depth {W}/s.cram | wc -l; echo rc=${{PIPESTATUS[0]}}')
note('C: samtools depth on the unreachable CRAM', o.strip().replace('\n', ' '))
# D. REF_PATH populated with an MD5-named file
seq0 = ''.join(l.strip() for l in open(W + '/d1.gone/ref.fa') if not l.startswith('>')).upper()
sh(f'mkdir -p {W}/rp')
open(f'{W}/rp/{m5}', 'w', newline='').write(seq0)   # MD5-named cache files hold the bare upper-case sequence (what seq_cache_populate.pl writes)
state('D: REF_PATH=<dir>/%s holding a file named by the M5', env=f'REF_PATH={W}/rp/%s')
rc, o, e = sh(f'{U} REF_PATH={W}/rp samtools view -o /dev/null {W}/s.cram && echo ok; echo rc=$?')
note('D2: REF_PATH=<dir> without %s (informational)', (o + e).strip().replace(chr(10), ' | ')[:200])
# G. REF_PATH dir holding the FASTA under its ordinary name (not md5-named)
sh(f'mkdir -p {W}/rn; cp {W}/d1.gone/ref.fa {W}/rn/ref.fa')
state('G: REF_PATH pointing at a dir with the FASTA under its normal name (Skill: elements are matched by the @SQ M5 name)', env=f'REF_PATH={W}/rn', expect_ok=False)
# E. REF_CACHE via seq_cache_populate.pl
rc, o, e = sh(f'{U} seq_cache_populate.pl -root {W}/cache {W}/d1.gone/ref.fa 2>&1 | tail -2; find {W}/cache -type f | sed "s#{W}/##"')
check('seq_cache_populate.pl writes cache/<M5[0:2]>/<M5[2:4]>/<M5[4:]>', f'cache/{m5[:2]}/{m5[2:4]}/{m5[4:]}' in o, o.strip()[-120:])
state('E: REF_CACHE=<root>/%2s/%2s/%s', env=f'REF_CACHE={W}/cache/%2s/%2s/%s')
# F. the Skill's own recipe, verbatim, with reference.fa substituted and HOME redirected
blk = skill.split('On HPC nodes without internet, populate a local cache once:')[1].split('```bash')[1].split('```')[0]
recipe = blk.replace('reference.fa', f'{W}/d1.gone/ref.fa').replace('file.cram', f'{W}/s.cram')
open(W + '/recipe.sh', 'w', newline='\n').write(f'export HOME={W}/home\nunset XDG_CACHE_HOME\n' + recipe)
rc, o, e = sh(f'bash {W}/recipe.sh; echo rc=$?')
lines_ok = o.strip().splitlines()
check('F: the Skill\'s HPC recipe run verbatim (mkdir, seq_cache_populate.pl, exports, quickcheck, full-decode check): quickcheck silent, then prints "ok", rc 0', 'ok' in o.split() and o.strip().endswith('rc=0'), o.strip().replace('\n', ' | ')[:200] + ' ' + e.strip()[:100])
check('F: the recipe created the cache under $HOME/cram_cache', sh(f'find {W}/home/cram_cache -type f | wc -l')[1].strip() == '1', sh(f'find {W}/home/cram_cache -type f')[1].strip()[-80:])
# H. wrong reference (1 base different): MD5 mismatch
seq = ''.join(l.strip() for l in open(W + '/d1.gone/ref.fa') if not l.startswith('>')).upper()
hdrline = open(W + '/d1.gone/ref.fa').readline().strip()
pos = int(sh(f'samtools view {W}/src.bam | head -1 | cut -f4')[1]) + 10     # 0-based index inside the first read
alt = seq[:pos] + ('A' if seq[pos] != 'A' else 'C') + seq[pos + 1:]
os.makedirs(W + '/d2', exist_ok=True)
open(W + '/d2/alt.fa', 'w').write(hdrline + '\n' + '\n'.join(alt[i:i + 60] for i in range(0, len(alt), 60)) + '\n')
sh(f'samtools faidx {W}/d2/alt.fa')
state('H: -T points at a 1-base-different reference: refused, MD5 mismatch', extra=f'-T {W}/d2/alt.fa', expect_ok=False, want_err='MD5')
# I. -T reference lacking the contig
open(W + '/d2/other.fa', 'w').write('>other\nACGTACGTACGTACGT\n')
sh(f'samtools faidx {W}/d2/other.fa')
state('I: -T points at a FASTA that lacks MT192765.1: fails', extra=f'-T {W}/d2/other.fa', expect_ok=False)
# H2. ignore_md5 silences the check
h, n, rc, e = cols(f'{U} samtools view -T {W}/d2/alt.fa --input-fmt-option ignore_md5=1 {W}/s.cram', 10)
b10, _, _, _ = cols(f'samtools view {W}/src.bam', 10)
check('H2: with ignore_md5=1 the wrong reference decodes (rc 0, 200 rows) but the SEQ column differs from the source: silent corruption only when the check is disabled (Skill)', rc == 0 and n == 200 and h != b10, f'rc={rc} n={n} seq-identical={h == b10}')
# J. embedded reference
sh(f'{U} samtools view -C -T {W}/d1.gone/ref.fa --output-fmt-option embed_ref=1 -o {W}/emb.cram {W}/src.bam')
state('J: embed_ref=1 CRAM with no reference reachable anywhere', cram='emb.cram')
# K. -C without -T, nothing resolvable
rc, o, e = sh(f'{U} samtools view -C -o {W}/noT.cram {W}/src.bam; echo rc=$?; ls -l {W}/noT.cram | wc -l')
check('K: `samtools view -C` with no -T and no reachable reference exits 0, warns "Enabling embed_ref=2", writes a CRAM (Skill text)', 'rc=0' in o and 'embed_ref=2' in e, (o + e).strip()[:200])
state('K2: that noT.cram decodes with no reference at all', cram='noT.cram')
# L. pysam
try:
    with pysam.AlignmentFile(W + '/s.cram', 'rc') as cr:
        n = sum(1 for _ in cr)
    check('pysam iterating a CRAM whose reference is gone raises (does not return partial data silently)', False, f'{n} reads returned')
except (OSError, ValueError) as ex:
    check('pysam iterating a CRAM whose reference is gone raises OSError/ValueError (does not return partial data silently)', True, f'{type(ex).__name__}: {str(ex)[:80]}')
with pysam.AlignmentFile(W + '/s.cram', 'rc', reference_filename=W + '/d1.gone/ref.fa') as cr:
    n = sum(1 for _ in cr)
check("pysam 'rc' + reference_filename decodes all 200 reads with the UR path dead", n == 200, n)

# M. =/X and MD/NM through CRAM on REAL aligner output (minimap2 --eqx from Input 5)
A = RUN + '/data/aln'
if os.path.exists(A + '/mm2eqx.bam'):
    sh(f'cp {A}/mm2eqx.bam {W}/eqx.bam; cp {A}/mm2.bam {W}/mm2.bam; cp {A}/g.fa {W}/g.fa; samtools faidx {W}/g.fa')
    for nm in ('eqx', 'mm2'):
        sh(f'{U} samtools view -C -T {W}/g.fa -o {W}/{nm}.cram {W}/{nm}.bam')
        a = sh(f'samtools view {W}/{nm}.bam | cut -f6 | grep -c "[=X]"')[1].strip()
        b = sh(f'{U} samtools view -T {W}/g.fa {W}/{nm}.cram | cut -f6 | grep -c "[=X]"')[1].strip()
        n_md_a = sh(f'samtools view {W}/{nm}.bam | grep -c "MD:Z:"')[1].strip()
        n_md_b = sh(f'{U} samtools view -T {W}/g.fa {W}/{nm}.cram | grep -c "MD:Z:"')[1].strip()
        note(f'minimap2 {nm}: reads with =/X ops before -> after CRAM round trip; reads with MD:Z before -> after', (a, b, n_md_a, n_md_b))
        if nm == 'eqx':
            eqx_before, eqx_after = int(a), int(b)
        else:
            md_before, md_after = int(n_md_a), int(n_md_b)
    check('REAL minimap2 --eqx BAM: =/X CIGAR ops are rewritten to M by the CRAM round trip (before >0, after 0): Skill text says a round trip keeps every field', eqx_before > 0 and eqx_after == 0, (eqx_before, eqx_after))
    check('REAL minimap2 BAM (NM, no MD): the CRAM round trip ADDS MD:Z to every mapped read (0 -> >0)', md_before == 0 and md_after > 0, (md_before, md_after))
else:
    note('minimap2 eqx BAM absent (run regress/in5.sh first)', '')
# N. cleanup of bulky intermediates is done by the runner
sh(f'rm -rf {RUN}/skill/examples/__pycache__')
