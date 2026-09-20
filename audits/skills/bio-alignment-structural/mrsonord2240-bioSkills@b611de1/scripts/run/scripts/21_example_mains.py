"""Run the __main__ blocks of examples/foldseek_search.py and examples/foldmason_msa.py from a COPY of the Skill, after replacing only the hard-coded
placeholder names (query.pdb, /path/to/afdb, structures/) with real data - the placeholders are the one thing the shipped examples cannot run with.
Asserts on the printed content. Run inside WSL (cwd = run/, after 20_input2 built work/in2)."""
import os, re, shutil, subprocess, sys
sys.dont_write_bytecode = True
D = 'data/real_pdb/'; w = os.path.abspath('work/in21'); shutil.rmtree(w, ignore_errors=True); os.makedirs(w + '/structures')
ex = os.path.abspath('skill/examples')
# ---- foldseek_search __main__ against the real AFDB Swiss-Prot with the default cap (200): expects the cap warning
src = open(ex + '/foldseek_search.py', encoding='utf-8').read()
db = '/mnt/openscience/audit-envs/alignment/public-data/foldseek-db/Alphafold_Swiss-Prot'
assert "'/path/to/afdb'" in src and "'query.pdb'" in src
open(w + '/fs_main.py', 'w', encoding='utf-8').write(src.replace("'/path/to/afdb'", repr(db)))
shutil.copy(D + '1MBN.pdb', w + '/query.pdb')
p = subprocess.run([sys.executable, '-B', 'fs_main.py'], cwd=w, capture_output=True, text=True)
out = p.stdout.split('Top 20 Foldseek hits:')[-1]
print('foldseek_search __main__ rc=%d\n%s%s' % (p.returncode, 'Top 20 Foldseek hits:' + out, p.stderr[-300:]))
assert p.returncode == 0 and 'Warning: 200 rows = the --max-seqs cap' in p.stdout and 'AF-P02185-F1-model_v6' in out and 'Confident structural hits' in out
# ---- foldmason_msa __main__ on 4 real structures (structures/*.pdb)
src = open(ex + '/foldmason_msa.py', encoding='utf-8').read()
for f in ('1MBN', '1A6M', '2LHB', '1HCK'): shutil.copy(D + f + '.pdb', w + '/structures/')
open(w + '/fm_main.py', 'w', encoding='utf-8').write(src)
p = subprocess.run([sys.executable, '-B', 'fm_main.py'], cwd=w, capture_output=True, text=True)
print('foldmason_msa __main__ rc=%d\n%s%s' % (p.returncode, '\n'.join(l for l in p.stdout.splitlines() if l.strip() and not l.startswith(('Input', 'Tmp'))) [-900:], p.stderr[-300:]))
assert p.returncode == 0 and 'files ->' in p.stdout and 'Per-column LDDT:' in p.stdout and os.path.exists(w + '/family_msa_aa.fa')
print('ALL ASSERTIONS OK')
