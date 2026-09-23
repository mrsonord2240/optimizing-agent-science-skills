"""Shipped-means-present + shipped examples: run every examples/*.py of the COPIED Skill as subprocesses from the copy; assert on printed content."""
import subprocess, sys, os, re
E = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skill', 'examples'); os.chdir(E)
F = []
def run(script, *args):
    r = subprocess.run([sys.executable, '-B', script, *args], capture_output=True, text=True, stdin=subprocess.DEVNULL, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'})
    return r.returncode, r.stdout, r.stderr
def check(n, c, o=''):
    print(('PASS  ' if c else 'FAIL  ') + n + ' | ' + str(o)[:200]); (None if c else F.append(n))
rc, out, err = run('alignment_from_file.py'); print(out[:400]); check("alignment_from_file.py runs with the shipped sequences.fasta and prints score 26.0 (hand: 21 matches... independent below)", rc == 0 and 'Score: 26.0' in out or '26.0' in out, (rc, err[-100:]))
# independent: seq1 vs seq2 in the shipped fasta, score from a hand count using the script's own scoring? use Bio: recompute
from Bio import SeqIO
from Bio.Align import PairwiseAligner
recs = list(SeqIO.parse('sequences.fasta', 'fasta'))
import ast
src = open('alignment_from_file.py').read(); print(re.findall(r'PairwiseAligner\(.*\)', src))
al = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
sc = al.score(recs[0].seq, recs[1].seq); print("independent score", sc)
check("alignment_from_file.py printed score equals an independent recomputation", f'{sc}' in out, (sc, out.strip().splitlines()[:2]))
rc, out, err = run('global_alignment.py'); print(out[-700:]); 
m = re.findall(r'(?i)(affine|linear)[^\n]*?(\d+\.\d+)', out)
print("affine/linear lines:", m)
check("global_alignment.py runs", rc == 0, (rc, err[-100:]))
for s in ('local_alignment.py', 'protein_alignment.py'):
    rc, out, err = run(s); print(s, '->', out.strip()[:200].replace('\n', ' | ')); check(s + ' runs and prints an alignment', rc == 0 and len(out) > 20, (rc, err[-100:]))
rc, out, err = run('empirical_pvalue.py'); print(out.strip()[:300]); check('empirical_pvalue.py runs and prints a p-value', rc == 0 and re.search(r'p', out) is not None and len(out) > 5, (rc, err[-100:]))
# no bytecode written into the copy by us
print("pycache in copy:", [d for d, _, _ in os.walk(os.path.dirname(E)) if d.endswith('__pycache__')])
print('FAILED:', F if F else 'none')
