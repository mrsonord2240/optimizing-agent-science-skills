"""Input 4 (Variant B): CRAM reference resolution, options and integrity claims in SKILL.md.
Prompt: 'Our HPC nodes have no internet. I need to archive these BAMs as CRAM and read them back. How does samtools find
the reference, how do I cache it, how do I prove a CRAM is readable, and is `archive` lossy?'
NOTE (found during the audit): `samtools view -c` on a CRAM does NOT decode bases, so every reachability test below uses a
full decode (`samtools view f > file`) and asserts on rc AND on the record count of that decode.
"""
import hashlib, os, shutil, sys
os.environ['AUDIT_INPUT'] = '4'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chk import check, note, sh
import pysam

D = os.environ['AFDATA'] + '/human'
BAM, REF = D + '/test.paired_end.sorted.bam', D + '/genome.fasta'
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = RUN + '/data/cram'
shutil.rmtree(W, ignore_errors=True)
os.makedirs(W)
U = 'env -u REF_PATH -u REF_CACHE '          # run with no reference environment at all


def canon(cmd):
    rc, o, e = sh(cmd)
    lines = [l.split('\t') for l in o.rstrip('\n').split('\n')] if o.strip() else []
    txt = ''.join('\t'.join(f[:11] + sorted(f[11:])) + '\n' for f in lines)
    return hashlib.md5(txt.encode()).hexdigest(), len(lines), rc, e


def full(prefix, f, extra=''):
    """full decode of every record; returns (rc, n_records, stderr)"""
    rc, o, e = sh(f'{prefix} samtools view {extra} {f} > {W}/full.out; echo rc=${{PIPESTATUS[0]}}; wc -l < {W}/full.out')
    a = o.split()
    return int(a[0][3:]), int(a[1]), e.strip()


base, n0, _, _ = canon(f'samtools view {BAM}')

# ---- setup: CRAM written against a private copy of the reference
sh(f'cp {REF} {W}/ref.fa; cp {REF}.fai {W}/ref.fa.fai; {U} samtools view -C -T {W}/ref.fa -o {W}/b.cram {BAM}; samtools index {W}/b.cram')
hdr = sh(f'{U} samtools view --no-PG -H {W}/b.cram')[1]
sq = [l for l in hdr.splitlines() if l.startswith('@SQ')][0]
m5 = [t[3:] for t in sq.split('\t') if t.startswith('M5:')][0]
check('@SQ has M5 (md5 of reference) and UR (path of the FASTA) written by samtools', 'UR:' in sq and m5 == '1922b52e1af6977302717072ebaca0a1', sq)
rc, n, e = full(U, W + '/b.cram')
check('with UR reachable: full decode of b.cram = 5644 records, rc 0 (no -T/REF_PATH/REF_CACHE: fallback #4 UR works)', (rc, n) == (0, 5644), (rc, n))

# ---- reference now UNREACHABLE (moved), no cache
os.rename(W + '/ref.fa', W + '/ref.gone')
rc, n, e = full(U, W + '/b.cram')
check('reference unreachable: full decode FAILS loudly (rc != 0, no records)', rc != 0 and n == 0, (rc, n, e[:100]))
rc, o, e = sh(f'{U} samtools view -c {W}/b.cram; echo rc=$?')
note('reference unreachable: samtools view -c b.cram', o.strip().replace('\n', ' '))
check('SKILL.md: "`samtools view -c file.cram` forces full decode; proves reference reachable" -> FALSE in 1.24: -c returns the count, rc 0, with NO reference',
      o.split()[0] == '5644' and o.strip().endswith('rc=0'), o.strip().replace('\n', ' '))
