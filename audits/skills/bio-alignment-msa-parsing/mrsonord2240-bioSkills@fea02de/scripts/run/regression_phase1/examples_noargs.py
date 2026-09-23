"""Shipped-means-runnable: every example script that takes an alignment path, run from the COPY with NO arguments (falls back to examples/data/),
from a scratch cwd so nothing is written into the Skill copy. Asserts on printed content, not on the exit code."""
import os, subprocess, sys
from common import *
scratch = os.path.join(DATA, 'noargs_work'); os.makedirs(scratch, exist_ok=True)
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'}
EXPECT = {   # a token that only appears when the example computed something on the shipped data (6 x 20 protein / 3 x 11 A2M)
 'analyze_alignment.py': 'Alignment: 6 sequences, 20 columns', 'a2m_a3m_io.py': '9 match columns', 'clean_alignment.py': 'Saved to cleaned_alignment.fasta',
 'consensus_sequence.py': 'Consensus (100% threshold)', 'find_conserved.py': 'Fully conserved positions', 'gap_analysis.py': 'Gaps per sequence',
 'henikoff_weights.py': 'Kish effective sample size', 'mi_apc.py': 'exceed the null', 'neff.py': 'Neff (62% threshold'}
for name, token in EXPECT.items():
    p = subprocess.run([sys.executable, os.path.join(EX, name)], cwd=scratch, capture_output=True, text=True, env=env, timeout=300)
    check(f'{name} with NO argument runs on the shipped data and prints "{token}"', p.returncode == 0 and token in p.stdout and not p.stderr.strip(), f'rc {p.returncode} {p.stderr.strip()[-120:]}')
# muscle5_column_confidence.py needs an .efa by design (argv), and msa_utils.py is a library
p = subprocess.run([sys.executable, os.path.join(EX, 'muscle5_column_confidence.py')], cwd=scratch, capture_output=True, text=True, env=env)
check('muscle5_column_confidence.py with no argument fails with a usage-level IndexError (documented: needs the .efa path)', p.returncode != 0 and 'IndexError' in p.stderr, p.stderr.strip().splitlines()[-1][:100])
import py_compile
compiled = []
for f in sorted(os.listdir(EX)):
    if f.endswith('.py'):
        try:
            py_compile.compile(os.path.join(EX, f), cfile=os.path.join(scratch, f + 'c'), doraise=True); compiled.append(f)
        except py_compile.PyCompileError as e:
            print('COMPILE ERROR', f, e)
check('all 11 example modules py_compile', len(compiled) == 11, str(compiled))
summary()
