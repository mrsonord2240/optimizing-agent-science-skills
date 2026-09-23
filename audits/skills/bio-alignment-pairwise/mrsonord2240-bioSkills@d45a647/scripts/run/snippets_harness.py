r"""Extract every ```python block from the COPIED SKILL.md (run\skill\SKILL.md) and exec them in ONE shared namespace, in
document order, then assert on the state (not just 'no exception').
Runs on Windows venv AND in WSL env `alignment` (pywfa/mappy blocks only work in WSL: the Skill says so).
User-supplied variables the snippets refer to (query/target/reference/fragment/read/ref.fa) are seeded:
target = real human HBB CDS (NM_000518.5); query = target with 3% SYNTHETIC edits (seed 4);
reference/fragment = SYNTHETIC 620-nt reference with the 20-nt fragment at [300,320] (the Skill's own comment says score 40, span [[300,320]]);
ref.fa/read for mappy = SYNTHETIC 5 kb reference and a 1 kb read (3% edits) cut from [2000,3000]."""
import re, io, os, sys, random, contextlib, warnings
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'work_' + ('wsl' if sys.platform.startswith('linux') else 'win'))
os.makedirs(WORK, exist_ok=True); os.chdir(WORK)
import shutil
shutil.copy(os.path.join(HERE, 'skill', 'examples', 'sequences.fasta'), 'sequences.fasta')
from Bio import SeqIO
from Bio.Align import PairwiseAligner
target = str(next(SeqIO.parse(os.path.join(HERE, 'data', 'hbb_cds_mammals.fasta'), 'fasta')).seq).upper()
random.seed(4)
def mutate(s, rate):
    out = []
    for ch in s:
        r = random.random()
        if r < rate / 3: out.append(random.choice([c for c in 'ACGT' if c != ch]))
        elif r < 2 * rate / 3: pass
        elif r < rate: out += [ch, random.choice('ACGT')]
        else: out.append(ch)
    return ''.join(out)
query = mutate(target, 0.03)
random.seed(11)
rnd = lambda n: ''.join(random.choice('ACGT') for _ in range(n))
fragment = 'GATTACAGATTACCAGGCTA'
reference = rnd(300) + fragment + rnd(300)
random.seed(21)
ref5k = rnd(5000); read = mutate(ref5k[2000:3000], 0.03)
open('ref.fa', 'w').write('>ref\n' + ref5k + '\n')
ns = {'query': query, 'target': target, 'reference': reference, 'fragment': fragment, 'read': read}
txt = open(os.path.join(HERE, 'skill', 'SKILL.md'), encoding='utf-8').read()
blocks = re.findall(r'```python\n(.*?)```', txt, re.S)
ok = fail = 0; snap = {}; results = []
for i, b in enumerate(blocks, 1):
    buf = io.StringIO()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', DeprecationWarning)   # any deprecated API in a shipped snippet becomes a failure
            with contextlib.redirect_stdout(buf):
                exec(compile(b, f'<SKILL block {i}>', 'exec'), ns)
        ok += 1; st = 'OK  '
    except Exception as e:
        fail += 1; st = f'FAIL {type(e).__name__}: {str(e)[:90]}'
    first = b.strip().splitlines()[0][:60]
    print(f"block {i:2d} [{st}] {first!r} | stdout: {buf.getvalue()[:160]!r}")
    if not st.startswith('OK'): continue
    if 'nw_striped_sat' in b and 'r' in ns: snap['parasail'] = ns['r'].score; snap['parasail_sat'] = ns['r'].saturated
    if "mode='NW', task='distance'" in b and 'd' in ns: snap['edlib'] = ns['d']
    if 'WavefrontAligner' in b and 'r' in ns: snap['pywfa'] = ns['r'].score; snap['pywfa_cigar'] = ns['r'].cigarstring[:40]
    if 'mappy' in b and 'h' in ns: snap['mappy'] = (ns['h'].ctg, ns['h'].r_st, ns['h'].r_en, ns['h'].mapq)
    if 'end_gap_score = 0.0' in b: snap['semi_both'] = (ns['alignment'].score, ns['alignment'].aligned[0].tolist())
    if 'open_left_deletion_score' in b: snap['semi_query'] = (ns['alignment'].score, ns['alignment'].aligned[0].tolist())
print(f"\n{ok}/{len(blocks)} blocks executed without exception, {fail} failed (DeprecationWarning promoted to error)")
print("snap:", snap)
# ---- state assertions vs independent ground truth ----
F = []
def check(n, c, o=''):
    print(('PASS  ' if c else 'FAIL  ') + n + ' | ' + str(o))
    if not c: F.append(n)
aff = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-1)
lev = PairwiseAligner(mode='global', match_score=0, mismatch_score=-1, open_gap_score=-1, extend_gap_score=-1)
if 'parasail' in snap:
    check('parasail snippet score == Biopython (the Skill\'s own comment) and not saturated', snap['parasail'] == aff.score(target, query) and not snap['parasail_sat'], (snap['parasail'], aff.score(target, query)))
if 'edlib' in snap:
    check('edlib snippet distance == -Levenshtein via Biopython (the Skill\'s comment)', snap['edlib'] == -lev.score(target, query), (snap['edlib'], -lev.score(target, query)))
if 'pywfa' in snap:
    x, o, e = 4, 6, 2
    bio = PairwiseAligner(mode='global', match_score=0, mismatch_score=-x, open_gap_score=-(o + e), extend_gap_score=-e)
    check('pywfa snippet score == Biopython (the Skill\'s comment)', snap['pywfa'] == bio.score(target, query), (snap['pywfa'], bio.score(target, query)))
if 'mappy' in snap:
    check('mappy snippet hits the planted locus 2000..3000 (+-30)', abs(snap['mappy'][1] - 2000) <= 30 and abs(snap['mappy'][2] - 3000) <= 40, snap['mappy'])
check('semiglobal snippet 1 (end_gap_score=0): 40.0 and target span [[300, 320]] (Skill comment)', snap.get('semi_both') == (40.0, [[300, 320]]), snap.get('semi_both'))
check('semiglobal snippet 2 (one-sided): 40.0 and [[300, 320]]', snap.get('semi_query') == (40.0, [[300, 320]]), snap.get('semi_query'))
print('FAILED:', F if F else 'none')