rc, o, e = sh(f'{U} samtools view -o /dev/null {W}/b.cram; echo rc=$?')
check('a working reachability proof: `samtools view -o /dev/null file.cram` gives rc != 0 when reference is unreachable', not o.strip().endswith('rc=0'), o.strip() + e.strip()[:80])
rc, o, e = sh(f'{U} samtools view -o /dev/null {W}/b.cram && echo ok; echo rc=$?')
check('Skill recipe verbatim `samtools view -o /dev/null file.cram && echo ok`: prints NO "ok" and stays non-zero when the reference is unreachable', 'ok' not in o.split() and 'rc=0' not in o, o.strip() + ' ' + e.strip()[:100])
rc, o, e = sh(f'{U} samtools flagstat {W}/b.cram | head -1; {U} samtools idxstats {W}/b.cram | head -1; echo rc=$?')
check('Skill: flagstat / idxstats print counts on a CRAM with no reachable reference (never decode bases)', '5644 + 0 in total' in o and 'chr22' in o, o.strip().replace(chr(10), ' | '))
rc, o, e = sh(f'{U} samtools stats {W}/b.cram > /dev/null; echo rc=$?')
check('Skill: `samtools stats` decodes bases, so it fails (non-zero) with the reference unreachable', 'rc=0' not in o, o.strip() + e.strip()[:80])
rc, o, e = sh(f'{U} samtools quickcheck -v {W}/b.cram; echo rc=$?')
check('quickcheck -v passes (rc 0) even though the reference is unreachable ("header + EOF only")', o.strip().endswith('rc=0'), o.strip())

# ---- claim: order -T > REF_CACHE > REF_PATH > UR ; seq_cache_populate.pl recipe
rc, o, e = sh(f'{U} seq_cache_populate.pl -root {W}/cache {W}/ref.gone 2>&1 | tail -4; find {W}/cache -type f')
files = [x for x in o.splitlines() if x.startswith('/') and '/cache/' in x and 'Use' not in x]
check('seq_cache_populate.pl ships with samtools 1.24 and writes files named by M5 in %2s/%2s/%s layout', any(x.endswith('/' + m5[:2] + '/' + m5[2:4] + '/' + m5[4:]) for x in files), files[:2])
CACHE = f'{W}/cache/%2s/%2s/%s'
for label, env in (('Skill recipe REF_CACHE=<root>/%2s/%2s/%s + REF_PATH=$REF_CACHE', f'REF_CACHE={CACHE} REF_PATH={CACHE}'),
                   ('REF_PATH alone', f'REF_PATH={CACHE}'), ('REF_CACHE alone', f'REF_CACHE={CACHE}')):
    rc, n, e = full(f'{U} {env}', W + '/b.cram')
    check(f'{label}: full decode offline = 5644 records rc 0', (rc, n) == (0, 5644), (rc, n, e[:80]))
# poisoned copies: file named by the true M5 but holding a 1-base-different sequence
seq = ''.join(l.strip() for l in open(W + '/ref.gone') if not l.startswith('>')).upper()
bad = list(seq); bad[1971] = 'A' if bad[1971] != 'A' else 'C'; bad = ''.join(bad)
os.makedirs(W + '/poison/' + m5[:2] + '/' + m5[2:4], exist_ok=True)
open(W + '/poison/' + m5[:2] + '/' + m5[2:4] + '/' + m5[4:], 'w').write(bad)
POI = f'{W}/poison/%2s/%2s/%s'
rc1, n1, e1 = full(f'{U} REF_CACHE={POI} REF_PATH={CACHE}', W + '/b.cram')
rc2, n2, e2 = full(f'{U} REF_CACHE={CACHE} REF_PATH={POI}', W + '/b.cram')
note('poisoned REF_CACHE + good REF_PATH', (rc1, n1, e1[:120]))
note('good REF_CACHE + poisoned REF_PATH', (rc2, n2, e2[:120]))
check('REF_CACHE is consulted BEFORE REF_PATH (Skill order #2 before #3): poisoned cache breaks decode; poisoned path + good cache decodes',
      rc1 != 0 and (rc2, n2) == (0, 5644), f'cache-first-poison rc={rc1}; path-poison rc={rc2} n={n2}')
# -T wins over everything: give -T the good FASTA while REF_CACHE is poisoned
os.rename(W + '/ref.gone', W + '/ref.fa')
rc3, n3, e3 = full(f'{U} REF_CACHE={POI} REF_PATH={POI}', W + '/b.cram', f'-T {W}/ref.fa')
check('-T ref.fa (#1) beats a poisoned REF_CACHE/REF_PATH', (rc3, n3) == (0, 5644), (rc3, n3, e3[:100]))
os.rename(W + '/ref.fa', W + '/ref.gone')
# UR is the LAST resort: point UR at a poisoned local FASTA? (UR ok when nothing else) -> covered by earlier test; now check REF_PATH beats UR
sh(f'cp {W}/ref.gone {W}/ref.fa')
open(W + '/ref.fa', 'w').write('>chr22\n' + '\n'.join(bad[i:i + 60] for i in range(0, len(bad), 60)) + '\n')   # UR target now poisoned
rc4, n4, e4 = full(f'{U}', W + '/b.cram')
rc5, n5, e5 = full(f'{U} REF_PATH={CACHE}', W + '/b.cram')
check('UR (#4) is last: with UR target poisoned, decode fails alone but REF_PATH (good) rescues it', rc4 != 0 and (rc5, n5) == (0, 5644), f'UR only rc={rc4}; +REF_PATH rc={rc5} n={n5}')
os.remove(W + '/ref.fa')

# ---- network default removed in >=1.22 : bogus proxy, no reference anywhere
rc, o, e = sh(f'{U} http_proxy=http://127.0.0.1:9 https_proxy=http://127.0.0.1:9 HTS_VERBOSE=9 samtools view -o /dev/null {W}/b.cram 2>&1 | head -12')
note('no reference, bogus proxy, full decode: output', o.strip().replace('\n', ' | ')[:500])
check('no network lookup by default (>=1.22): no ebi/ena/curl/proxy mention when reference unresolvable', not any(t in o.lower() for t in ('ebi.ac.uk', 'proxy', 'curl', 'connect')), o.strip()[:200])
libdir = sh('dirname $(readlink -f $(which samtools))')[1].strip()
rc, o, e = sh(f'strings -a {libdir}/../lib/libhts.so.3* 2>/dev/null | grep -ci "ebi.ac.uk/ena/cram"')
check('libhts 1.24 binary holds no built-in ebi.ac.uk/ena/cram default (independent confirmation of the 1.22 removal claim)', o.strip() == '0', o.strip())
rc, o, e = sh(f'{U} REF_PATH="https://www.ebi.ac.uk/ena/cram/md5/%s" http_proxy=http://127.0.0.1:9 https_proxy=http://127.0.0.1:9 timeout 25 samtools view -o /dev/null {W}/b.cram 2>&1 | head -6; echo "exit=${{PIPESTATUS[0]}} (124 = still retrying the server when killed after 25 s)"')
note('REF_PATH set explicitly to the ENA URL + bogus proxy: the server IS tried', o.strip().replace('\n', ' | ')[:400])

# ---- claim: --output-fmt-option archive is a lossless preset
os.rename(W + '/ref.gone', W + '/ref.fa')
rc, o, e = sh(f'{U} samtools view -o /dev/null {W}/b.cram && echo ok; echo rc=$?')
check('Skill recipe prints "ok" and rc 0 once the reference is reachable again (UR path restored)', o.split() == ['ok', 'rc=0'], o.strip())
rc, o, e = sh(f'{U} samtools view -C --output-fmt-option archive -T {W}/ref.fa -o {W}/arch.cram {BAM}; echo rc=$?')
check('`--output-fmt-option archive` is accepted syntax', o.strip().endswith('rc=0'), o.strip() + e[:120])
h, n, rc, e = canon(f'{U} samtools view -T {W}/ref.fa {W}/arch.cram')
check('archive CRAM is lossless: 5644 records identical after tag canonicalisation (Skill: "does not alter bases or qualities")', (h, n) == (base, n0), f'{n} records, identical={h == base}')
sizes = {}
for prof in ('fast', 'normal', 'small', 'archive'):
    sh(f'{U} samtools view -C --output-fmt-option {prof} -T {W}/ref.fa -o {W}/p_{prof}.cram {BAM}')
    sizes[prof] = os.path.getsize(f'{W}/p_{prof}.cram')
check('archive is the smallest profile ("maximum-compression preset")', sizes['archive'] == min(sizes.values()), sizes)
rc, o, e = sh('samtools view -? 2>&1 | grep -i -E "embed_ref|no_ref|lossy_names|store_md|archive" | head -5')
note('CRAM option names available (embed_ref / no_ref etc. -- Skill mentions none)', o.strip().replace('\n', ' | ')[:300])
rc, o, e = sh(f'{U} samtools view -C --output-fmt-option embed_ref -o {W}/emb.cram -T {W}/ref.fa {BAM}; mv {W}/ref.fa {W}/ref.gone; {U} samtools view -o /dev/null {W}/emb.cram; echo rc=$?; mv {W}/ref.gone {W}/ref.fa')
check('embed_ref (undocumented in Skill) yields a self-contained CRAM: decodes with NO reference reachable', o.strip().endswith('rc=0'), o.strip()[-40:] + e.strip()[:100])

# ---- claim: a different reference "silently corrupts bases on read-back"
alt = list(seq); alt[1971] = 'A' if alt[1971] != 'A' else 'C'; alt = ''.join(alt)   # 0-based 1971 = 1-based 1972: covered (reads sit only in 1952-4617)
open(W + '/alt.fa', 'w').write('>chr22\n' + '\n'.join(alt[i:i + 60] for i in range(0, len(alt), 60)) + '\n')
sh(f'samtools faidx {W}/alt.fa')
h, n, rc, e = canon(f'{U} samtools view -T {W}/alt.fa {W}/b.cram')
check('(i) CRAM (true ref) read with a 1-base-different reference: hard error (rc!=0, MD5 mismatch), not silent corruption', rc != 0 and 'MD5' in e and n == 0, f'rc={rc} n={n} err={e.strip()[:110]!r}')
sh(f'{U} samtools view -C -T {W}/alt.fa -o {W}/c_alt.cram {BAM}')
h, n, rc, e = canon(f'{U} samtools view -T {W}/ref.fa {W}/c_alt.cram')
check('(ii) BAM converted against the WRONG reference, read back with the right one: hard error, not silent', rc != 0 and n == 0, f'rc={rc} n={n} identical={h == base}')
h, n, rc, e = canon(f'{U} samtools view -T {W}/alt.fa {W}/c_alt.cram')
check('(iii) read back with the same wrong reference: faithful (records identical)', h == base, f'identical={h == base}')
# does htslib really check? disable md5 check
rc, o, e = sh(f'{U} samtools view -T {W}/alt.fa --input-fmt-option ignore_md5=1 {W}/b.cram | wc -l; ')
h, n, rc, e = canon(f'{U} samtools view -T {W}/alt.fa --input-fmt-option ignore_md5=1 {W}/b.cram')
note('with --input-fmt-option ignore_md5=1 the mismatch IS silent: records identical to original?', f'rc={rc} n={n} identical={h == base}')
check('silent corruption is possible only when the M5 check is switched off (ignore_md5=1): reads differ from the original', n == n0 and h != base, f'n={n} identical={h == base}')

# ---- truncated / corrupted files vs quickcheck
sz = os.path.getsize(W + '/b.cram')
sh(f'head -c {sz // 2} {W}/b.cram > {W}/trunc.cram')
rc, o, e = sh(f'{U} samtools quickcheck -v {W}/trunc.cram; echo rc=$?')
check('quickcheck detects a truncated CRAM (missing EOF) with non-zero rc', not o.strip().endswith('rc=0'), o.strip()[-30:])
data = bytearray(open(W + '/b.cram', 'rb').read())
for i in range(sz // 2, sz // 2 + 40):
    data[i] ^= 0xFF
open(W + '/corrupt.cram', 'wb').write(data)
rc, o, e = sh(f'{U} samtools quickcheck -v {W}/corrupt.cram; echo qc=$?')
rcf, nf, ef = full(U, W + '/corrupt.cram', f'-T {W}/ref.fa')
rcc, oc, ec = sh(f'{U} samtools view -c -T {W}/ref.fa {W}/corrupt.cram; echo rc=$?')
check('mid-file corruption: quickcheck rc 0 (header+EOF only) but a FULL decode fails', o.strip().endswith('qc=0') and rcf != 0, f'qc rc0; full decode rc={rcf} n={nf}')
check('mid-file corruption is also NOT caught by `samtools view -c` (only a full decode is)', oc.split()[0] == '5644' or not oc.strip().endswith('rc=0') is False, f'view -c => {oc.strip()!r} {ec.strip()[:80]}')

# ---- BAM->CRAM without -T
rc, o, e = sh(f'{U} samtools view -C -o {W}/noT.cram {BAM}; echo rc=$?')
note('BAM->CRAM WITHOUT -T, no reference env (help says "-C requires -T")', f'{o.strip()} err={e.strip()[:260]!r}')
check('SKILL.md "CRAM requires a reference FASTA with -T": samtools 1.24 nonetheless exits 0 and writes a CRAM (with warnings) -> silent non-portable file', o.strip().endswith('rc=0') and os.path.getsize(W + '/noT.cram') > 0, o.strip())
hn = sh(f'{U} samtools view --no-PG -H {W}/noT.cram')[1]
note('noT.cram @SQ (no M5/UR)', [l for l in hn.splitlines() if l.startswith('@SQ')])
rc, n, e = full(U, W + '/noT.cram')
check('that CRAM written without -T is readable with no reference at all (embedded/no_ref)', (rc, n) == (0, 5644), (rc, n, e[:100]))

# ---- pysam + shipped view_bam.py on CRAM (index made above: b.cram.crai)
with pysam.AlignmentFile(W + '/b.cram', 'rc', reference_filename=W + '/ref.fa') as cr:
    n = sum(1 for _ in cr.fetch('chr22', 1999, 3000))
check("pysam 'rc' + reference_filename + .crai: fetch chr22:2000-3000 gives 2732 (same as BAM)", n == 2732, n)
rc, o, e = sh(f'{U} python {RUN}/skill/examples/view_bam.py {W}/b.cram 2 2>&1 | tail -6')
note('view_bam.py on an INDEXED CRAM (mode "rb")', o.strip().replace('\n', ' | ')[:300])
check('view_bam.py works on an indexed CRAM (prints Mapped: 5642)', 'Mapped: 5642' in o, o.strip().replace('\n', ' | ')[:200])

# ---- view_bam.py on a CRAM whose reference is unreachable: friendly error, rc 1 (fixed), and with the 3rd arg it works
os.rename(W + '/ref.fa', W + '/ref.gone')
rc, o, e = sh(f'{U} python {RUN}/skill/examples/view_bam.py {W}/b.cram 2; echo rc=$?')
check('view_bam.py on CRAM with unreachable reference: exit 1 with a readable error naming the reference option, no Traceback', 'rc=1' in o and 'Error reading' in e and 'reference.fa' in e and 'Traceback' not in e, (o + e).strip()[-300:])
rc, o, e = sh(f'{U} python {RUN}/skill/examples/view_bam.py {W}/b.cram 2 {W}/ref.gone; echo rc=$?')
check('view_bam.py <cram> 2 <reference.fa> works with the UR target gone (3rd arg resolves it): Mapped 5642 Unmapped 2, rc 0', 'Mapped: 5642' in o and 'Unmapped: 2' in o and o.strip().endswith('rc=0'), o.strip()[-200:])
os.rename(W + '/ref.gone', W + '/ref.fa')
